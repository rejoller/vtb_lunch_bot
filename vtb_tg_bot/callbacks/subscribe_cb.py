from aiogram import Router, F
from aiogram.types import  CallbackQuery


from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.dialects.postgresql import insert
from database.models import Subscriber

from datetime import datetime as dt



router = Router()




@router.callback_query(F.data.startswith("subscr"))
async def subscribe(call: CallbackQuery, session: AsyncSession):

    user_id = str(call.from_user.id)

    query = insert(Subscriber).values(user_id=user_id, date = dt.now())
    await session.execute(query)
    await session.commit()
    await call.answer("Вы подписались на рассылку", show_alert=True)