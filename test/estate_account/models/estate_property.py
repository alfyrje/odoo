from odoo import models, Command

class EstateProperties(models.Model):
    _inherit = "estate.property"
    
    def action_property_sold(self):
        for record in self:
            partner_id = record.buyer.id if record.buyer else False
            invoice_vals = {
                'name':'Invoice',
                'partner_id': partner_id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name':'6% of the selling price',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name':'additional 100.00 from administrative fees',
                        'quantity': 1,
                        'price_unit': 100,
                    }),
                ],
            }
            self.env['account.move'].create(invoice_vals)
        return super().action_property_sold()