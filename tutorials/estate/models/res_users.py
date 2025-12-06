from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    estate_property_ids = fields.One2many("estate.property", "salesperson_id", string="Properties", domain=['|', ('state', '=', 'new'), ('state', '=', 'offer_received')])