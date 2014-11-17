# -*- coding: utf-8 -*-
##############################################################################
#
#    Member Profile
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


class res_partner(models.Model):
    _inherit = 'res.partner'

    memberprofile_id = fields.One2many('memberprofile.member', 'partner_id',
                                       string="Member",
                                       company_dependent=True)
    memberno = fields.Integer(string="Membernumber")


class memberprofile(models.Model):
    _name = "memberprofile.member"
    _description = 'Members'

    _inherits = {
        'res.partner': 'partner_id',
    }

    partner_id = fields.Many2one('res.partner', required=True,
            string='Related Partner', ondelete='restrict',
            help='Partner-related data of the user', auto_join=True)
    scout_name = fields.Char()
    display_name = fields.Char(compute='_compute_display_name', inverse='_inverse_display_name')

    @api.one
    @api.depends('scout_name', 'partner_id.name')     # this definition is recursive
    def _compute_display_name(self):
        if self.partner_id:
            self.display_name = self.partner_id.display_name + ' (' + self.scout_name + ')'
        else:
            self.display_name = self.name + ' (' + self.scout_name + ')'

    @api.one
    def _inverse_display_name(self):
        names = self.display_name.split('c')
        
        self.name = names[0].strip()

    

    
    
