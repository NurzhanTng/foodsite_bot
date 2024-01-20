from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.handlers.basic import main_page
from core.keyboards.inline import get_back_inline_keyboard
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.RestHandler import RestHandler
from core.utils.states import States

router = Router()


@router.callback_query(lambda m: m.data == 'contact')
async def get_my_data(call: CallbackQuery, chat_handler: ChatHistoryHandler, state: FSMContext, rest: RestHandler):
    await chat_handler.delete_messages(call.message.chat.id)
    # user = await rest.get(url=f'user\\{message.from_user.id}')
    user = {
        "id": call.message.from_user.id,
        "bonus": 1000,
        'name': call.message.from_user.full_name,
        'date': '2023-01-13'
    }
    await chat_handler.send_message(call.message,
                                    f'*🍕 Pizzeria*\n'
                                    f'Наши контакты: +77715518120\n'
                                    f'Инстаграм: [pizzeria_ala](https://instagram.com/pizzeria_ala)\n'
                                    f'Адрес: Алматы, улица Курмангазы, 54',
                                    reply_markup=get_back_inline_keyboard())
    await call.answer()
    await state.set_state(States.MY_DATA)


@router.callback_query(States.MY_DATA, lambda m: m.data == 'to-back')
async def go_back(call: CallbackQuery, chat_handler: ChatHistoryHandler, rest: RestHandler):
    await chat_handler.delete_messages(call.message.chat.id)
    await main_page(call.message, chat_handler, rest)
