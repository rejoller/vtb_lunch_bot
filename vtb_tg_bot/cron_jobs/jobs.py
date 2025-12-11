import os
import requests
import pytesseract
from PIL import Image
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Menu_review
#s
from datetime import datetime as dt
import logging
from bot import bot






async def get_menu(session: AsyncSession):
    
    url = 'https://freshvote.ru/menu/000000035.jpg'

    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

    save_dir = 'menu_path'  

    t = str(dt.now()).replace('-','').replace(' ','').replace(':','').replace('.','')

    filename = url.split('/')[-1]
    filename = t + '_'+ filename

    filepath = os.path.join(save_dir, filename)

    
    with open(filepath, 'wb') as f:
        openai_api_key = os.getenv('openai_api_key')

        

        resp = requests.get(url, headers={
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Expires": "0"
        })
        
        def teseract_recognition(path_img):
            return pytesseract.image_to_string(Image.open(path_img), lang='rus+eng', config=r'--oem 3 --psm 6') 
        f.write(resp.content)
        
        response_tesseract = teseract_recognition(filepath)
        
        from openai import OpenAI
        client = OpenAI(api_key=openai_api_key)

        gpt_response = client.responses.create(
            model="gpt-5",
            input=f"""ты помощник по составлению краткого меню для категории бизнес ланчей за 305 рублей (про другие категории не говори) в таком стиле, вот примеры, :
            [1. Коллеги ну а сегодня 3 декабря среда, с чем я вас и поздравляю\n
            На гарнир у нас булгур или вареная картошка, а салаты либо с крабовыми палочками либо с пекинской капустой.
            А вот супы максимально удручают, <b>уха</b> или <b>рассольник с перловкой</b>
                
            2. Итак сегодня 2 декабря у нас на гарнир <b>гречка</b> и <b>пюре</b>. Салаты и супы тоже вполне солидные
            ]
            
                , напиши меню на основе этого распозннаного изображения и возьми дату от туда (могут быть неточности так как изображение прогонялось через библиотеку tesseracrt)
                используя разметку HTML для телеграм и добавляй еще немного смайлов. 

            Используй только такие HTML теги: <b>, <i>     Не используй никакие другие теги.
                Не используй символы вроде «умных» кавычек. Используй только обычные: " и ', ты работаешь для сотрудников банка ВТБ, так как столовая там : {response_tesseract}"""
        )
        review_text = gpt_response.output_text
        if review_text:
            query = insert(Menu_review).values(dttm=dt.now(), review_text=str(review_text))
            #-4897200857

            await bot.send_message(chat_id = '964635576', text = review_text, parse_mode = 'HTML') 
            await session.execute(query)
            await session.commit()
        else:
            logging.info('Не удалось получить меню')
