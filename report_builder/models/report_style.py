# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class ReportStyle(models.Model):
    _name = "report.style"
    _description = "Report Style"

    name = fields.Char(required=True)
    text_color = fields.Char(
        help="Text color in valid RGB code (from #000000 to #FFFFFF)",
        default="#000000",
    )
    text_color_inherit = fields.Boolean(default=True)
    background_color = fields.Char(
        help="Background color in valid RGB code (from #000000 to #FFFFFF)",
        default="#FFFFFF",
    )
    background_color_inherit = fields.Boolean(default=True)
    font_style = fields.Selection(selection=lambda self: self._get_font_styles())
    font_style_inherit = fields.Boolean(default=True)
    font_weight = fields.Selection(selection=lambda self: self._get_font_weights())
    font_weight_inherit = fields.Boolean(default=True)
    font_size = fields.Selection(
        selection=lambda self: self._get_font_sizes(),
    )
    font_size_inherit = fields.Boolean(default=True)
    indent_level = fields.Integer()
    indent_level_inherit = fields.Boolean(default=True)
    prefix = fields.Char()
    prefix_inherit = fields.Boolean(default=True)
    suffix = fields.Char()
    suffix_inherit = fields.Boolean(default=True)
    rounding = fields.Integer()
    rounding_inherit = fields.Boolean(default=True)
    divider = fields.Selection(
        [
            ("1e-6", "µ"),
            ("1e-3", "m"),
            ("1", "1"),
            ("1e3", "k"),
            ("1e6", "M"),
        ],
        string="Factor",
        default="1",
    )
    divider_inherit = fields.Boolean(default=True)
    hide_empty = fields.Boolean(default=False)
    hide_empty_inherit = fields.Boolean(default=True)
    hide_always = fields.Boolean(default=False)
    hide_always_inherit = fields.Boolean(default=True)

    def _get_font_styles(self):
        return [
            ("normal", _("Normal")),
            ("italic", _("Italic")),
            ("oblique", _("Oblique")),
        ]

    def _get_font_weights(self):
        return [
            ("normal", _("Normal")),
            ("bold", _("Bold")),
            ("bolder", _("Bolder")),
            ("lighter", _("Lighter")),
        ]

    def _get_font_sizes(self):
        return [
            ("xx-small", _("XX-Small")),
            ("x-small", _("X-Small")),
            ("small", _("Small")),
            ("medium", _("Medium")),
            ("large", _("Large")),
            ("x-large", _("X-Large")),
            ("xx-large", _("XX-Large")),
            ("xxx-large", _("XXX-Large")),
        ]

    def _get_style(self, style=None):
        """Get style values from the current style or the given style."""
        if not style:
            style = {}
        if not self:
            return style
        return {
            "color": self.text_color
            or (self.text_color_inherit and style.get("color")),
            "background-color": self.background_color
            or (self.background_color_inherit and style.get("background-color")),
            "font-style": self.font_style
            or (self.font_style_inherit and style.get("font-style")),
            "font-weight": self.font_weight
            or (self.font_weight_inherit and style.get("font-weight")),
            "font-size": self.font_size
            or (self.font_size_inherit and style.get("font-size")),
            "padding-left": self.indent_level
            or (self.indent_level_inherit and style.get("padding"))
            or 1,
            "prefix": self.prefix or (self.prefix_inherit and style.get("prefix")),
            "suffix": self.suffix or (self.suffix_inherit and style.get("suffix")),
            "rounding": self.rounding
            or (self.rounding_inherit and style.get("rounding")),
            "divider": self.divider or (self.divider_inherit and style.get("divider")),
            "hide_empty": self.hide_empty
            or (self.hide_empty_inherit and style.get("hide_empty")),
            "hide_always": self.hide_always
            or (self.hide_always_inherit and style.get("hide_always")),
        }

    def _get_style_map(self):
        return [
            ("background-color", lambda r: r),
            ("color", lambda r: r),
            ("font-style", lambda r: r),
            ("font-weight", lambda r: r),
            ("font-size", lambda r: r),
            ("padding-left", lambda r: f"{r * 20}px"),
            ("border-radius", lambda r: f"{r}px"),
        ]

    def _get_style_css(self, style):
        css_style = self._get_style(style)
        computed_style = []
        for key, parse_style in self._get_style_map():
            if key in css_style:
                computed_style.append(f"{key}: {parse_style(css_style.get(key))}")
        return ";".join(computed_style), css_style
