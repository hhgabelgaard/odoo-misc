# -*- coding: utf-8 -*-
##############################################################################
#
#    Translation Status
#    Copyright (C) 2014 Hans Henrik Gabelgaard
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
from openerp import tools
import logging

_logger = logging.getLogger(__name__)

class transstat_module_wiz(models.TransientModel):
    """ Check Language"""
    _name = "transstat.module.wiz"
    _description = "Module Language Status"
    
    wiz_id = fields.Many2one('transstat.wiz')
    module_id = fields.Many2one('ir.module.module')
    nb_tot = fields.Integer(string = 'Strings total')
    nb_trans = fields.Integer(string = 'Strings translated')
    percent = fields.Integer(string = '% translated')
    
    
#     nb_tot = fields.Integer(string = 'Strings total', compute = '_compute_transstat')
#     nb_trans = fields.Integer(string = 'Strings translated', compute = '_compute_transstat')
#     percent = fields.Integer(string = '% translated', compute = '_compute_transstat')
#     
#     @api.one
#     @api.depends('module_id','wiz_id.lang')
#     def _compute_transstat(self):
#         self.nb_tot = self.env['ir.translation'].search_count([('module_id','=', self.module_id.id),('lang','=',self.wiz_id.lang)])
#         self.nb_trans = self.env['ir.translation'].search_count([('module_id','=', self.module_id.id),('lang','=',self.wiz_id.lang),('value','!=', False)])
#         self.percent = rec.nb_trans * 100 / rec.nb_tot
#         _logger.warning('Calc %s %d, %d', self.module_id.name, self.nb_tot, self.nb_trans)
#         
class transstat_wiz(models.TransientModel):
    """ Check Language"""

    _name = "transstat.wiz"
    _description = "Check Language"
    
    def _langsel(self):
        return tools.scan_languages()
    
    lang = fields.Selection(selection= '_langsel',string='Language', required=True)
    state = fields.Selection([('init','init'),('done','done')], string= 'Status', readonly=True, default='init')
    module_ids = fields.One2many('transstat.module.wiz', 'wiz_id')
    
    
    
    @api.multi
    def lang_show(self):
        wizmod = self.env['transstat.module.wiz']
        for rec in self.env['ir.module.module'].search([('state','=','installed')]):
            nb_tot = self.env['ir.translation'].search_count([('module','=', rec.name),('lang','=',self.lang)])
            nb_trans = self.env['ir.translation'].search_count([('module','=', rec.name),('lang','=',self.lang),('value','!=', False)])
            percent = nb_trans * 100 / nb_tot if nb_tot > 0 else 0
            _logger.warning('Calc %s %d, %d', rec.name, nb_tot, nb_trans)
            wizmod.create({'wiz_id' : self.ids[0],
                           'module_id' : rec.id,
                           'nb_tot' : nb_tot,
                           'nb_trans': nb_trans,
                           'percent' : percent})
            
            _logger.warning("wizmod %s", rec.name)
        self.state = 'done'
        _logger.warning('returning')
        view = self.env.ref('translation_status.view_transstat_language')

        return True
#      {
#               'name': 'Show Translation Status',
#               'type': 'ir.actions.act_window',
#               'res_model': 'transtat.wiz',
#               'view_mode': 'form',
#               'view_type': 'form',
#               'res_id': self.ids[0],
#               'views': [(view.id, 'form')],
#               'view_id': view.id,
#               'target': 'new',
#               
#                }