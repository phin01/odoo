from odoo import fields, models, api

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float(required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ])
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")


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
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'
            # Refuse all other offers
            record.property_id.property_offer_ids.filtered(lambda o: o.id != record.id).action_refuse_offer()

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'