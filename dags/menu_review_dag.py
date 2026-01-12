from airflow.decorators import task
from airflow import DAG
from airflow.models import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook

from openai import OpenAI
import pytesseract
from PIL import Image
import requests
import telebot


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
    def send_menu_review_to_telegram(review_text):
        
        bot = telebot.TeleBot(token=Variable.get("BOT_TOKEN"))
        
        pg_hook = PostgresHook(postgres_conn_id="vtb_lunch_tg_bot")
        conn = pg_hook.get_conn()
        session = conn.cursor()
        
        
        ids_query = """select distinct user_id from subscriber"""
        session.execute(ids_query)
        ids = session.fetchall()
        chat_ids = [id[0] for id in ids]
        
        for id in chat_ids:
            try:
                bot.send_message(chat_id=id, text=review_text, parse_mode='HTML')
            except Exception as e:
                logging.error(f"Failed to send message to {id} {e}")
                
        
        session.close()
        conn.close()



    filepath = import_menu_from_website()
    response_tesseract = get_tesseract_recognition(filepath)
    review_text = get_openai_text(response_tesseract)
    send_menu_review_to_telegram(review_text)
    
    
    
    
