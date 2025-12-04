from aiogram import Router, F
from aiogram.types import  Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext


router = Router()


@router.message(CommandStart(), F.chat.type == "private")
async def handle_start(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать!")
    
    

    
    
    

    
    
