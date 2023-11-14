import requests
import zlib
from datetime import datetime, timedelta

def get_rate_today(ondate, currency_code):
    url = f"https://api.nbrb.by/exrates/rates/{currency_code}"
    params = {"ondate": ondate}

    response = requests.get(url, params=params)
    return response

date = input("Введите дату (в формате YYYY-MM-DD, или нажмите Enter для текущей даты): ")
currency_code = input("Введите код валюты (например, 456): ")

date = date if date else None

exchange_rate_today_response = get_rate_today(ondate=date, currency_code=currency_code)

if date:
    yesterday = (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
    exchange_rate_yesterday_response = get_rate_today(ondate=yesterday, currency_code=currency_code)

    if exchange_rate_today_response.ok and exchange_rate_yesterday_response.ok:
        exchange_rate_today = exchange_rate_today_response.json()
        exchange_rate_yesterday = exchange_rate_yesterday_response.json()

        rate_today = exchange_rate_today['Cur_OfficialRate']
        rate_yesterday = exchange_rate_yesterday['Cur_OfficialRate']

        currency_name = exchange_rate_today['Cur_Name']
        trend = "повысился" if rate_today > rate_yesterday else "понизился" if rate_today < rate_yesterday else "остался неизменным"
        
        print(f"Курс валюты {currency_name} с кодом {currency_code} на дату {date}: {rate_today}")
        print(f"Курс {trend} по сравнению с предыдущим днем.")

        crc32 = zlib.crc32(exchange_rate_today_response.content)
        headers = {'CRC32': str(crc32)}
        print(f"Заголовок CRC32: {headers}")
    else:
        print(f"Информация о курсе валюты с кодом {currency_code} на дату {date} или на предыдущий день не найдена.")
else:
    print("Не удалось получить информацию о предыдущем дне, так как не указана конкретная дата.")
