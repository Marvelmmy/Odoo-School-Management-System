from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class Kelas(models.Model):
    _name = 'om_school.kelas'  # Model name
    _description = 'Class'  # Model description

    # Fields definition
    name = fields.Char(string='Class Name', required=True) 
    guru_id = fields.Many2one('om_school.guru', string='Class Teacher')
    murid_ids = fields.One2many('om_school.murid', 'kelas_id', string='Students')
    display_name = fields.Char(compute="_compute_display_name", store=True)

    # Function to compute display name with teacher name
    @api.depends('name', 'guru_id')
    def _compute_display_name(self):
        for rec in self:
            if rec.guru_id:
                rec.display_name = f"{rec.name} - {rec.guru_id.nama}"
            else:
                rec.display_name = rec.name
