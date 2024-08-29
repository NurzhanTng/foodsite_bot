import json
import logging

from aiogram import Bot, Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.keyboards.inline import get_mailing_inline_keyboard
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.RestHandler import RestHandler
from core.handlers.basic import get_start

router = Router()


@router.message(Command(commands=['mailing']))
async def send_mailing(message: Message, bot: Bot, chat_handler: ChatHistoryHandler, rest: RestHandler,
                       state: FSMContext):
    context = await state.get_data()
    user = context.get('user', None)
    if user is None:
        await message.answer('Пользователь не авторизован для рассылки. \nДля авторизации используйте команду /start')
        return

    if user.get('role', 'client') != 'admin':
        logging.error(f"User {user.get('telegram_id', -1)} tried to send out a mailing")
        return

    users = await rest.post('service/users_find/', data={"role": "admin"})
    await message.answer(f'Рассылка началась. Количество пользователей для рассылки: {len(users)}')
    error_users = {}
    for user in users:
        chat_id = user.get('telegram_id', -1)
        try:
            message_id = (await bot.send_photo(chat_id,
                                               "https://pizza.pizzeria-almaty.kz/media/images/margarita_low.jpg")
                          ).message_id
            chat_handler.add_new_message(chat_id, message_id)
            message_id = (await bot.send_message(chat_id,
                                                 "Здравствуйте, Ваш друг подарил вам пиццу Маргариту "
                                                 "отметив вас, на любой ваш заказ мы подарим вам "
                                                 "вкусную пиццу от вашего друга. Для заказа перейдите по "
                                                 "ссылке, где в корзине вам уже добавлена ваша пицца 👇",
                                                 reply_markup=get_mailing_inline_keyboard())).message_id
            chat_handler.add_new_message(chat_id, message_id)
        except Exception as e:
            error_users[chat_id] = {
                'error': e,
                'location': f"{e.__traceback__.tb_frame.f_code.co_filename} "
                            f"(строка {e.__traceback__.tb_lineno}, "
                            f"в функции {e.__traceback__.tb_frame.f_code.co_name})"
            }
    await message.answer(f'Рассылка закончилась. Успешно отправленные '
                         f'сообщения [{len(users) - len(error_users)}/{len(users)}]')
    logging.info(f'Рассылка: {error_users}')


@router.callback_query(F.data == "mailing_cancel")
async def go_back(callback: CallbackQuery, chat_handler: ChatHistoryHandler, rest: RestHandler, state: FSMContext,
                  command: CommandObject | None = None):
    await chat_handler.delete_messages(callback.message.chat.id)
    await get_start(callback.message, chat_handler, rest, state, command)

