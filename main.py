import json
from random import random
import requests
import os
from bs4 import BeautifulSoup
import time
import random
import re
import csv


def get_html():
    
    # открываю ссесию
    sess = requests.Session()
    
    url = 'https://rosnou.ru/institutes/'
    
    response = sess.get(url=url)
    
    # создаю директория для сохранения
    if not os.path.exists("data"):
        os.mkdir("data")
    
    # сохраняю главную страницу
    with open("data/data.html", "w") as file:
        file.write(response.text)
        
    # читаю сохраненную страницу
    with open("data/data.html") as file:
        src = file.read()
        
    # создаю объект бьютифулсупа
    soup = BeautifulSoup(src, "lxml")
    
     # переменная для записи json
    all_json_data = []
        
    # переменная для записи в csv
    data = []
    
    # нахожу блок с институтами
    block_institutions = soup.find("div", class_="stage__wrapper stage-wrapper").find("div", class_="grid-list").find_all("div",class_="grid-item")
    
    # достаю низвания институтов и ссылки на них
    for block in block_institutions:
        
        # название института
        name_institute = block.find("div", class_="info-card__title").text.replace("\n", "")
        
        # ссылку на институт        
        link_institute = f'https://rosnou.ru{block.find("a").get("href")}'
        
        # print(f"{name_institute}: {link_institute}\n ")
        
        # пауза перед тем, как перейти по ссылке в институт
        time.sleep(random.randrange(1, 3))
        
        # прохожу во внутрь каждого института (6 шт.)
        response = sess.get(url=link_institute)
        
        # сохраняю страницу института (потом УДАЛИТЬ)
        with open(f"data/{name_institute}.html", "w") as file:
            file.write(response.text)
        
        # пауза между запросами к каждому институту
        time.sleep(random.randrange(1, 3))
        
        # читаю страницу института (потом УДАЛИТЬ)
        with open(f"data/{name_institute}.html") as file:
            src = file.read()
        
        # пока пишу код, читаю один институт, потом удалить и сдвинуть код вправо!!!!
    
    # with open(f"data/Гуманитарный институт.html") as file:
    #     src = file.read()    
       
        # создаю объект бьютифулсупа
        soup = BeautifulSoup(src, "lxml")
            
        # я цепляюсь за то, что есть у каждой карточки это номер специальность
        block_with_cards_of_one_university = soup.find_all("div", class_="article-card__type")
        
        for i in block_with_cards_of_one_university:
            
            # Наименование специальности!
            direction = i.find_next("div", class_="article-card__title").text
            
            # имя универа
            institute_dirty = i.find_next("span", class_="tag__title").text.replace("\n", "")
            # print(f"institute_dirty до применения комбинации -> ' '.join(institute_dirty.split())\n{institute_dirty}")
            institute = " ".join(institute_dirty.split()) # классно!      
            
            # print(f"institute_dirty до после применения комбинации -> ' '.join(institute_dirty.split())\n{institute}")
            
            # стоимость        
            try:
                price = i.find_next("div", class_="article-card__info-wrapper").find(string=re.compile("Стоимость в год")).parent.previous_sibling.previous_sibling.text.replace("₽", "")
            except Exception as ex:
                price = "No data!"
                
            # бюджетные места
            try:
                budget_places = i.find_next("div", class_="article-card__info-wrapper").find(string=re.compile("Бюджетных мест")).parent.previous_sibling.previous_sibling.text
            except Exception as ex:
                budget_places = "No data!"
            
            print(f"Институт: {institute} - Специальность: {direction} - Стоимость: {price} - Бюджетных мест: {budget_places} ")
            
            # упаковываю данные для записи в json
            all_json_data.append(
                {
                    "institute": institute,
                    "direction": direction,
                    "budget_places": budget_places,
                    "price": price
                }
            )
            
            # упаковываю данные для записи в csv
            data.append(
                [
                    institute,
                    direction,
                    budget_places,
                    price
                ]
            )
            
            # пауза после каждого универа, сайт тугой
            time.sleep(random.randrange(1, 3))
            
    # записываю в csv, заголовоки
    with open("data/data_institute.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "Институт",
                "Напрвление",
                "Бюджетные места",
                "Стоимость"
            )
        )
        writer.writerows(data) #записываю значения
        
    # записываю json
    with open("data/all_json_data.json", "w") as file:
        json.dump(all_json_data, file, indent=4, ensure_ascii=False)


def main():
    get_html()


if __name__ == "__main__":
    main()
