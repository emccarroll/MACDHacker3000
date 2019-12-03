import requests, json, time

def write_json(stock_name, timeframe):  
    response_macd = requests.get(f'https://www.alphavantage.co/query?function=MACD&symbol={stock_name}&interval={timeframe}&series_type=close&apikey=SKY470CWGO52HCSQ')
    response_sma50 = requests.get(f'https://www.alphavantage.co/query?function=SMA&symbol={stock_name}&interval={timeframe}&time_period=50&series_type=close&apikey=N29DY72L98XQRYRB')
    response_sma200 = requests.get(f'https://www.alphavantage.co/query?function=SMA&symbol={stock_name}&interval={timeframe}&time_period=200&series_type=close&apikey=CW3985DDZ00FVGZ5')
    response_RSI = requests.get(f'https://www.alphavantage.co/query?function=RSI&symbol={stock_name}&interval={timeframe}&time_period=10&series_type=close&apikey=N29DY72L98XQRYRB')
    response_stockprice = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_{timeframe.upper()}&symbol={stock_name}&outputsize=full&apikey=SKY470CWGO52HCSQ')
    if (response_macd.status_code != 404 or response_stockprice.status_code != 404):
        parsed_macd = response_macd.json()
        parsed_sma50 = response_sma50.json()
        parsed_sma200 = response_sma200.json()
        parsed_RSI = response_RSI.json()
        parsed_stockprice = response_stockprice.json()
        MACD_data = parsed_macd['Technical Analysis: MACD']
        sma50_data = parsed_sma50['Technical Analysis: SMA']
        sma200_data = parsed_sma200['Technical Analysis: SMA']
        RSI_data = parsed_RSI['Technical Analysis: RSI']
        l = []
        for key in parsed_stockprice.keys():
            l.append(key)
        stock_data = parsed_stockprice[l[1]]
        dict = {}
        for date in sma200_data:
            dict[date] = {}
            dict[date]["sma50"] = sma50_data[date]["SMA"]
            dict[date]["sma200"] = sma200_data[date]["SMA"]
            dict[date]['MACD_Signal'] = MACD_data[date]['MACD_Signal']
            dict[date]['MACD'] = MACD_data[date]['MACD']
            dict[date]['MACD_Hist'] = MACD_data[date]['MACD_Hist']
            dict[date]['RSI'] = RSI_data[date]['RSI']
            closing_price = stock_data[date]["4. close"]
            dict[date]["price"] = closing_price
                  #text_file = open(f"StockData/{stock_name}_{timeframe}.json", "w")
                  #text_file.write(str(dict))
                  # text_file.close()
        with open(f"StockData/{stock_name}_{timeframe}.json", "w") as fp:
           json.dump(dict,fp)
        print(f'Successfully wrote {stock_name}_{timeframe}.json')
    else:
        print('Error code 404')


def findCrossovers(stock_name, timeframe):
    ##text_file = open(f"StockData/{stock_name}_{timeframe}.json", "r")

    with open(f"StockData/{stock_name}_{timeframe}.json", "r") as json_file:
        data=json.load(json_file)
        for x in data:
            print('sma50: '+x["sma50"])

##### Change arguments below and run script #####
##### arg1 is ticker symbol, arg2 can be 'daily', 'weekly', 'monthly' #####

list = ['LYB', 'KMB', 'JPM', 'JNJ', 'GOOGL', 'GOOG', 'FB', 'AMZN', 'AAPL']
for name in list:
    write_json(name,'daily')
    time.sleep(60)
    write_json(name,'weekly')
#write_json('MSFT', 'daily')

#for name in list:
    #findCrossovers(name,'weekly')


