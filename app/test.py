import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
from main_db import write_to_db

app_data = []


def format_date(x):
    if x[0].isnumeric():
        my_list = x.split('/')

        y = ('-').join(my_list)
        return y
    elif x[0].isalpha():
        date_N_days_ago = datetime.now() - timedelta(days=1)
        y = date_N_days_ago.strftime('%d-%m-%Y')
        return y
    else:
        my_list = x.split(' ')
        if my_list[-2] == 'hours':
            m = datetime.now()
            now_time = m.strftime("%H:%M:%S").split(':')
            if int(my_list[1]) > int(now_time[0]):
                date_N_days_ago = datetime.now() - timedelta(days=1)
                y = date_N_days_ago.strftime('%d-%m-%Y')
                return y
            else:
                y = datetime.now().strftime('%d-%m-%Y')
                return y
        else:
            m = datetime.now()
            now_time = m.strftime("%H:%M:%S").split(':')
            if int(now_time[0]) >= 1:
                y = datetime.now().strftime('%d-%m-%Y')
                return y
            else:
                if int(my_list[1]) > int(now_time[1]):
                    date_N_days_ago = datetime.now() - timedelta(days=1)
                    y = date_N_days_ago.strftime('%d-%m-%Y')
                    return y
                else:
                    y = datetime.now().strftime('%d-%m-%Y')
                    return y


def get_count_of_pages():
    r = requests.get('https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273?ad=offering')
    soup = BeautifulSoup(r.text, 'lxml')
    count_info = soup.select_one('.resultsShowingCount-1707762110').text

    my_list = count_info.split(' ')
    total_items = int(my_list[-2])

    count_of_pages = total_items // 40 + 1
    return count_of_pages


def get_data_page(page):
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'referer': 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-3/c37l1700273?ad=offering'
    }

    url = f'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{page}/c37l1700273?ad=offering'

    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')

    content = soup.select('.clearfix')

    if len(content) == 0:
        print('WORK')

    for item in content:
        try:
            url_item = item.select_one('img[data-src]').get('data-src')
        except AttributeError:
            url_item = 'https://ca.classistatic.com/static/V/11166/img/placeholder-large.png'
            continue
        try:
            date_posted = item.select_one('.date-posted').text
            export_date_posted = format_date(date_posted)
        except AttributeError:
            date_posted = 'Unknown'
            continue
        try:
            price = item.select_one('.price').text.strip().replace('\n', ' ')
        except AttributeError:
            price = 'Unknown'
            continue

        app_data.append((export_date_posted, price, url_item))

    print(f'[INFO] Обработал страницу {page}')


def main():
    for page in range(1, get_count_of_pages()):
        get_data_page(page)

    with open('new.json', "w") as f:
        json.dump(app_data, f, indent=4, ensure_ascii=False)

    print(len(app_data))
    write_to_db(app_data)


if __name__ == '__main__':
    main()
