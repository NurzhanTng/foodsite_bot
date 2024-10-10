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
    try:
        await message.answer('Добро пожаловать в нашего телеграм бота для заказа еды 🎉\n\n'
                             'Бот предлагает удобное меню, заказы и отслеживание статуса. \n'
                             'Получайте уведомления об акциях и бонусах в боте!')
        await get_start(message, chat_handler, rest, state, command)
    except Exception as e:
        logging.error(f"_get_start error: {e}")


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

        logging.info(f"1")

        if promo.startswith("---"):
            try:
                order_id = int(promo.replace("-", ""))
                await rest.update(url=f'food/orders/{order_id}/', data={ "client_id": str(message.chat.id) })
            except ValueError as e:
                logging.error(f"Terminal assign error: {e}")
            promo = ""

        logging.info(f"2")

        payload = {
            'telegram_id': str(message.chat.id),
            'telegram_fullname': message.from_user.full_name,
            'promo': promo
        }

        logging.info(f"3")

        logging.info(f"payload [auth/register/]: {json.dumps(payload)}")

        logging.info(f"4")

        user = await rest.post(url=f'auth/register/', data=payload)
        logging.info(f"5")
        if type(user) == type([]):
            payload = {
                'telegram_id': str(message.chat.id),
                'telegram_fullname': f"-telegram- {message.from_user.full_name}",
                'promo': ''
            }
            user = await rest.post(url=f'auth/register/', data=payload)

        logging.info(f"6")
        await state.update_data(user=user)
        logging.info(f"7")
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
        logging.info(f"8")
    except Exception as e:
        print(f"Main function error: {e}")


@router.message(lambda message: not message.web_app_data)
async def handle_all_messages(message: Message, bot: Bot):
    await bot.delete_message(message.chat.id, message.message_id)
    ...
