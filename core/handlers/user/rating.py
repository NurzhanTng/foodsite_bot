import json
import logging

from aiogram import Bot, Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.handlers.basic import get_start
from core.keyboards.inline import get_back_inline_keyboard
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.RestHandler import RestHandler
from core.utils.states import States
from core.keyboards.inline import get_rating_inline_keyboard

router = Router()


@router.message(Command(commands=['rating']))
async def test_rating(message: Message, chat_handler: ChatHistoryHandler):
    text = ("Пожалуйста, выберите смайлик, который наилучшим образом описывает ваше впечатление от заказа:\n\n😞 - Не "
            "понравилось\n😐 - Средне\n🙂 - Хорошо\n😊 - Отлично")
    await chat_handler.send_message(message, text=text, reply_markup=get_rating_inline_keyboard(1))


@router.callback_query(F.data.startswith('rating'))
async def get_my_data(callback: CallbackQuery, chat_handler: ChatHistoryHandler, rest: RestHandler, state: FSMContext):
    user_rating = callback.data.split('-')[1]
    order_id = callback.data.split('-')[2]
    await rest.update(url=f"food/orders/{order_id}/", data={"rating": user_rating})
    logging.info(f'Rest [food/orders/{order_id}/] -> {json.dumps({"rating": user_rating})}')
    await chat_handler.delete_messages(callback.message.chat.id)
    await get_start(callback.message, chat_handler, rest, state)
