from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(required=True)
    

    # ---------------------------------------
    # CONSTRAINTS
    # ---------------------------------------

    _unique_name = models.Constraint(
        definition='UNIQUE(name)',
        message='Property Tag already exists!')