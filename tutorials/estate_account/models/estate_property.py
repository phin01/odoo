from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = 'estate.property'



    # ---------------------------------------
    # METHOD OVERRIDES
    # ---------------------------------------

    def action_set_sold(self):
        print("Creating accounting entries for sold property...")
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.buyer_id.id,
            # 'invoice_line_ids': [
            #     Command.create({
            #     'name': f'Sale of property {self.name}',
            #     'quantity': 1,
            #     'price_unit': self.selling_price,
            # })],
        }
        self.env['account.move'].create(invoice_vals)
        super().action_set_sold()