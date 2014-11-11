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

from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging

_logger = logging.getLogger(__name__)


class transstat_module_wiz(osv.osv_memory):

    """ Check Language"""
    _name = "transstat.module.wiz"
    _description = "Module Language Status"

    _columns = {
        'wiz_id': fields.many2one('transstat.wiz'),
        'module_id': fields.many2one('ir.module.module', 'Module'),
        'nb_tot': fields.integer(string='Strings total'),
        'nb_trans': fields.integer(string='Strings translated'),
        'percent': fields.integer(string='% translated'),
    }

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


class transstat_wiz(osv.osv_memory):

    """ Check Language"""

    _name = "transstat.wiz"
    _description = "Check Language"

    _columns = {
        'lang': fields.selection(tools.scan_languages(), 'Language', required=True),
        'state': fields.selection([('init', 'init'), ('done', 'done')], 'Status', readonly=True),
        'module_ids': fields.one2many('transstat.module.wiz', 'wiz_id', 'Modules'),
    }
    _defaults = {
        'state': 'init',
    }

    def lang_show(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        wiz = self.browse(cr, uid, ids, context)[0]
        wizmod = self.pool.get('transstat.module.wiz')
        mod_obj = self.pool.get('ir.module.module')
        tran_obj = self.pool.get('ir.translation')
        for mod in mod_obj.browse(cr, uid, mod_obj.search(cr, uid, [('state', '=', 'installed')])):
            nb_tot = 0
            nb_trans = 0
            for tran in tran_obj.browse(cr, uid, tran_obj.search(cr, uid,
                                                                 [('module', '=', mod.name), ('lang', '=', wiz.lang)])):
                nb_tot += 1
                if tran.value:
                    nb_trans += 1

            percent = nb_trans * 100 / nb_tot if nb_tot > 0 else 0
            _logger.warning('Calc %s %d, %d', mod.name, nb_tot, nb_trans)
            wizmod.create(cr, uid,
                          {'wiz_id': ids[0],
                           'module_id': mod.id,
                           'nb_tot': nb_tot,
                           'nb_trans': nb_trans,
                           'percent': percent})

        self.write(cr, uid, ids, {'state': 'done'})
        _logger.warning('returning')

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'transstat.wiz',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': wiz.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
