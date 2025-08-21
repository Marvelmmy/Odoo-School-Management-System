from odoo import http
from odoo.http import request
import json 

# List of teachers restAPI
class GuruAPI(http.Controller):
    @http.route('/api/guru', type='http', auth='public', methods=['GET'], csrf=False) # API endpoint
    def get_teachers(self, **kw): # getting the list of teachers
        try:
            guru_list = request.env['om_school.guru'].sudo().search([])
        except Exception as e:
              return request.make_json_response({'status': 'error', 'message': str(e)})
        data_guru = []
        
        # adding the fields from the guru model to the json file
        for guru in guru_list:
            data_guru.append({
                'id': guru.id,
                'nama': guru.nama,
                'kelas': [
                    {'id': kelas.id, 'nama': kelas.name}
                    for kelas in guru.kelas_wali_id
                    ] if guru.kelas_wali_id else [],
                'alamat': guru.alamat,
                'no telp': guru.no_telp,
                'ref': guru.ref
            })
        
        return request.make_json_response(data_guru)

# list of students restAPI
class MuridAPI(http.Controller):
      @http.route('/api/murid', type='http', auth='public', methods=['GET'], csrf=False) # API endpoint
      def get_siswa(self, **kw):
            try:
                  murid_list = request.env['om_school.murid'].sudo().search([])
            except Exception as e:
                  return request.make_json_response({'status': 'error', 'message': str(e)})
            data_murid = []

            # adding the fields from the murid model to the json file
            for murid in murid_list:
                  data_murid.append({
                        'id': murid.id,
                        'nama': murid.nama,
                        'kelas': {
                        'id': murid.kelas_id.id if murid.kelas_id else False,
                        'nama': murid.kelas_id.name if murid.kelas_id else False,
                        'wali_kelas': murid.kelas_id.guru_id.nama if murid.kelas_id.guru_id else False},
                        'alamat': murid.alamat,
                        'no telp': murid.no_telp,
                        'ref': murid.ref 
                  })
            
            return request.make_json_response(data_murid)

# API endpoint to add new students
class ADDMuridAPI(http.Controller):
      @http.route('/api/murid/add', type='json', auth='public', methods=['POST'], csrf=False)
      def add_siswa(self, **kwargs):
            try: 
                # accepting data from the JSON request
                nama = kwargs.get('nama')
                kelas_id = kwargs.get('kelas_id')
                alamat = kwargs.get('alamat')
                no_telp = kwargs.get('no_telp')

                # validation
                if not nama or not kelas_id or not alamat or not no_telp:
                      return {'status': 'error', 'message': 'semua field wajib diisi!'}

                # Create record 
                murid = request.env['om_school.murid'].sudo().create({
                      'nama': nama,
                      'kelas_id': kelas_id,
                      'alamat': alamat,
                      'no_telp': no_telp
                })

                return {
                      'status': 'success',
                      'id': murid.id,
                      'ref': murid.ref, 
                      'message': f'Murid {murid.nama} berhasil ditambahkan!'
                }
            except ValueError as e:
                  return {'status': 'error', 'message': str(e)}
            except Exception as e:
                  return {'status': 'error', 'message': f"Terjadi error: {str(e)}"}
            
            # how to add new student via postman
        #                {
        #       "jsonrpc": "2.0",
        #        "method": "call",
        #        "params": {
        #            "nama": "nama murid",
        #            "kelas_id": "id kelas",
        #            "alamat": "alamat",
        #            "no_telp": "08xxxxxxxx"
        #        },
        #        "id": null
        #    }