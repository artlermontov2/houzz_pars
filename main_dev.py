import requests
from bs4 import BeautifulSoup
import random
from time import sleep

def get_lst_link():
    """
    Получаем список ссылок на страницы дизайнеров\студий
    """
    page = 15

    lst_link = []
    # 1572
    while page <= 4500:
        url = f'https://www.houzz.ru/professionals/dizayn-interyera/c/Москва--регион-Москва/p/{page}'
        res = requests.get(url)
        soup = BeautifulSoup(res.text,'lxml')

        class_list = soup.find(
            'div', class_='pro-results'
        ).find(
            'ul', class_='hz-pro-search-results mb0'
        ).find_all(
            'li', class_='hz-pro-search-results__item'
        )

        for i in class_list:
            link = i.find('a').get('href')
            lst_link.append(link)
        page += 15

        dalay = random.randint(0, 2)
        sleep(dalay)

    return lst_link


def get_contact(lst_link):
    """
    Парсим имя и номер телефона проходясь по списку ссылок на профиль
    """
    contact = {}
    for url in lst_link:
        res = requests.get(url)
        soup = BeautifulSoup(res.text,'lxml')
        try:
            info = soup.find(
                'div', class_='sc-183mtny-0 sc-1wm9uar-0 kVLgJv ljhVzJ hui-grid'
            ).find(
                'section', id='business'
            ).find_all(
                'p', class_='sc-mwxddt-0 cZJFpr'
            )
            contact[info[0].text] = info[1].text
        except AttributeError:
            pass
        
        dalay = random.randint(0, 2)
        sleep(dalay)
    
    with open('houzz.txt','a+') as file:
        for k,v in contact.items():
            file.write(f'{k}:{v}\n')


print(get_contact(get_lst_link()))

# print(get_lst_link())