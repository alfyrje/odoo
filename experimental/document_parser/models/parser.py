from odoo import fields, models

class Parser(models.Model):
    _name = 'parser.parser'
    _description = 'Document parsers'

    name = fields.Char(required = True)
    parse_method = fields.Selection([('Python', 'Python'), ('AI', 'AI')], default = 'Python', required = True)
    detect_func = fields.Text()
    parse_func = fields.Text()
    request_ids = fields.One2many("parser.request", "parser_id")

    