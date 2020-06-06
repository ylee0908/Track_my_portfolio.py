import requests
from flask import Flask, render_template
import json
from .databaseaccessors import DatabaseAccessors

app = Flask(__name__)

api_headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': "86ab38246fmshded8bcac8ff0c75p14b81cjsn8feeaa8ce1aa"}

@app.route("/summary")
def summary():
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-summary"

    querystring = {"region": "US", "lang": "en"}

    response = requests.request("GET", url, headers=api_headers, params=querystring)

    return str(response.text)


@app.route("/stocks")
def stocks():

    database_preferences = DatabaseAccessors.get_my_preferred_stocks()

    query_object = create_query_symbols(database_preferences)
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-quotes"
    api_response = requests.request("GET", url, headers=api_headers, params=query_object)
    api_results_array = json.loads(api_response.text)["quoteResponse"]["result"]

    my_stock_info = collate_all_stock_info(database_preferences, api_results_array)

    return create_final_display(my_stock_info)

@app.route("/chart")
def load_detail():
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-chart"

    querystring = {"interval": "5m", "region": "US", "symbol": "AMRN", "lang": "en", "range": "1d"}

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': "23fd1f61dfmshccb8119fb5a82e6p1c1a3bjsnac942deff27b"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
