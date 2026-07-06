# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'

    tax_ids = fields.Many2many(
        'account.tax',
        string='Taxes',
        check_company=True,
        context={'active_test': False}
    )
    # Currency field required for Monetary calculations
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', store=True)

    price_subtotal = fields.Monetary(compute='_compute_repair_totals', string='Subtotal', store=True)
    price_tax = fields.Float(compute='_compute_repair_totals', string='Tax Amount', store=True)
    price_total = fields.Monetary(compute='_compute_repair_totals', string='Total', store=True)

    @api.depends('product_uom_qty', 'price_unit', 'tax_ids')
    def _compute_repair_totals(self):
        for move in self:
            if move.repair_id:
                # Utilizing standard Odoo tax compute logic
                taxes = move.tax_ids.compute_all(
                    move.price_unit,
                    move.currency_id,
                    move.product_uom_qty,
                    move.product_id,
                    move.repair_id.partner_id
                )
                move.price_subtotal = taxes['total_excluded']
                move.price_tax = taxes['total_included'] - taxes['total_excluded']
                move.price_total = taxes['total_included']
            else:
                move.price_subtotal = 0.0
                move.price_tax = 0.0
                move.price_total = 0.0


class RepairOrder(models.Model):
    _inherit = 'repair.order'

    # ── Relational field linking invoices to this repair order ─────────────
    invoice_ids = fields.Many2many(
        comodel_name='account.move',
        relation='repair_order_account_move_rel',
        column1='repair_id',
        column2='move_id',
        string='Invoices',
    )

    invoice_count = fields.Integer(
        string='Invoice Count',
        compute='_compute_invoice_count',
        store=True,
    )

    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', store=True)
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, compute='_compute_amounts')
    amount_tax = fields.Monetary(string='Taxes', store=True, compute='_compute_amounts')
    amount_total = fields.Monetary(string='Grand Total', store=True, compute='_compute_amounts')

    @api.depends('move_ids.price_subtotal', 'move_ids.price_tax', 'move_ids.price_total')
    def _compute_amounts(self):
        for order in self:
            order.amount_untaxed = sum(order.move_ids.mapped('price_subtotal'))
            order.amount_tax = sum(order.move_ids.mapped('price_tax'))
            order.amount_total = sum(order.move_ids.mapped('price_total'))



    # ── Compute ────────────────────────────────────────────────────────────
    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.invoice_ids)

    # ── Action: Create Invoice ─────────────────────────────────────────────
    def action_create_repair_invoice(self):
        """
        Create a customer invoice directly from the repair order.

        In Odoo 17+ the old 'operations' and 'fees_lines' One2many fields
        were removed. Parts are now tracked through stock.move records on
        move_ids. We build invoice lines from those moves; if none exist we
        fall back to a single line for the repair service itself.
        """
        self.ensure_one()

        if not self.partner_id:
            raise UserError(
                _('Please set a customer on the repair order before creating an invoice.')
            )

        # ── Build invoice lines from stock moves (Parts tab in Odoo 17-19) ─
        invoice_line_vals = []

        # move_ids holds all stock moves tied to this repair order.
        # We skip cancelled/draft/scrapped moves — only confirmed/done parts.
        for move in self.move_ids.filtered(
            lambda m: m.state not in ('cancel', 'draft')
            and not m.scrap_id

        ):
            if not move.product_id:
                continue

            # Resolve income account via product template
            account = (
                move.product_id.product_tmpl_id
                .get_product_accounts()
                .get('income')
            )

            line = {
                'product_id': move.product_id.id,
                'name': move.product_id.display_name,
                # 'quantity' field name changed in Odoo 17 (was product_uom_qty on moves)
                'quantity': move.quantity if hasattr(move, 'quantity') else move.product_uom_qty,
                'product_uom_id': move.product_uom.id,
                'price_unit': move.price_unit,
                'tax_ids': move.tax_ids,
            }

            if account:
                line['account_id'] = account.id

            # Pull taxes from the product, filtered to current company
            taxes = move.product_id.taxes_id.filtered(
                lambda t: t.company_id == self.company_id
            )
            if taxes:
                line['tax_ids'] = [(6, 0, taxes.ids)]

            invoice_line_vals.append((0, 0, line))

        # ── Fallback: one service line for the whole repair ────────────────
        if not invoice_line_vals:
            invoice_line_vals.append((0, 0, {
                'name': _('Repair Service: %s') % (self.name or ''),
                'quantity': 1.0,
                'price_unit': self.amount_total if hasattr(self, 'amount_total') else 0.0,
            }))

        # ── Create the invoice ─────────────────────────────────────────────
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'repair_id': self.id,
            'job_completion_date': self.job_completion_date,
            'invoice_origin': self.name,
            'ref': self.name,
            'invoice_line_ids': invoice_line_vals,
            'invoice_date': self.job_completion_date,
            'description_text': self.description_text,
            'site_location': self.site_location,
            'narration': _('Invoice generated from Repair Order: %s') % self.name,
        })

        # ── Link invoice back to repair order ──────────────────────────────
        self.invoice_ids = [(4, invoice.id)]

        # ── Open the newly created invoice form ────────────────────────────
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoice'),
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }

    # ── Action: Smart button → open all linked invoices ───────────────────
    def action_view_invoices(self):
        """Open all invoices linked to this repair order."""
        self.ensure_one()
        invoice_ids = self.invoice_ids.ids

        if len(invoice_ids) == 1:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Invoice'),
                'res_model': 'account.move',
                'res_id': invoice_ids[0],
                'view_mode': 'form',
                'target': 'current',
            }

        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoices'),
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', invoice_ids)],
            'target': 'current',
        }

    def copy(self, default=None):
        new_order = super().copy(default)

        for old_move, new_move in zip(self.move_ids, new_order.move_ids):
            new_move.write({
                'price_unit': old_move.price_unit,
            })

        return new_order