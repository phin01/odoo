from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(required=True)
    

    # ---------------------------------------
    # CONSTRAINTS
    # ---------------------------------------

    _unique_name = models.Constraint(
        definition='UNIQUE(name)',
        message='Property Type already exists!')