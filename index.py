#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Flask, url_for, render_template, request, flash, redirect
import requests
import json
import random
from datetime import datetime


app = Flask(__name__)

params = {
    "ApiKey": "5fa1e6f9-cba3-4d61-b0f5-35a85713b689",
    "SearchRequest": {
        "Keyword": "smartphone",
        "SortBy": "relevance",
        "Pagination": {
            "ItemsPerPage": 10,
            "PageNumber": 0
        },
        "Filters": {
            "Price": {
                "Min": 0,
                "Max": 1500
            },
            "Navigation": "smartphone",
            "IncludeMarketPlace": 'false',
            "Brands": [
                "apple"
            ],
            "Condition": 'null'
        }
    }
}

r = requests.post('https://api.cdiscount.com/OpenApi/json/Search', data=json.dumps(params))

res_array = []
ret = []
times = []
time_elapsed = []
items = []

@app.route('/le_juste_prix/', methods=['GET', 'POST'])
def juste_prix():
    msgs = ['C\'est plus petit', 'C\'est plus grand', 'Félicitations, vous avez le juste prix !',
            'Entrée incorrecte.']
    items.append(r.json()['Products'])

    if request.method == 'POST':
        if len(times) > 0:
            time = times[0]
        else:
            time = datetime.now()

        times.append(datetime.now())
        time_elapsed.append(datetime.now() - time)

        res = request.form['response']

        random_nb = int(request.form.get('random_nb'))

        item_name = items[0][random_nb]['Name']
        item_brand = items[0][random_nb]['Brand']
        item_img = items[0][random_nb]['MainImageUrl']
        item_prc = items[0][random_nb]['BestOffer']['SalePrice']
        try:
            if isinstance(float(res), float):
                if int(res) > float(item_prc):
                    res_array.append(int(res))
                    ret.append(msgs[0])
                elif int(res) < float(item_prc):
                    res_array.append(int(res))
                    ret.append(msgs[1])
                elif int(res) == float(item_prc):
                    res_array.append(int(res))
                    ret.append(msgs[2])
        except ValueError:
            res_array.append(res)
            ret.append(msgs[3])

        return render_template('juste_prix.html', msg=ret, res_array=res_array, name=item_name, brand=item_brand,
                               img=item_img, time=time_elapsed, random_nb=random_nb)
    else:
        random_nb = random.randint(0, 9)

        if len(res_array) > 0:
            res_array.pop()
            ret.pop()
            times.pop()
            time_elapsed.pop()
            items.pop()

        print(res_array)

        item_name = items[0][random_nb]['Name']
        item_brand = items[0][random_nb]['Brand']
        item_img = items[0][random_nb]['MainImageUrl']

        return render_template('juste_prix.html', random_nb=random_nb, name=item_name, brand=item_brand, img=item_img)

if __name__ == '__main__':
    app.run(host="0.0.0.0")