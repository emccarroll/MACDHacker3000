import requests, json

def write_json(stock_name, timeframe):  
    response = requests.get(f'https://www.alphavantage.co/query?function=MACD&symbol={stock_name}&interval={timeframe}&series_type=open&apikey=CW3985DDZ00FVGZ5')
    if (response.status_code != 404):
        parsed = response.json()
        MACD_data = str(parsed['Technical Analysis: MACD'])
        text_file = open(f"StockData/{stock_name}_{timeframe}.json", "w")
        text_file.write(MACD_data)
        text_file.close()
        print(f'Successfully wrote {stock_name}_{timeframe}.json')
    else:
        print('Error code 404')


##### Change arguments below and run script #####
##### arg1 is ticker symbol, arg2 can be 'daily', 'weekly', 'monthly' #####
write_json('LYB', 'daily')