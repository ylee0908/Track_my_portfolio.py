import requests
import json
from flask import Flask, render_template
from .databaseaccessors import DatabaseAccessors

app = Flask(__name__)

api_headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "12cdeace0fmsh1f3e797a34584d7p180ce2jsn85de5922bf64"
}


@app.route("/API")
def summary():
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-summary"

    querystring = {"region": "US", "lang": "en"}

    response = requests.request("GET", url, headers=api_headers, params=querystring)

    return str(response.text)


@app.route("/<string:symbol>")
def load_detail(symbol):
    return f"Hello, {symbol}!"

'''
{% block body %}
    <form action="{{ url_for('hello') }}" method="post">
        <input type="text" name="name" placeholder="Enter your name">
        <button>Submit</button>
    </form>
{% endblock %}
'''

@app.route("/stocks")
def stocks():
    # Talk to our database
    database_preferences = DatabaseAccessors.get_my_preferred_stocks()

    # Talk to Yahoo Finance API
    query_object = create_query_object(database_preferences)
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-quotes"
    api_response = requests.request("GET", url, headers=api_headers, params=query_object)
    api_results_array = json.loads(api_response.text)['quoteResponse']['result']

    # Combine the results
    my_stock_info = collate_all_stock_info(database_preferences, api_results_array)

    # Return something to the screen
    return create_final_display(my_stock_info)


def create_query_object(database_info):
    # From the database I get a dictionary of dictionaries
    # The key of the outside dictionary is the ticker

    tickers = []
    for key in database_info:
        tickers.append(str(key))

    query_symbols = ','.join(tickers)
    query_object = {"region": "US", "lang": "en", "symbols": query_symbols}
    return query_object


def collate_all_stock_info(database_preferences, api_results_array):
    my_stock_info = []
    for stock in api_results_array:
        database_stock = database_preferences[str(stock['symbol'])]
        info_tuple = (str(stock['symbol']),
                      str(stock['longName']),
                      str(stock['regularMarketPrice']),
                      str(database_stock['nickname']),
                      str(database_stock['buyPrice']),
                      str(database_stock['sellPrice']),
                      str(database_stock['priority']))
        my_stock_info.append(info_tuple)
    return my_stock_info


def create_final_display(my_stock_info):
    return render_template("stock_list.html", stock_list=my_stock_info)
