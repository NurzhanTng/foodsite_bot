from aiogram import Bot, Router, F
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.handlers.basic import get_start
from core.keyboards.inline import get_back_inline_keyboard
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.RestHandler import RestHandler
from core.utils.states import States

router = Router()


@router.message(F.text == '👤 Мои данные')
async def get_my_data(message: Message, chat_handler: ChatHistoryHandler, state: FSMContext):
    context = await state.get_data()
    user = context.get('user')

    await chat_handler.delete_messages(message.chat.id)
    await chat_handler.send_message(message, f'👤 *Мои данные:*\n\n'
                                                      f'ID: {user["telegram_id"]}\n'
                                                      f'Имя: {user["telegram_fullname"]}\n'
                                                      f'Кол-во бонусов: {user["bonus"]}\n\n'
                                                      f'Дата регистраций: {user["created_at"].split("T")[0]}',
                                    reply_markup=get_back_inline_keyboard())
    await state.set_state(States.MY_DATA)


@router.callback_query(States.MY_DATA, F.data == 'to-back')
async def go_back(callback: CallbackQuery, chat_handler: ChatHistoryHandler, rest: RestHandler, state: FSMContext,
                  command: CommandObject | None = None):
    await chat_handler.delete_messages(callback.message.chat.id)
    await get_start(callback.message, chat_handler, rest, state, command)
