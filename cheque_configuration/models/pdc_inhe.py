from odoo import models, fields, api


class PdcWizardInherit(models.Model):
    _inherit = 'pdc.wizard'

    cheque_style_id = fields.Many2one(
        'pdc.cheque.style',
        string="Cheque Format",
        compute="_compute_cheque_style_id",
        store=True,
        readonly=False
    )

    main_style = fields.Char(related='cheque_style_id.main_style')
    name_style = fields.Char(related='cheque_style_id.name_style')
    date_style = fields.Char(related='cheque_style_id.date_style')
    amount_num_style = fields.Char(related='cheque_style_id.amount_num_style')
    amount_word_style = fields.Char(related='cheque_style_id.amount_word_style')

    @api.depends('bank_reference')
    def _compute_cheque_style_id(self):
        for rec in self:
            style_to_assign = self.env['pdc.cheque.style']

            if rec.bank_reference and rec.bank_reference.name:
                search_text = rec.bank_reference.name.upper()

                all_styles = self.env['pdc.cheque.style'].search([('bank_code', '!=', False)])
                filtered_style = all_styles.filtered(lambda s: s.bank_code.upper() in search_text)

                if filtered_style:
                    style_to_assign = filtered_style[0]
            rec.cheque_style_id = style_to_assign.id

    def get_boxed_date(self):
        if self.payment_date:
            return "  ".join(self.payment_date.strftime('%d%m%Y'))
        return ""
