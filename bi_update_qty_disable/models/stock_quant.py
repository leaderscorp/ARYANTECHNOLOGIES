# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, _
from odoo.exceptions import ValidationError

class StockQuant(models.Model):
	_inherit = 'stock.quant'

	inventory_quantity = fields.Float()
	is_true = fields.Boolean()
	def _search(self, domain, *args, **kwargs):
		qty = super()._search(domain, *args, **kwargs)
		is_qty_group = self.env.user.has_group('bi_update_qty_disable.group_onhand_qty_user')
		if is_qty_group:
			self.is_true = False
		else:
			self.is_true = True
		return qty


class productTemplate(models.Model):
	_inherit = 'product.template'

	def write(self,vals):
		res = super(productTemplate, self).write(vals)
		if not self.env.user.has_group("bi_update_qty_disable.group_onhand_qty_user"):
			raise ValidationError(
				_("You don't have access rights for update on hand quantity!"))
		return res


class productProduct(models.Model):
	_inherit = 'product.product'

	def write(self,vals):
		res = super(productProduct, self).write(vals)
		if not self.env.user.has_group("bi_update_qty_disable.group_onhand_qty_user"):
			raise ValidationError(
				_("You don't have access rights for update on hand quantity!"))
		return res