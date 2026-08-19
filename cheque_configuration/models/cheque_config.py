# pdc_cheque_style.py
from odoo import models, fields, api

class PdcChequeStyle(models.Model):
    _name = 'pdc.cheque.style'
    _description = 'PDC Cheque Style Configuration'
    _rec_name = 'bank_code'

    bank_reference = fields.Many2one("bank.reference", string="Bank Reference")
    bank_code = fields.Char(string="Bank Code", compute='_compute_bank_code', store=True, readonly=False, required=True)
    main_style = fields.Char(string="Main Style")
    name_style = fields.Char(string="Name Style")
    date_style = fields.Char(string="Date Style")
    amount_num_style = fields.Char(string="Amount Number Style")
    amount_word_style = fields.Char(string="Amount Word Style")

    @api.depends('bank_reference')
    def _compute_bank_code(self):
        for record in self:
            if record.bank_reference and record.bank_reference.bank:
                record.bank_code = record.bank_reference.bank.bank_code
            else:
                record.bank_code = record.bank_code or ""


