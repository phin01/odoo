from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name asc"

    name = fields.Char(required=True)
    sequence = fields.Integer()
    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='property_type_id',
        string='Properties'
    )
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_type_id',
        string='Offers'
    )
    offer_count = fields.Integer(
        compute='_compute_offer_count',
        string='Number of Offers'
    )
    

    # ---------------------------------------
    # CONSTRAINTS
    # ---------------------------------------

    _unique_name = models.Constraint(
        definition='UNIQUE(name)',
        message='Property Type already exists!')
    

    # ---------------------------------------
    # COMPUTE METHODS
    # ---------------------------------------
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)