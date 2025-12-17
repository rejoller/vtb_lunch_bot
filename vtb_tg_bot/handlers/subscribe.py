from aiogram import Router, F
from aiogram.types import  Message
from aiogram.filters import Command


from sqlalchemy.ext.asyncio import AsyncSession


from kb.subscribe import markup

router = Router()



@router.message(Command('subscribe'), F.chat.type == "private")
async def handle_start(message: Message, session: AsyncSession):
    
    
    await message.answer("Подписаться", reply_markup=markup)