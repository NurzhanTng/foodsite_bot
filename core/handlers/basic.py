import json
import logging

from aiogram import Bot, Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.keyboards.inline import get_main_inline_keyboard, get_manager_inline_keyboard
from core.keyboards.reply import get_delivery_reply_keyboard
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.RestHandler import RestHandler
from core.filters.without_state_filter import WithoutStateFilter

router = Router()


@router.message(Command(commands=['start', 'run']))
async def _get_start(message: Message, command: CommandObject, chat_handler: ChatHistoryHandler, rest: RestHandler,
                     state: FSMContext):
    await message.answer('Добро пожаловать в нашего телеграм бота для заказа еды 🎉\n\n'
                         'Бот предлагает удобное меню, заказы и отслеживание статуса. \n'
                         'Получайте уведомления об акциях и бонусах в боте!')
    await get_start(message, chat_handler, rest, state, command)


# @router.message(Command(commands=['test']))
# async def test(message: Message):
#     logging.info(f"User_id: {message.chat.id}.")
#     logging.info(f"User_id: {message.model_dump_json(indent=2)}.")


async def get_start(message: Message, chat_handler: ChatHistoryHandler, rest: RestHandler,
                    state: FSMContext, command: CommandObject | None = None, delete_previous_messages: bool = True) \
        -> None:
    try:
        promo = ""
        if command is not None:
            promo = command.args

        payload = {
            'telegram_id': str(message.chat.id),
            'telegram_fullname': message.from_user.full_name,
            'promo': promo
        }
        logging.info(f"payload [auth/register/]: {json.dumps(payload)}")
        user = await rest.post(url=f'auth/register/', data=payload)
        if type(user) == type([]):
            payload = {
                'telegram_id': str(message.chat.id),
                'telegram_fullname': f"-telegram- {message.from_user.full_name}",
                'promo': ''
            }
            user = await rest.post(url=f'auth/register/', data=payload)

        await state.update_data(user=user)
        if user["role"] == "admin":
            await chat_handler.send_message(message,
                                            f"*🏠 Вы находитесь на главной странице админа компании*\n"
                                            f"_Чтобы увидеть заказы, воспользуйтесь кнопками_",
                                            reply_markup=get_manager_inline_keyboard())

        if user["role"] == "manager":
            await chat_handler.send_message(message,
                                            f"*🏠 Вы находитесь на главной странице менеджера*\n"
                                            f"_Чтобы увидеть заказы, воспользуйтесь кнопками_",
                                            reply_markup=get_manager_inline_keyboard())

        if user["role"] == "cook":
            await chat_handler.send_message(message,
                                            f"*🏠 Вы находитесь на главной странице повара*\n"
                                            f"_Чтобы увидеть заказы, воспользуйтесь кнопками_",
                                            reply_markup=get_manager_inline_keyboard())

        if user["role"] == "runner":
            await chat_handler.send_message(message,
                                            f"*🏠 Вы находитесь на главной странице с раздачей готовых заказов*\n"
                                            f"_Чтобы увидеть заказы, воспользуйтесь кнопками_",
                                            reply_markup=get_manager_inline_keyboard())

        if user["role"] == "client":
            await chat_handler.send_message(message,
                                            f"*Вы находитесь на главной странице* "
                                            f"{'' if user['telegram_fullname'] is None else user['telegram_fullname']}"
                                            f"!\n*В данный момент у вас:* {user['bonus']} бонусов!\n" +
                                            f"_При оформление заказа, вы сможете потратить эти бонусы_\n" +
                                            f"_Чтобы сделать предзаказ, воспользуйтесь кнопками._",
                                            reply_markup=get_main_inline_keyboard())

        if user["role"] == "delivery":
            await chat_handler.send_message(message,
                                            "*🏠 Вы находитесь на главной странице доставщика*\n"
                                            f"_Чтобы увидеть заказы, воспользуйтесь кнопками_",
                                            reply_markup=get_delivery_reply_keyboard())
    except Exception as e:
        print(e)


@router.message(lambda message: not message.web_app_data)
async def handle_all_messages(message: Message, bot: Bot):
    await bot.delete_message(message.chat.id, message.message_id)
    ...
