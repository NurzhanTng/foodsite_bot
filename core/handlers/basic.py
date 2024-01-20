from aiogram import Bot, Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.keyboards.inline import get_main_inline_keyboard, get_back_inline_keyboard
from core.settings import settings
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.RestHandler import RestHandler
from core.utils.states import States

router = Router()


@router.startup()
async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text="Бот запущен!")


@router.message(Command(commands=['start', 'run']))
async def get_start(message: Message, command: CommandObject, chat_handler: ChatHistoryHandler, rest: RestHandler,
                    state: FSMContext):
    try:
        payload = {
            'chat_id': message.chat.id,
            'full_name': message.from_user.full_name,
            'token': '' if command.args is None else command.args,
        }

        # user = await rest.post(url='users', data=payload)
        user = {"bonus": 1000, 'name': message.from_user.full_name}
        await state.clear()
        await chat_handler.delete_messages(message.chat.id)
        await chat_handler.send_message(message,
                                        f"👋🏻 *Добро пожаловать в пиццерию {'' if user['name'] is None else user['name']}!*\n"
                                        f"*В данный момент у вас:* {user['bonus']} бонусов!\n" +
                                        f"_При оформление заказа, вы сможете потратить эти бонусы_\n" +
                                        f"_Чтобы сделать предзаказ, воспользуйтесь кнопками._",
                                        reply_markup=get_main_inline_keyboard())
    except Exception as e:
        print(e)


async def main_page(message: Message, chat_handler: ChatHistoryHandler, rest: RestHandler):
    try:
        # user = await rest.get(url=f'users\\{message.from_user.id}')
        user = {"bonus": 1000, 'name': message.from_user.full_name}
        await chat_handler.send_message(message,
                                        f"*В данный момент у вас:* {user['bonus']} бонусов!\n" +
                                        f"_При оформление заказа, вы сможете потратить эти бонусы_\n" +
                                        f"_Чтобы сделать предзаказ, воспользуйтесь кнопками._",
                                        reply_markup=get_main_inline_keyboard())
    except Exception as e:
        print(e)


@router.message(Command(commands=['help']))
async def help_message(message: Message, chat_handler: ChatHistoryHandler):
    await chat_handler.send_message(message, f'Chat id:{message.chat.id}\nMessage id: {message.message_id}')


@router.message(Command(commands=['delete']))
async def delete_all_messages(message: Message, chat_handler: ChatHistoryHandler):
    await chat_handler.delete_messages(message.chat.id)


@router.message(lambda message: True)
async def handle_all_messages(message: Message):
    # Заглушка для всех остальных сообщений
    ...
