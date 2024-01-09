from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero

class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Properties"
    _order = "id desc"
    
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'A property expected price must be strictly positive.'),
         ('check_selling_price', 'CHECK(selling_price >= 0)',
         'A property selling price must be positive.'),
    ]
    
    name = fields.Char(required = True)
    property_type_id = fields.Many2one("estate.property.type", string = "Property Type")
    description = fields.Text()
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string = "Offers")
    buyer = fields.Many2one("res.partner", copy = False)
    salesperson = fields.Many2one("res.users", default = lambda self: self.env.user)
    postcode = fields.Char()
    date_availability = fields.Date(copy = False, default =lambda self: fields.Date.today() + relativedelta(months = 3))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer(string = 'Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean(default = False)
    garden_area = fields.Integer(string = 'Garden Area (sqm)')
    garden_orientation = fields.Selection([('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')])
    active = fields.Boolean(default = True)
    state = fields.Selection([('New', 'New'), ('Offer Received', 'Offer Received'), ('Offer Accepted', 'Offer Accepted'), ('Sold', 'Sold'), ('Canceled', 'Canceled')]
                                                  , string = 'Status', required = True, copy = False, default = 'New')
    total_area = fields.Integer(compute = "_compute_total_area")
    best_price = fields.Float(compute = "_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price') or [0,]);

                
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'North'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_property_sold(self):
        for record in self:
            if record.state != 'Canceled':
                record.state = 'Sold'
            else:
                raise UserError('??')
    
    def action_property_canceled(self):
        for record in self:
            if record.state != 'Sold':
                record.state = 'Canceled'
            else:
                raise UserError('?')
            
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, 2):
                if record.selling_price < record.expected_price * 0.9:
                    raise ValidationError('The selling price cannot be lower than 90% of the expected price.')