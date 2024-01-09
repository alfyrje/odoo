from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tags"
    _order = "name asc"

    _sql_constraints = [('check_unique', 'unique(name)', 'A property tag name should be unique.')]

    name = fields.Char(required = True)
    color = fields.Integer()