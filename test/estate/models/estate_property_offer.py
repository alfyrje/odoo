from odoo import fields, models, api
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offers"
    _order = "price desc"

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'An offer price must be strictly positive.'),
        
    ]

    price = fields.Float()
    status = fields.Selection([('Accepted', 'Accepted'), ('Refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.property_id.date_availability + relativedelta(days=record.validity)
    @api.onchange("date_deadline")
    def _inverse_date_deadline(record):
        if record.property_id.date_availability and record.date_deadline:
            record.validity = (fields.Date.from_string(record.date_deadline) - fields.Date.from_string(record.property_id.date_availability)).days

    def action_accept(self):
        for record in self:
            if record.status != 'Refused' and record.property_id.state != 'Offer Accepted':
                record.status = 'Accepted'
                record.property_id.selling_price = record.price
                record.property_id.buyer = record.partner_id
                record.property_id.state = 'Offer Accepted'

    def action_refuse(self):
        for record in self:
            if record.status != 'Accepted':
                record.status = 'Refused'

    @api.model
    def create(self, vals):
        self.env['estate.property'].browse(vals['property_id']).set_state_offer_received()
        return super().create(vals)