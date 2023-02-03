# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class IndexCustomApi(http.Controller):
    @http.route('/index_custom_api/product/api/', auth='public', website=False, csrf=False, type="json", methods=['GET', 'POST'])
    def index(self, **kw):
        # Code bar: code_bar (barcode)
        # Nom de l'article: product_name (name)
        #Cout du produit: product_cost (standard_price)
        if(kw.get('code_bar') and kw.get('product_name') and kw.get('product_cost')):
            code_bar = str(kw.get('code_bar'))
            product_name = kw.get('product_name')
            product_cost = kw.get('product_cost')
            values={
                "name": product_name,
                "standard_price": product_cost,
            }
            product_template = request.env['product.template'].sudo()
            existing_prod = product_template.search([('barcode', '=', code_bar)])
            if existing_prod:
                print('*'*80)
                print('updating record')
                existing_prod.write(values)

            else:
                print('*'*80)
                print('No bar code found')
        return kw