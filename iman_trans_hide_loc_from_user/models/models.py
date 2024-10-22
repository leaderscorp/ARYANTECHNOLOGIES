from odoo import models, fields, api
from odoo.exceptions import ValidationError


class iman_trans_hide_loc_from_user(models.Model):
    _inherit = 'stock.picking'

    loc_ids = fields.Many2many(
        # related="user_id.location_ids"
        compute='compute_loc_ids'
    )

    def compute_loc_ids(self):
        self.loc_ids = self.env.user.location_ids.ids

    dest_loc_ids = fields.Many2many(
        # related="user_id.dest_location_ids"
        compute='compute_dest_loc_ids'
    )

    def compute_dest_loc_ids(self):
        self.dest_loc_ids = self.env.user.dest_location_ids.ids


    pick_ids = fields.Many2many(
        # related="user_id.picking_type_ids"
        compute='compute_pick_ids'
    )
    def compute_pick_ids(self):
        self.pick_ids = self.env.user.picking_type_ids.ids

    # def rec_to_user(self, check_rec_id, check_user_ids):
    #         if check_rec_id is False:
    #             pass
    #         elif check_rec_id.id in check_user_ids:
    #             pass
    #         else:
    #             print('else')
    #             raise ValidationError(
    #                 f"You are trying to use '{check_rec_id.display_name}' source location, but uou are only allowed to use these source location: \n {', '.join(check_user_ids.mapped('name'))}")

    @api.constrains('picking_type_id', 'user_id')
    def _check_valid_pick(self):
        if self.user_id: # so that odoobot user is not interrupted
            for rec in self:
                if rec.picking_type_id is False:
                    pass
                elif rec.picking_type_id.id in rec.pick_ids.ids:
                    pass
                else:
                    raise ValidationError(
                        f"You are trying to use '{rec.picking_type_id.display_name}' operation type, but you are only allowed to use these operation type: \n  {', '.join(rec.pick_ids.mapped('name'))}" )

    @api.constrains('location_id', 'user_id')
    def _check_valid_loc(self):
        if self.user_id:
            for rec in self:
                if rec.location_id is False:
                    pass
                elif rec.location_id.id in rec.loc_ids.ids:
                    pass
                else:
                    # print('else')
                    raise ValidationError(
                        f"You are trying to use '{rec.location_id.display_name}' source location, but uou are only allowed to use these source location: \n {', '.join(rec.loc_ids.mapped('name'))}" )


    @api.constrains('location_dest_id', 'user_id')
    def _check_valid_dest_loc(self):
        if self.user_id:
            for rec in self:
                if rec.location_dest_id is False:
                    pass
                elif rec.location_dest_id.id in rec.dest_loc_ids.ids:
                    pass
                else:
                    raise ValidationError(f"You are trying to use '{rec.location_dest_id.display_name}' destination location, but you are only allowed to use these destination locations: \n  {', '.join(rec.dest_loc_ids.mapped('name'))}" )
