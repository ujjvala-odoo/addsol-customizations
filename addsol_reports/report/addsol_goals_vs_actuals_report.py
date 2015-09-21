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

#from openerp.osv import fields, osv
from openerp import models, fields, api, _
from openerp import tools


class goals_vs_actuals_report(models.Model):
    _name = "goals.vs.actuals.report"
    _description = ""
    _auto = False
    
    salesperson = fields.Char("Salesperson")
    name = fields.Char("Product Name")
    goal = fields.Integer("Goal Quantity")
    actual = fields.Integer("Actual Quantity")


    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'goals_vs_actuals_report')
        cr.execute("""
            CREATE view goals_vs_actuals_report as
                SELECT 
                    res.id as id,
                    res.name as salesperson, 
                    prd.name as name, 
                    sum(goal) as goal, 
                    sum(actual) as actual
                FROM 
                    ( SELECT res as res, product as product, goal,
                          NULL::float as actual
                    FROM   (SELECT res.id as res, pt.product_id as product, sum(pt.quantity) as goal
                        FROM resource_resource res
                            JOIN addsol_goals gl ON gl.user_id = res.user_id
                            JOIN addsol_target_products pt ON pt.target_id = gl.id
                            JOIN addsol_date_periods pd ON pd.id = gl.period_id
                        GROUP BY res.id, pt.id) goals
                    UNION  ALL
                    SELECT res, product, NULL::float as goal, actual
                    FROM   (SELECT res.id as res, invl.product_id as product, sum(invl.quantity) as actual
                            FROM resource_resource res
                                JOIN account_invoice inv ON inv.user_id = res.user_id
                                JOIN account_invoice_line invl ON invl.invoice_id = inv.id
                            GROUP BY res.id, invl.id) actuals
                    ) results
                    JOIN resource_resource res ON res.id = results.res
                    JOIN product_template prd ON prd.id = results.product 
                GROUP BY res.name, prd.name,res.id
        """)