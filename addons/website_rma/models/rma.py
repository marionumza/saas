# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from harpiya import fields, models, api, _
from datetime import date, time, datetime

class RMAOrder(models.Model):
    _name = "rma.order"
    _description = "RMA Orders"
    _order = "id desc"
    
    name = fields.Char(string='RMA Reference',default=lambda self: self.env['ir.sequence'].next_by_code('rma.order'))
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    order_id = fields.Many2one('sale.order', string='Sale Order', required=True)
    create_date = fields.Datetime(string='Creation Date', required=True, index=True, help="Date on which RMA order is created.")
    rma_product_id = fields.Many2one('product.product', required=True, string='Return Product')
    rma_product_uom_qty = fields.Float(string='Return Quantity', required=True, default=1.0)
    rma_product_uom = fields.Many2one('uom.uom', string='UOM')
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange', default=lambda self: self.env.user)
    team_id = fields.Many2one('crm.team', 'Sales Team')
    company_id = fields.Many2one('res.company', 'Company')
    #order_line = fields.One2many('sale.order.line', 'order_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)
    reason = fields.Text('Reason of Return')
    stock_picking_ids = fields.One2many('stock.picking','rma_order_id',"Stock Picking", compute='_compute_picking')
    return_order_ids = fields.One2many('stock.picking','rma_order_id',"Return Picking",compute='_compute_return_order')
    delivery_count = fields.Integer(string='Delivery Orders', compute='_compute_picking_ids')
    return_count = fields.Integer(string='Return Order', compute='_compute_return_order_ids')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('approved', 'Approved'),
        ('return', 'Return'),
        ('cancel','Cancel'),
        ], string='Status', default='draft')
    
    def _compute_picking(self):
        picking_list = []
        for picking in self.order_id.picking_ids:
            if picking.picking_type_code == 'outgoing':
                picking_list.append(picking.id)
        self.stock_picking_ids=[(6,0,picking_list)]
        return
        
    def _compute_return_order(self):
        return_order_list = []
        return_order_ids = self.env['stock.picking'].search([ ('rma_order_id', '=', self.id),('picking_type_code', '=', 'incoming')])
        for picking in return_order_ids:
            return_order_list.append(picking.id)
        self.return_order_ids=[(6,0,return_order_list)]
        return   
            
    def action_confirm(self):
        self.write({'state':'confirmed'})
        return
        
    def action_approved(self):
        self.write({'state':'approved'})
        return
    
    def action_return(self):
        self.write({'state':'return'})
        return
        
    def action_cancel(self):
        self.write({'state':'cancel'})
        return                


    def action_view_delivery(self): 
        self.ensure_one() 
        return { 'name': 'Stock Picking', 
                'type': 'ir.actions.act_window', 
                'view_mode': 'tree,form', 
                'res_model': 'stock.picking', 
                'domain': [('sale_id','=',self.order_id.id),('picking_type_code', '=', 'outgoing')], 
    }

    def action_view_return_order(self): 
        self.ensure_one() 
        return { 'name': 'Stock Picking', 
                'type': 'ir.actions.act_window', 
                'view_mode': 'tree,form', 
                'res_model': 'stock.picking', 
                'domain': [('rma_order_id', '=', self.id)], 
    }
                
    '''@api.onchange('order_id')
    def onchange_picking_code(self):
        if self.code == 'incoming':
            self.default_location_src_id = self.env.ref('stock.stock_location_suppliers').id
            self.default_location_dest_id = self.env.ref('stock.stock_location_stock').id
        elif self.code == 'outgoing':
            self.default_location_src_id = self.env.ref('stock.stock_location_stock').id
            self.default_location_dest_id = self.env.ref('stock.stock_location_customers').id'''
                            
            
    def _compute_picking_ids(self):
        for order in self:
            stock_picking_ids = self.env['stock.picking'].search([('sale_id','=',order.order_id.id),('picking_type_code', '=', 'outgoing')])
            order.delivery_count = len(stock_picking_ids)

    def _compute_return_order_ids(self):
        for return_order in self:
            return_order_ids = self.env['stock.picking'].search([ ('rma_order_id', '=', return_order.id),('picking_type_code', '=', 'incoming')])
            return_order.return_count = len(return_order_ids) 
            
                
class StockPicking(models.Model):
    _inherit = "stock.picking"
    
    rma_order_id = fields.Many2one('rma.order',"RMA Order")

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    return_order_count = fields.Integer(string='Return Orders', compute='_compute_return_ids')
    
    def action_rma_order_view(self): 
        self.ensure_one() 
        return { 'name': 'Return Order', 
                'type': 'ir.actions.act_window', 
                'view_mode': 'tree,form', 
                'res_model': 'rma.order', 
                'domain': [('order_id', '=', self.id)], 
    }
    
    def _compute_return_ids(self):
        for return_order in self:
            rma_order_ids = self.env['rma.order'].search([('order_id','=',self.id)])
            return_order.return_order_count = len(rma_order_ids)  
        
class ResPartner(models.Model):
    _inherit = "res.partner"
    
    return_order_count = fields.Integer(string='Return Orders', compute='_compute_return_ids')
    
    def action_rma_order_view(self): 
        self.ensure_one() 
        return { 'name': 'Return Order', 
                'type': 'ir.actions.act_window', 
                'view_mode': 'tree,form', 
                'res_model': 'rma.order', 
                'domain': [('partner_id', '=', self.id)], 
    }
    
    def _compute_return_ids(self):
        for partner_id in self:
            rma_order_ids = self.env['rma.order'].search([('partner_id','=',int(partner_id.id))])
            partner_id.return_order_count = len(rma_order_ids)
                
class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    def _create_returns(self):
        # Prevent copy of the carrier and carrier price when generating return picking
        # (we have no integration of returns for now)
        new_picking, pick_type_id = super(StockReturnPicking, self)._create_returns()
        picking = self.env['stock.picking'].browse(new_picking)
        picking.write({'carrier_id': False,
                       'carrier_price': 0.0})
        return new_picking, pick_type_id    
            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    
