import requests, json

def write_json(stock_name, timeframe):  
    response_macd = requests.get(f'https://www.alphavantage.co/query?function=MACD&symbol={stock_name}&interval={timeframe}&series_type=close&apikey=CW3985DDZ00FVGZ5')
    response_stockprice = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_{timeframe.upper()}&symbol={stock_name}&outputsize=full&apikey=CW3985DDZ00FVGZ5')
    if (response_macd.status_code != 404 or response_stockprice.status_code != 404):
        parsed_macd = response_macd.json()
        parsed_stockprice = response_stockprice.json()
        MACD_data = parsed_macd['Technical Analysis: MACD']
        stock_data = parsed_stockprice[list(parsed_stockprice.keys())[1]]
        for date in MACD_data:
            closing_price = stock_data[date]["4. close"]
            MACD_data[date]["price"] = closing_price
        text_file = open(f"StockData/{stock_name}_{timeframe}.json", "w")
        text_file.write(str(MACD_data))
        text_file.close()
        print(f'Successfully wrote {stock_name}_{timeframe}.json')
    else:
        print('Error code 404')


##### Change arguments below and run script #####
##### arg1 is ticker symbol, arg2 can be 'daily', 'weekly', 'monthly' #####
write_json('KMB', 'daily')