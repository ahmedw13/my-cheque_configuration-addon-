from odoo import api, fields, models, _


class BankReference(models.Model):
    _name = 'bank.reference'

    name = fields.Char()
    bank = fields.Many2one("account.account", string="Bank", required=True)
    cheque_paper_num = fields.Integer("Number of Cheques")
    start_seq = fields.Integer("Sequence Start On", required=True)
    last_so_seq = fields.Integer("Last SO Sequence", compute="_compute_last_so_seq")
    sequence = fields.One2many("bank.reference.seq", "bank_reference")
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')], default="draft")

    @api.depends('start_seq')
    def _compute_last_so_seq(self):
        for rec in self:
            default_seq = False
            if rec.start_seq:
                default_seq = rec.start_seq - 1
                pdc_wizard = self.env['pdc.wizard'].search([('bank_reference', '=', rec.id)])
                if pdc_wizard:
                    seq = []
                    for pdc in pdc_wizard:
                        if pdc.reference:
                            seq.append(pdc.reference)
                    if seq:
                        default_seq = max(seq)
            rec.last_so_seq = default_seq

    def create_seq_lines(self):
        if self.start_seq:
            start = self.start_seq - 1
            for line in range(self.cheque_paper_num):
                start += 1
                self.write({"sequence": [(0, 0, {'seq': start})]})
            self.state = 'confirmed'


class BankReferenceSequence(models.Model):
    _name = 'bank.reference.seq'

    bank_reference = fields.Many2one("bank.reference")
    seq = fields.Integer("Sequence")
