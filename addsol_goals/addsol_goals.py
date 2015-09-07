# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-2016 Addition IT Solutions Pvt. Ltd. (<http://www.aitspl.com>).
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

from openerp import models, fields, api, _
    
class addsol_goals(models.Model):
    _name = 'addsol.goals'
    
    
    name = fields.Char("Name", required=True)
    user_id = fields.Many2one('res.users', string="Salesperson", required=True)
    period_id = fields.Many2one('addsol.date.periods', "Period", required=True)
    product_line_ids = fields.One2many('addsol.target.products','target_id', 'Product Lines')
    
    @api.one
    @api.constrains('period_id')
    def _check_periodicity_dates(self):
        """ This constraint is used for can not assign same period """
        for periodic_ids in self.browse(self.ids):
            domain =[
                 ('period_id.st_date', '=', periodic_ids.period_id.st_date),
                 ('period_id.ed_date', '=', periodic_ids.period_id.ed_date),
                 ('user_id', '=', periodic_ids.user_id.id),
            ]
            no_repeat_date = self.search_count(domain)
            if no_repeat_date > 1:
                raise Warning(_('Can not assign same period to salesperson'))
        return True
    
class addsol_target_products(models.Model):
    _name = 'addsol.target.products'
    
    target_id = fields.Many2one('addsol.goals')
    product_id = fields.Many2one('product.product', "Product", required=True)
    quantity = fields.Float("Quantity", required=True)
    

class addsol_date_periods(models.Model):
    _name = 'addsol.date.periods'
    
    name = fields.Char("Name", required=True)
    st_date = fields.Date("Start date", required=True)
    ed_date = fields.Date("End Date", required=True)

class addsol_res_users(models.Model):
    # Inherits user for add it on addsol.goals
    _inherit = 'res.users'

    goal_ids = fields.One2many('addsol.goals', 'user_id', string='Goals',
        readonly=True, copy=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
