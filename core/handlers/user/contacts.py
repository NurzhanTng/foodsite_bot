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


@router.callback_query(F.data == 'contact')
async def get_my_data(callback: CallbackQuery, chat_handler: ChatHistoryHandler, state: FSMContext):
    await chat_handler.delete_messages(callback.message.chat.id)
    await state.set_state(States.CONTACTS)
    await chat_handler.send_message(callback.message,
                                    f'🍜 *Monopizza*\n'
                                    f'Наши контакты: +7 (702) 136 6697\n'
                                    f'Инстаграм: [Monopizza](https://www.instagram.com/pizza.mono/)'
                                    f'\nАдрес: [г.Алматы. Улица Курмангазы 54](https://2gis.kz/almaty/geo/70000001066330354)',
                                    reply_markup=get_back_inline_keyboard())


@router.callback_query(States.CONTACTS, F.data == 'to-back')
async def go_back(callback: CallbackQuery, chat_handler: ChatHistoryHandler, rest: RestHandler, state: FSMContext,
                  command: CommandObject | None = None):
    await chat_handler.delete_messages(callback.message.chat.id)
    await get_start(callback.message, chat_handler, rest, state, command)

#
# @router.callback_query(F.data)
# async def go_back(callback: CallbackQuery, chat_handler: ChatHistoryHandler, rest: RestHandler, state: FSMContext,
#                   command: CommandObject | None = None):
#     await chat_handler.delete_messages(callback.message.chat.id)
#     await chat_handler.send_message(callback.message,
#                                     f'Пришел колбек: {callback.data}')
