from airflow.decorators import task
from airflow import DAG
from airflow.models import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook

from openai import OpenAI
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import requests
import telebot
from pyrogram import Client
import tempfile


from datetime import datetime as dt, timedelta
import os
import logging
import pendulum




local_tz = pendulum.timezone("Europe/Moscow")
default_args = {
    "owner": "Vlad Kazakov"
}

    
        
with DAG(
    dag_id="menu_review_dag",
    start_date=dt(2025, 12, 11, tzinfo=local_tz),
    schedule="2 10 */1 * 1-5",
    catchup=False,
    default_args=default_args,
    max_active_runs=1,
    description= "Отправка меню через телеграм бота",
    max_active_tasks=1
) as dag:
    
    @task
    def import_menu_from_website():
        
        url = 'https://freshvote.ru/menu/000000035.jpg'
        SAVE_DIR = 'menu_path'  

        t = str(dt.now()).replace('-','').replace(' ','').replace(':','').replace('.','')

        filename = url.split('/')[-1]
        filename = t + '_'+ filename
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
            
        filepath = os.path.join(SAVE_DIR, filename)
        
        resp = requests.get(url, headers={
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Expires": "0"
        })
        
        print(resp.status_code)
        
        if resp.ok:
            with open(filepath, 'wb') as f:
                f.write(resp.content)
                return filepath
        else:
            return None
        
        
    @task
    def get_tesseract_recognition(filepath):
        
        pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
        response_tesseract = pytesseract.image_to_string(Image.open(filepath), lang='rus+eng', config=r'--oem 3 --psm 6')
        
        return response_tesseract
        
        
    @task
    def get_openai_text(response_tesseract):
        openai_api_key = Variable.get("openai_api_key")
        client = OpenAI(api_key=openai_api_key)
        
        
        gpt_response = client.responses.create(
<<<<<<< HEAD
            model="gpt-5",
            input=f"""ты помощник по составлению краткого меню для категории бизнес ланчей за 305 рублей (другие категории упоминать не надо) в таком стиле, вот примеры, :
=======
            model="gpt-5.2",
            input=f"""ты помощник по составлению краткого меню для категории бизнес ланчей за 305 рублей (про другие категории не говори) в таком стиле, вот примеры, :
>>>>>>> ebb1d9d (меню евразия работает, нужно добавлять федерацию)
            [1. Коллеги ну а сегодня 3 декабря среда, с чем я вас и поздравляю\n
            На гарнир у нас булгур или вареная картошка, а салаты либо с крабовыми палочками либо с пекинской капустой.
            А вот супы максимально удручают, <b>уха</b> или <b>рассольник с перловкой</b>
                
            2. Итак сегодня 2 декабря у нас на гарнир <b>гречка</b> и <b>пюре</b>. Салаты и супы тоже вполне солидные
            ]
            
                , напиши меню на основе этого распознанного изображения и указывай текущую дату в формате "ДД Месяц, День недели" (в тексте могут быть неточности так как изображение прогонялось через библиотеку tesseracrt, учитывай это и исправляй артефакты если заметишь)
                используя разметку HTML для телеграм и добавляй еще немного смайлов.  

            Используй только такие HTML теги: <b>, <i>     Не используй никакие другие теги.
                Не используй символы вроде «умных» кавычек. Используй только обычные: " и ', ты работаешь для сотрудников банка ВТБ (команда Антифрод), так как столовая находится там, а если сегодня пятница то напоминай что рабочий день до 16:45 а не до 18:00 как обычно, а у Максима и Игоря вообще до 15:45 так как они приходят на работу на час раньше чем остальные . Можешь еще упомянуть сколько осталось рабочих дней до новогодних выходных праздникров, будь всегда на позитиве и уделяй особое внимание редактированию сообщения. слог должен быть хороший и форматирвоание: {response_tesseract}"""
        )
        review_text = gpt_response.output_text
        
        return review_text
    
    
    
    
    
    @task
    def get_fed_menu():
        
        api_id = Variable.get("api_id")
        api_hash = Variable.get("api_hash")
        cafetera_chat_id = Variable.get("cafetera_chat_id")
        
        app = Client("my_account", api_id, api_hash)
        app.start()
        
        
        date = dt.date
        for message in app.get_chat_history(chat_id=cafetera_chat_id, limit=3):

            if message.document:
                for document in message.document.file_name:
                    if '7' in document:
                        date_7_file = date(message.document.date)
                        floor_7_filepath = f'menu_path/7_floor_{date_7_file}.pdf'
                        
                        message.download(floor_7_filepath)

                    
                    if '1' in document:
                        date_1_file = date(message.document.date)
                        floor_1_filepath = f'menu_path/1_floor_{date_1_file}.pdf'
                        
                        message.download(floor_1_filepath)
        
        menu_dict = {'7_floor': floor_7_filepath, '1_floor': floor_1_filepath}
        
        return menu_dict
    
    @task
    def federation_menu_recognition(menu_dict):
        
        floor_7_filepath = menu_dict['7_floor']
        floor_1_filepath = menu_dict['1_floor']
        
        if floor_7_filepath:
            floor_1_text_result = []

            with tempfile.TemporaryDirectory() as tmpdir:
                pages = convert_from_path(
                    floor_7_filepath,
                    dpi=300,              
                    fmt="png",
                    output_folder=tmpdir
                )

                for i, page in enumerate(pages):
                    img_path = os.path.join(tmpdir, f"page_{i}.png")
                    page.save(img_path, "PNG")

                    text = pytesseract.image_to_string(
                        Image.open(img_path),
                        lang="rus+eng",
                        config="--oem 3 --psm 6"
                    )
                    floor_1_text_result.append(text)

        full_7_floor_text = "\n\n".join(floor_1_text_result)
        
        
        if floor_1_filepath:
            floor_1_text_result = []
            
            with tempfile.TemporaryDirectory() as tmpdir:
                pages = convert_from_path(
                    floor_1_filepath,
                    dpi=300,              
                    fmt="png",
                    output_folder=tmpdir
                )

                for i, page in enumerate(pages):
                    img_path = os.path.join(tmpdir, f"page_{i}.png")
                    page.save(img_path, "PNG")

                    text = pytesseract.image_to_string(
                        Image.open(img_path),
                        lang="rus+eng",
                        config="--oem 3 --psm 6"
                    )
                    floor_1_text_result.append(text)

        full_1_floor_text = "\n\n".join(floor_1_text_result)

        federation_menu_dict = {'7_floor': full_7_floor_text, '1_floor': full_1_floor_text}
        
        return federation_menu_dict
            
    @task
    def get_federation_openai_text(federation_menu_dict):
        openai_api_key = Variable.get("openai_api_key")
        client = OpenAI(api_key=openai_api_key)
        
        
        gpt_response_1_floor= client.responses.create(
            model = 'gpt-5',
            input=f""" сделай краткое меню бизнес ланча за 305 рублей на основе текста:
            {federation_menu_dict['1_floor']} Используй только такие HTML теги: <b>, <i>. Не используй никакие другие теги"""),
        
        review_1_floor = gpt_response_1_floor.output_text
        
        gpt_response_7_floor= client.responses.create(
            model = 'gpt-5',
            input = f""" сделай краткое меню бизнес ланча за 305 рублей на основе текста:
            {federation_menu_dict['7_floor']} Используй только такие HTML теги: <b>, <i>. Не используй никакие другие теги """)
        
        review_7_floor = gpt_response_7_floor.output_text
        
        review_1_and_7_floor = {'1_floor': review_1_floor, '7_floor': review_7_floor}

        return review_1_and_7_floor
    
        

    
    @task
    def send_menu_review_to_telegram(review_text, review_1_and_7_floor):
        
        floor_1_text = review_1_and_7_floor['1_floor']
        floor_7_text = review_1_and_7_floor['7_floor']
        
        bot = telebot.TeleBot(token=Variable.get("BOT_TOKEN"))
        
        pg_hook = PostgresHook(postgres_conn_id="vtb_lunch_tg_bot")
        conn = pg_hook.get_conn()
        session = conn.cursor()
        
        text = f"""{review_text}\n\n меню первого этажа: <blockquote expandable>{floor_1_text}</blockquote>\n\n меню второго этажа: <blockquote expandable>{floor_7_text}</blockquote>\n\n"""
        ids_query = """select distinct user_id from subscriber"""
        session.execute(ids_query)
        ids = session.fetchall()
        chat_ids = [id[0] for id in ids]
        
        for id in chat_ids:
            try:
                bot.send_message(chat_id=id, text=text, parse_mode='HTML')
            except Exception as e:
                logging.error(f"Failed to send message to {id} {e}")
                
        
        session.close()
        conn.close()



    filepath = import_menu_from_website()
    response_tesseract = get_tesseract_recognition(filepath)
    menu_dict = get_fed_menu()
    federation_menu_dict = federation_menu_recognition(menu_dict)
    
    review_1_and_7_floor = get_federation_openai_text(federation_menu_dict)
    review_text = get_openai_text(response_tesseract)
    send_menu_review_to_telegram(review_text, review_1_and_7_floor)
    
    
    
    
