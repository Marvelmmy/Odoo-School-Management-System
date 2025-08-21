from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.models import NewId 

class Guru(models.Model):
    _name = "om_school.guru"  # Model name
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Inherit mail features
    _description = "Information"
    _rec_name = "nama" 

    # Fields definition
    nama = fields.Char(string="Name", required=True, tracking=True)
    kelas_wali_id = fields.Many2one(
        'om_school.kelas', string='Class Teacher', 
        help="Class taught as the homeroom teacher"
    )
    alamat = fields.Char(string="Address", required=True, tracking=True)
    no_telp = fields.Char(string="Phone Number", required=True, tracking=True)
    ref = fields.Char(string='Reference', default=lambda self: _('New'))
    jumlah_siswa = fields.Integer(
        string="Number of Students", compute="_compute_jumlah_siswa", store=True
    )
    is_active = fields.Boolean(string="Status", default=True)

    # Generate reference sequence
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['ref'] = self.env['ir.sequence'].next_by_code('school.guru')
        return super(Guru, self).create(vals_list)

    # Validate phone number
    @api.constrains('no_telp')
    def check_no_telp(self):
        for rec in self:
            if rec.no_telp and not rec.no_telp.isdigit():
                raise ValidationError(_("Phone number must contain digits only!"))
            
    # validasi untuk nomor unik supaya tidak ada double di data
    @api.constrains('no_telp')
    def unique_no_telp(self):
        for rec in self:
            if not rec.no_telp:
                continue
            domain = [('no_telp', '=', rec.no_telp)]
            if isinstance(rec.id, NewId):
                pass
            else:
                domain.append(('id', '!=', rec.id))
                
            existing_record = self.env['om_school.guru'].search(domain, limit=1)
            
            
            if existing_record:
                raise ValidationError(_('Nomor telepon ini sudah ada di dalam database.'))

    # Display name with reference in Many2one fields
    def name_get(self):
        result = []
        for rec in self:
            display = f"{rec.nama} ({rec.ref})" if rec.ref else rec.nama
            result.append((rec.id, display))
        return result
    
    # Compute the number of students per guru
    @api.depends('kelas_wali_id', 'kelas_wali_id.murid_ids')
    def _compute_jumlah_siswa(self):
        for guru in self:
            if guru.kelas_wali_id:
                guru.jumlah_siswa = len(guru.kelas_wali_id.murid_ids)
            else:
                guru.jumlah_siswa = 0

    def action_toggle_murid(self):
        for guru in self:
            kelas = guru.kelas_wali_id
            if kelas:
                for murid in kelas.murid_ids:
                    murid.is_active = not murid.is_active
        return True
