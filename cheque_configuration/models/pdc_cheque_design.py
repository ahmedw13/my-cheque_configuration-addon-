from odoo import api, fields, models


class PdcChequeDesign(models.Model):
    _name = 'pdc.cheque.design'
    _description = 'PDC Cheque Design'
    _rec_name = 'bank_name'
    _order = 'bank_name'

    bank_name = fields.Char(
        string='Bank Name',
        required=True
    )

    bank_code = fields.Char(
        string='Bank Code',
        required=True
    )


    date_top = fields.Float(
        string='Top'
    )

    date_right = fields.Float(
        string='Right'
    )

    date_width = fields.Float(
        string='Width'
    )

    date_font_size = fields.Float(
        string='Font Size'
    )

    date_letter_spacing = fields.Float(
        string='Letter Spacing'
    )

    date_courier = fields.Boolean(
        string='Courier New'
    )

    date_bold = fields.Boolean(
        string='Bold'
    )


    name_top = fields.Float(
        string='Top'
    )

    name_right = fields.Float(
        string='Right'
    )

    name_width = fields.Float(
        string='Width'
    )

    name_font_size = fields.Float(
        string='Font Size'
    )

    name_letter_spacing = fields.Float(
        string='Letter Spacing'
    )

    name_bold = fields.Boolean(
        string='Bold'
    )


    amount_num_top = fields.Float(
        string='Top'
    )

    amount_num_right = fields.Float(
        string='Right'
    )

    amount_num_width = fields.Float(
        string='Width'
    )

    amount_num_font_size = fields.Float(
        string='Font Size'
    )

    amount_num_letter_spacing = fields.Float(
        string='Letter Spacing'
    )

    amount_num_bold = fields.Boolean(
        string='Bold'
    )


    amount_word_top = fields.Float(
        string='Top'
    )

    amount_word_right = fields.Float(
        string='Right'
    )

    amount_word_width = fields.Float(
        string='Width'
    )

    amount_word_font_size = fields.Float(
        string='Font Size'
    )

    amount_word_letter_spacing = fields.Float(
        string='Letter Spacing'
    )

    amount_word_center = fields.Boolean(
        string='Center Text',
        default=True
    )

    amount_word_line_height = fields.Float(
        string='Line Height',
        default=1.4
    )


    _sql_constraints = [
        (
            'unique_bank_code',
            'unique(bank_code)',
            'Bank Code must be unique. A cheque design already exists for this Bank Code.'
        ),
    ]


    @staticmethod
    def _add_px(style, property_name, value):
        """
        Add a CSS property using px when the value is greater than zero.
        Zero means the property was not configured.
        """
        if value is not False and value is not None and value > 0:
            style.append(f'{property_name}: {value:g}px;')

    def _build_style(
        self,
        top=None,
        right=None,
        width=None,
        font_size=None,
        letter_spacing=None,
        courier=False,
        bold=False,
        center=False,
        line_height=None,
    ):
        style = [
            'position: absolute;',
        ]

        self._add_px(style, 'top', top)
        self._add_px(style, 'right', right)
        self._add_px(style, 'width', width)
        self._add_px(style, 'font-size', font_size)
        self._add_px(style, 'letter-spacing', letter_spacing)

        if courier:
            style.append(
                "font-family: 'Courier New', Courier, monospace;"
            )

        if bold:
            style.append('font-weight: bold;')

        if center:
            style.append('text-align: center;')

        if line_height is not None and line_height is not False:
            style.append(f'line-height: {line_height:g};')

        return ' '.join(style)


    def get_date_style(self):
        self.ensure_one()

        return self._build_style(
            top=self.date_top,
            right=self.date_right,
            width=self.date_width,
            font_size=self.date_font_size,
            letter_spacing=self.date_letter_spacing,
            courier=self.date_courier,
            bold=self.date_bold,
        )


    def get_name_style(self):
        self.ensure_one()

        return self._build_style(
            top=self.name_top,
            right=self.name_right,
            width=self.name_width,
            font_size=self.name_font_size,
            letter_spacing=self.name_letter_spacing,
            bold=self.name_bold,
        )


    def get_amount_num_style(self):
        self.ensure_one()

        return self._build_style(
            top=self.amount_num_top,
            right=self.amount_num_right,
            width=self.amount_num_width,
            font_size=self.amount_num_font_size,
            letter_spacing=self.amount_num_letter_spacing,
            bold=self.amount_num_bold,
        )


    def get_amount_word_style(self):
        self.ensure_one()

        return self._build_style(
            top=self.amount_word_top,
            right=self.amount_word_right,
            width=self.amount_word_width,
            font_size=self.amount_word_font_size,
            letter_spacing=self.amount_word_letter_spacing,
            center=self.amount_word_center,
            line_height=self.amount_word_line_height,
        )


    def _apply_to_cheque_style(self):
        """
        Synchronize this design with the existing
        pdc.cheque.style record having the same bank code.
        """
        self.ensure_one()

        if not self.bank_code:
            return

        style = self.env['pdc.cheque.style'].search(
            [
                ('bank_code', '=', self.bank_code),
            ],
            limit=1
        )

        if not style:
            return

        style.write({
            'date_style': self.get_date_style(),
            'name_style': self.get_name_style(),
            'amount_num_style': self.get_amount_num_style(),
            'amount_word_style': self.get_amount_word_style(),
        })


    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        for record in records:
            record._apply_to_cheque_style()

        return records


    def write(self, vals):
        result = super().write(vals)

        for record in self:
            record._apply_to_cheque_style()

        return result