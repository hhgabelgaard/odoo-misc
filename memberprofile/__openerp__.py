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


{
    'name': "Member Profile",

    'summary': """
        Profile fields for the Scout""",

    'description': """
        All the Scout related fields pr member pr "unit"
    """,

    'author': "Hans Henrik Gabelgaard",
    'website': "http://www.yourcompany.com",


    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
     'data': [
         # 'security/ir.model.access.csv',
         'memberprofile_view.xml',
     ],
    # only loaded in demonstration mode
    #     'demo': [
    #         'demo.xml',
    #     ],
}