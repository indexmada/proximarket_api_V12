# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
from datetime import datetime

class IndexCustomApi(http.Controller):
    @http.route('/index_custom_api/product/api/', auth='public', website=False, csrf=False, type="json", methods=['GET', 'POST'])
    def index(self, **kw):
        # Code bar: code_bar (barcode)
        # Nom de l'article: product_name (name)
        #Cout du produit: product_cost (standard_price)
        # if(kw.get('code_bar') and kw.get('product_name') and kw.get('product_cost')):
        #     code_bar = str(kw.get('code_bar'))
        #     product_name = kw.get('product_name')
        #     product_cost = kw.get('product_cost')
        #     values={
        #         "name": product_name,
        #         "standard_price": product_cost,
        #     }
        #     product_template = request.env['product.template'].sudo()
        #     existing_prod = product_template.search([('barcode', '=', code_bar)])
        #     if existing_prod:
        #         print('*'*80)
        #         print('updating record')
        #         existing_prod.write(values)

        #     else:
        #         print('*'*80)
        #         print('No bar code found')
        return 'Salut'

    @http.route('/index_custom_api/product/req235/', auth='public', website=False, csrf=False, type="json", methods=['GET', 'POST'])
    def _index_api(self, **kw):
        domain = [('type','=', 'product')]
        # if kw.get('ugs'):
        #     domain += [('barcode', 'in', kw.get('ugs'))]
        products = request.env['product.template'].sudo().search(domain)
        data = []
        for product in products:
            product.write({"to_send": False})
            qty_tosend = 0
            stock_qty = request.env['stock.quant'].sudo().search([('product_tmpl_id', '=', product.id), ('location_id.usage', '=', 'internal'),('location_id.stock_cod','=', True)])
            for i in stock_qty:

                qty_tosend = qty_tosend + i.quantity 

            qty_tosend = (qty_tosend * product.seuil)/100
            values = {
                'name': product.name,
                'display_name': product.display_name,
                'standard_price': product.standard_price,
                'barcode': product.barcode,
                'qty_available': qty_tosend,
            }
            data.append(values)

        json_data = json.dumps(data)
        return json_data

    @http.route('/index_custom_api/sale_order/api/', auth='public', website=False, csrf=False, type="json", methods=['GET', 'POST'])
    def index_sale_order(self, **kw):
        login_ok = kw.get('login') and kw.get('login') == 'IndexMadaApi'
        password_ok = kw.get('password') and kw.get('password') == 'Indexconsapi2023'
        if login_ok and password_ok:
            if kw.get('orders'):
                # partner_id = request.env['res.partner'].browse(7).id
                orders = json.loads(kw.get('orders'))
                if orders:
                    for order in orders:
                        partner = request.env['res.partner'].sudo().search([('name', '=', order['partner_name'])], limit=1)
                        if not partner:
                            partner = request.env['res.partner'].sudo().create({'name': order['partner_name']})
                        if order['date_order']:
                            date_order = datetime.strptime(order['date_order'], '%d/%m/%Y').date()
                        else:
                            date_order = False
                        if order['order_line']:
                            line_tab = []
                            for line in order['order_line']:
                                line_vals = {}
                                product_id = request.env['product.product'].sudo().search([('barcode','=', line['barcode'])], limit=1)
                                if product_id:
                                    line_vals['product_id'] = product_id.id
                                    line_vals['product_uom_quantity'] = line['quantity'] or 1
                                    line_tab.append(line_vals)
                                else:
                                    line_vals = False

                        if line_tab and len(line_tab) != 0:
                            vals = {
                                "partner_id": partner.id,
                                "date_order": date_order or None,
                                "order_line": [(0,0, line_tab[0])]
                            }
                            new_order = request.env['sale.order'].sudo().create(vals)
                            count = 0
                            for l in line_tab:
                                if count != 0:
                                    new_order.sudo().write({'order_line': [(0,0, l)]})
                                count +=1
                        else:
                            return "No order created!"
        else:
            return 'You are not allowed to access this Api'
        return 'Order Successfully Created.'