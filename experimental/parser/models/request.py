from odoo import fields, models
from odoo.tools.safe_eval import safe_eval

class Request(models.Model):
    _name = 'parser.request'
    _description = 'Error request from clients'

    request_time = fields.Date()
    IP_address = fields.Char()
    request_content = fields.Text()
    return_content = fields.Text()
    client_id = fields.Many2one('parser.client')
    processed_by = fields.Many2one('parser.parser')

    def action_process_request(self):
        for record in self:
            detected = False
            parsers = self.env['parser.parser'].search([])
            for parser in parsers:
                if parser.parse_method == 'Python':
                    detect_func_code = parser.detect_func
                    if detect_func_code:
                        try: 
                            localdict = {
                                'content': record.request_content,
                                'result': None,
                            }
                            safe_eval(detect_func_code, localdict, mode = "exec", nocopy=True)
                            return_value = localdict['result']
                            if return_value is not None and return_value is True:
                                record.return_content = 'Detected ' + parser.name
                                record.processed_by = parser
                                detected = True
                                break
                        except Exception as e:
                            record.return_content = f'Error executing detect function for {parser.name}: {e}'
            if not detected: record.return_content = 'Unable to detect'

        