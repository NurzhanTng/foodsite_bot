from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.handlers.basic import get_start
from core.keyboards.reply import get_back_reply_keyboard
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.RestHandler import RestHandler
from core.utils.states import States

router = Router()


@router.message(lambda m: m.text == '📞 Контакты')
async def get_my_data(message: Message, chat_handler: ChatHistoryHandler, state: FSMContext):
    await chat_handler.delete_messages(message.chat.id)
    await chat_handler.send_message(message,
                                    f'*🍕 Pizzeria*\n'
                                    f'Наши контакты: +77715518120\n'
                                    f'Инстаграм: [pizzeria_ala](https://instagram.com/pizzeria_ala)\n'
                                    f'Адрес: Алматы, улица Курмангазы, 54',
                                    reply_markup=get_back_reply_keyboard())
    await state.set_state(States.CONTACTS)


@router.message(States.CONTACTS, lambda m: m.text == '🔙 На главную')
async def go_back(message: Message, chat_handler: ChatHistoryHandler, rest: RestHandler, state: FSMContext):
    await state.set_state(None)
    await chat_handler.delete_messages(message.chat.id)
    await get_start(message, chat_handler, rest, state)
