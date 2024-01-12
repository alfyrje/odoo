from odoo import fields, models

class Client(models.Model):
    _name = 'parser.client'
    _description = 'Clients using the service'

    name = fields.Char(required = True)
    authorize_key = fields.Char()
    key_expires = fields.Date()
    request_ids = fields.One2many('parser.request', 'client_id', string = 'Requests')