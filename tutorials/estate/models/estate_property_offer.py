from odoo import fields, models, api, _
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ])
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    property_type_id = fields.Many2one(related="property_id.property_type_id", string="Property Type", store=True)


    # ---------------------------------------
    # CONSTRAINTS
    # ---------------------------------------

    _positive_offer_price = models.Constraint(
        definition='CHECK(price > 0)',
        message='Offer price must be positive.')


    # ---------------------------------------
    # COMPUTE METHODS
    # ---------------------------------------

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date.date(), days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                delta = (record.date_deadline - record.create_date.date()).days
                record.validity = delta
            else:
                delta = (record.date_deadline - fields.Date.today()).days
                record.validity = delta
    

    # ---------------------------------------
    # BUTTON ACTIONS
    # ---------------------------------------

    def action_accept_offer(self):
        for record in self:
            record.property_id.selling_price = record.price   # triggers selling price validation before any state change
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'
            # Refuse all other offers
            record.property_id.property_offer_ids.filtered(lambda o: o.id != record.id).action_refuse_offer()

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'


    # ---------------------------------------
    # METHOD OVERRIDES
    # ---------------------------------------

    @api.model
    def create(self, vals):
        property_id = vals[0].get('property_id')
        if property_id:
            property_record = self.env['estate.property'].browse(property_id)
            if property_record.state not in ['new', 'offer_received']:
                raise UserError(_("Offer not allowed: Cannot make an offer on a property that is not new or in offer received state."))
        
        return super().create(vals)