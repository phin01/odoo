from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name asc"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='property_type_id',
        string='Properties'
    )
    

    # ---------------------------------------
    # CONSTRAINTS
    # ---------------------------------------

    _unique_name = models.Constraint(
        definition='UNIQUE(name)',
        message='Property Type already exists!')