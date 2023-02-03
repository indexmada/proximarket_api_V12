# -*- coding: utf-8 -*-

from odoo import http, models, fields, api
from odoo.http import request

import requests
import json

class productTemplate(models.Model):
    _inherit = "product.template"

    def api_send_product(self):

        print('__'*80)
        self.send_created_product()
        print('Product successfully sent')
        return 'salut'


    def send_created_product(self):
        url = 'http://clicodeal.thewebsquare.com/' # # # A changer à l'url provenant du serveur PHP
        data = {'params': {
                                'code_bar': self.barcode,
                                'product_name': self.name,
                                'product_cost': self.standard_price
                }}
        print(data)
        headers = {'content-type':'application/json'}
        requests.get(url, data=json.dumps(data), headers=headers)
        return 'var'
