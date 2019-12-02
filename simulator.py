import json, requests,csv, time

#Simulators has 2 tasks:
#1. Scan "bought" list for potential sells, sell, remove from "bought", add trade to profits list
#2. Scan list of stocks for potential buys, add it to "bought" list


def findRSIGoodSpots(data_set, initialKey):
   # hello Eoghan
    goodSpots=[]
    temp= float(data_set[initialKey]["RSI"])

    for date in data_set:
        currentRSI=float(data_set[date]["RSI"])
       
        if((currentRSI>=70 and temp<70) or (currentRSI<=30 and temp>30)):
            goodSpots.append(date)
        temp=currentRSI
        
    return goodSpots



timeframe = "daily"

#returns list of points where there is a crossover
def findCrossovers(data_set, initialKey):

#data=[]      
        temp="red above black"
        # blackabovered=False
        blackabovered = float(data_set[initialKey]["MACD"]) >  float(data_set[initialKey]["MACD_Signal"])
        #print("2019-11-29 MACD = "+data_set["2019-11-29"]["MACD"])
        #print("2019-11-29 MACD_signal = "+data_set["2019-11-29"]["MACD_Signal"])
        #print(float(data_set["2019-11-29"]["MACD"]) >  float(data_set["2019-11-29"]["MACD_Signal"]))
        crossoverPoints = []
        for date in data_set:
            macd = float(data_set[date]["MACD"])
            signal = float(data_set[date]["MACD_Signal"])
           
            if(blackabovered!=(macd>signal)):
                crossoverPoints.append(date)
            blackabovered=macd>signal
        return crossoverPoints


        #do shit start
        # timeChange = 1
        # priceChange = 0
        # for crossOver in daysofcrossover:
        #     priceChange = findPriceChange(data_set,crossOver,timeChange)
        #     
        #do shit end
            

    




#for price range time units afterwards
def findPercentChange(data, current_time,time): 
    currentData = data[current_time]
    dates = list(data.keys())
    dataVals = list(data.values())
    currentTimeIndex = dates.index(current_time)
    futureData = dataVals[currentTimeIndex+ time]
    return abs(float(currentData["4. close"]) - float(futureData["4. close"]))/float((currentData["4. close"]))

# finds the average of the change
def findAvgPercentChange(data, timesofcrossover, time_change):
    # times of crossover is the key to the data in the dictonary
    average = 0
    number = 0
    for time in timesofcrossover:
        average = ((average * number) + findPercentChange(data, f"{time}:00", time_change)) /(number + 1)
        number += 1
    return average

# finds the average of the change
def findRSIAvgPercentChange(data, timesofcrossover, time_change):
    # times of crossover is the key to the data in the dictonary
    average = 0
    number = 0
    for time in timesofcrossover:
        average = ((average * number) + findPercentChange(data, f"{time}", time_change)) /(number + 1)
        number += 1
    return average


# def findPercentChange(data, current_time,time): 
#     currentData = data[current_time]
#     dates = list(data.keys())
#     dataVals = list(data.values())
#     currentTimeIndex = dates.index(current_time)
#     futureData = dataVals[currentTimeIndex+ time]
#     return abs(currentData["price"] - futureData["price"])/(currentData["price"])


# def findAvgPercentChange(data, times, time_change):
#     average = 0
#     number = 0
#     for i in range(len(data)):
#         average = ((average * number) + findPercentChange(data[i], times[i], time_change)) /(number + 1)
#         number += 1
#     return average


#https://www.alphavantage.co/query?function=MACD&symbol=MSFT&interval=60min&outputsize=full&series_type=open&apikey=CW3985DDZ00FVGZ5
#https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&outputsize=full&interval=60min&apikey=CW3985DDZ00FVGZ5

#gets hourly data for a given stock at a given date


# def MACD_zoom(stockname, date):
#     datapoints = []
#     for key in price_parsed_data:
#         if date in key:
#             dict = {}
#             #do stuff
#             dict["MACD"] = macd_parsed_data[key[:-3]]["MACD"]
#             dict["MACD_Signal"] = macd_parsed_data[key[:-3]]["MACD_Signal"]
#             dict["price"] = price_parsed_data[key]["4. close"]
#             datapoints.append(dict)
#     return datapoints




    
# for day in daysofcrossover:
#     datapoints = MACD_zoom("AMZN",day)
#     hoursofcrossover=findCrossovers(datapoints, "2019-11-29 13:00") 
    
#     print(findAvgPercentChange(datapoints, hoursofcrossover, 1)) #finds price change hourly


#datapoints=[]

#for day in daysofcrossover:

   # datapoints.append(MACD_zoom("AMZN",day))

#hoursofcrossover=findCrossovers(datapoints, "2019-11-29 13:00") 


#--------------------------------------------------------------------
#'''MAIN'''
#--------------------------------------------------------------------
#KEYS: SKY470CWGO52HCSQ, N29DY72L98XQRYRB, CW3985DDZ00FVGZ5
def getAvgChange(stockName, apikey):
    macd_response_data = requests.get(f'https://www.alphavantage.co/query?function=MACD&symbol={stockName}&interval=60min&outputsize=full&series_type=open&apikey={apikey}')
    price_response_data = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stockName}&outputsize=full&interval=60min&apikey={apikey}')
    macd_parsed_data = macd_response_data.json()
    price_parsed_data = price_response_data.json()
    
    macd_parsed_data = macd_parsed_data["Technical Analysis: MACD"]
    price_parsed_data = price_parsed_data["Time Series (60min)"]
    #with open(f"StockData/{stock_name}_{timeframe}.json", "r") as json_file:        
    #    data_set = json.load(json_file)    
    crossoverPoints=findCrossovers(macd_parsed_data, "2019-11-29 13:00")
    vals = []
    csvVals = [stockName]
    with open('stockData.csv', mode='a+') as stockData:
        stock_writer = csv.writer(stockData, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        for i in range(1,6):
            d = findAvgPercentChange(price_parsed_data, crossoverPoints, i)
            csvVals.append(d)
            vals.append("Hour "+ str(i) +": "+ str(d))
        stock_writer.writerow(csvVals)
    
    
    print(vals) #finds price change hourly



def getAvgRSIChange(stockName, apikey):
    rsi_response_data = requests.get(f'https://www.alphavantage.co/query?function=RSI&symbol={stockName}&interval=daily&time_period=14&series_type=open&apikey={apikey}')
    price_response_data = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stockName}&outputsize=full&interval=60min&apikey={apikey}')
    rsi_parsed_data = rsi_response_data.json()
    price_parsed_data = price_response_data.json()
    
    rsi_parsed_data = rsi_parsed_data["Technical Analysis: RSI"]
    price_parsed_data = price_parsed_data["Time Series (Daily)"]
    #with open(f"StockData/{stock_name}_{timeframe}.json", "r") as json_file:        
    #    data_set = json.load(json_file)    
    crossoverPoints=findRSIGoodSpots(rsi_parsed_data, "2019-11-29")
    vals = []
    csvVals = [stockName]
    with open('stockRSIData.csv', mode='a+') as stockData:
        stock_writer = csv.writer(stockData, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        for i in range(1,6):
            d = findRSIAvgPercentChange(price_parsed_data, crossoverPoints, i)
            csvVals.append(d)
            vals.append("Day "+ str(i) +": "+ str(d))
            
        stock_writer.writerow(csvVals)
    
    
    print(vals) #finds price change hourly

# getAvgChange("AMZN","SKY470CWGO52HCSQ")
# getAvgChange("MSFT","SKY470CWGO52HCSQ")
# getAvgChange("AAPL","CW3985DDZ00FVGZ5")
# getAvgChange("FB","CW3985DDZ00FVGZ5")
# getAvgChange("JPM","N29DY72L98XQRYRB")
# getAvgChange("GOOG","N29DY72L98XQRYRB")




keys = ["SKYA470CWGO52HCSQ","CW3985DDZ00FVGZ5","N29DY72L98XQRYRB"]
stocks = ["MSFT","AAPL", "AMZN", "FB","GOOG"]
# stocks = ["MSFT","AAPL", "AMZN", "FB","JPM","GOOGL","JNJ","TSLA","V","",""]
i = 0
count = 0
# for stock in stocks:
#     getAvgChange(stock, keys[i])
#     i += 1
#     if i>= len(keys):
#         i = 0
#         count +=1
#     if count>=2:
#         time.sleep(60)
#         count = 0

for stock in stocks:
    getAvgRSIChange(stock, keys[2])
    count +=1
    if count >= 2:
        time.sleep(70)
        count = 0