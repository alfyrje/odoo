from odoo import fields, models

class Parser(models.Model):
    _name = 'parser.parser'
    _description = 'Document parsers'

    name = fields.Char(required = True)
    parse_method = fields.Selection([('Python', 'Python'), ('AI', 'AI')], default = 'Python', required = True)
