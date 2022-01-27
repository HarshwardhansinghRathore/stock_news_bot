import requests
import smtplib
import datetime

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
email = 'hr1566027'
app_password = 'brodlyeytybyjwdx'

stock_api_k = '1K5JK09JZDGOPQO9'
news_api_k = '7da181883b7e48e18f8b6da21a881e94'

stock_parameters = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': STOCK,
            'interval': '1440min',
            'apikey': stock_api_k
}
stock_api_response = requests.get(url='https://www.alphavantage.co/query', params=stock_parameters)
stock_api_response.raise_for_status()

stock_data = stock_api_response.json()
daily_stock_data = stock_data['Time Series (Daily)']

data = [float(value['4. close'])for key, value in daily_stock_data.items()]
yesterday = data[0]
day_before_yesterday = data[1]

today = datetime.datetime.now()
pro_or_loss_percent = (day_before_yesterday-yesterday)/day_before_yesterday*100

if pro_or_loss_percent < 5 or pro_or_loss_percent > -5:
    news_parameters = {
        'apiKey': news_api_k,
        'q': COMPANY_NAME,
        'sortBy': 'popularity',
        'from': f"{today.year}-{today.month}-{today.day - 2}"
    }

    news_api_response = requests.get(url='https://newsapi.org/v2/everything', params=news_parameters)

    news_api_response.raise_for_status()
    news_data = news_api_response.json()
    if pro_or_loss_percent < 0:
        percent_change = abs(pro_or_loss_percent)
    else:
        percent_change = pro_or_loss_percent
    if news_data['totalResults'] > 0:
        first_article = news_data['articles'][0]
        news_title = first_article['title']
        news_description = first_article['description']
        if pro_or_loss_percent < 0:
            message = f'increase{round(percent_change,4)} %\ntitle:{news_title}\ndescription:{news_description}'
        else:
            message = f'decrease{round(percent_change,4)}\ntitle:{news_title}\ndescription:{news_description}'
        connection = smtplib.SMTP('smtp.gmail.com', port=587)
        connection.starttls()
        connection.login(user=email, password=app_password)
        connection.sendmail(from_addr=email, to_addrs="hrathore076@gmail.com", msg=f"Subject:Stock News\n\n{message.encode('utf-8')}")
        connection.close()
