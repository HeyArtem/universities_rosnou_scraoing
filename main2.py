# pip install requests, bs4, lxml
from bs4 import BeautifulSoup
import requests
import csv


def collect_data():
    sess = requests.Session()
    
    response = sess.get('https://rosnou.ru/institutes/')
        
    soup = BeautifulSoup(response.text, 'lxml')
    
    # информация с каждой карточки университета
    institutes_urls = soup.find_all('a', class_='info-card')
    # print(f"institutes_urls:{institutes_urls}\n")
    
    # сохраняю сюда готовые ссылки на каждый универ
    links_list = []
    
    # буду сохранять Наименование института, Наименование направления, Количество бюджетных мест, стоимость годового обучения
    data = []
    
    for url in institutes_urls:
        
        # получил полуссылки 
        link = url.get('href')
        
        # скомпилировал готовую ссылку
        links_list.append(f'https://rosnou.ru{link}')

        # ссылка для реквестов
        link = f'https://rosnou.ru{link}'
        
        # запрос к каждому универу
        response = sess.get(link)
        soup = BeautifulSoup(response.text, 'lxml') 
        
        # карточка направления
        inst_cards = soup.find_all('div', 'article-card_specialty')
        
        
        for item in inst_cards:
            
            # наименование направления
            card_title = item.find('div', 'article-card__title').text.strip()
            
            # наименование института
            card_institute = item.find('span', 'tags-list__item').find('span').get('data-title').strip()
            
            # блок со стоимостью
            card_info_div = item.find_all('div', 'article-card__info')
            
            # если блоков "card_info_div" >0 & <2 (т.е. он один)-> бюджетных мест нет
            if len(card_info_div) > 0 and len(card_info_div) < 2:
                places_amount = 0
                
                # стоимость годового обучения
                year_price = card_info_div[0].find('div', 'article-card-annotation__title').text.strip()
                
            # если блоков "card_info_div" >0 & их 2 шт.-> так только в карточках, где есть бюджетные места
            elif len(card_info_div) > 0 and len(card_info_div) == 2:
                
                # то из первого блока беру кол-во бюджетных мест
                places_amount = card_info_div[0].find('div', 'article-card-annotation__title').text.strip()
                
                # во втором блоке беру стоимость годового обучения
                year_price = card_info_div[1].find('div', 'article-card-annotation__title').text.strip()
            
            # иначе бюджетных мест и стоимости обучения нет
            else:
                places_amount = 0
                year_price = 0
               
            # сохраняю в переменную Наименование института, Наименование направления, Количество бюджетных мест, стоимость годового обучения
            data.append(
               [card_institute, card_title, places_amount, year_price]
            )
            
        print(f'{link} is done!')
    
    # записываю данные в csv
    with open("data/data_2_institute.csv", "w") as file:
        writer = csv.writer(file)
        
        writer.writerow(
            [
                "Институт",
                "Напрвление",
                "Бюджетные места",
                "Стоимость"
            ]
        )
        writer.writerows(  #записываю значения
            data
            ) 
    
    # # для фоловеров Билла
    # with open('result_utf8sig.csv', 'w', encoding="utf-8-sig") as file:
    #     writer = csv.writer(file, delimiter=";") 
        
    #     writer.writerow(
    #         [
    #             'Институт',
    #             'Специальность',
    #             'Количество бюджетных мест',
    #             'Стоимость в год'
    #         ]
    #     )
        
    #     writer.writerows(
    #         data
    #     )
        
    
def main():
    collect_data()
    
    
if __name__ == '__main__':
    main()
