from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.http import request
from datetime import timedelta
from num2words import num2words


class inherit_account_account(models.Model):
    _inherit = 'account.account'
    _description = 'add bank_code account.account '

    bank_code = fields.Char(string='Bank Code', default=False)


class inherit_pdc_wizard(models.Model):
    _inherit = 'pdc.wizard'
    _description = 'PDC Wizard'

    bank_reference = fields.Many2one("bank.reference", string="Bank Reference", domain="[('state', '=', 'confirmed')]")
    bank_code = fields.Char(related='bank_reference.bank.bank_code', string='cheque_name', store=True)
    reference_seq = fields.Many2one("bank.reference.seq", string="Cheque Reference",
                                    domain="[('bank_reference', '=', bank_reference)]")

    display_date = fields.Boolean(string='Display Date')
    close_date = fields.Boolean(string='Close Date', default=False)
    display_close_date = fields.Char('display_close_date', compute='_display_close_date')

    pay_type = fields.Selection([('0', 'Partner'), ('1', 'Agent')], string='Pay Type', default='0')
    display_name = fields.Char('display_name', compute='_display_name')

    close_pay_name = fields.Boolean(string='Close Pay Name', default=False)
    display_close_pay_name = fields.Char('display_close_pay_name', compute='_display_close_pay_name')

    @api.constrains('reference')
    def check_reference(self):
        if self.reference:
            bank_reference_seq = self.env['bank.reference.seq'].search(
                [('bank_reference', '=', self.bank_reference.id), ('seq', '=', self.reference)], limit=1)
            if not bank_reference_seq:
                raise UserError("Cheque Reference you trying to enter doesn't exist")
            else:
                self.reference_seq = bank_reference_seq.id

    @api.onchange('bank_reference')
    def _onchange_cheque_ref(self):
        if self.bank_reference:
            next_seq = self.bank_reference.last_so_seq + 1
        else:
            next_seq = self.bank_reference.start_seq
        self.reference = next_seq
        self.bank_reference.last_so_seq = next_seq

    @api.depends('close_date')
    def _display_close_date(self):
        for rec in self:
            f_close_date = rec.close_date

            rec.display_close_date = ''

            if f_close_date == True:
                rec.display_close_date = '_________________'

    @api.depends('pay_type')
    def _display_name(self):
        for rec in self:
            pay_type = rec.pay_type

            if pay_type == '1':
                rec.display_name = rec.agent
            else:
                rec.display_name = rec.partner_id.name

    @api.depends('close_pay_name')
    def _display_close_pay_name(self):
        for rec in self:
            close_pay_name = rec.close_pay_name

            rec.display_close_pay_name = ''

            if close_pay_name:
                rec.display_close_pay_name = 'يصرف للمستفيد الأول'
