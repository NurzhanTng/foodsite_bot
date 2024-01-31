from aiogram import Bot, Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.keyboards.reply import get_main_reply_keyboard
from core.utils.ChatHistoryHandler import ChatHistoryHandler
from core.utils.RestHandler import RestHandler
from core.filters.without_state_filter import WithoutStateFilter

router = Router()


# @router.startup()
# async def start_bot(bot: Bot):
#     await bot.send_message(settings.bots.admin_id, text="Бот запущен!")


@router.message(Command(commands=['start', 'run']))
async def _get_start(message: Message, command: CommandObject, chat_handler: ChatHistoryHandler, rest: RestHandler,
                     state: FSMContext):
    await message.answer('Верхний текст для показа пользователям. Он нужен, чтобы в некоторых телефонах не вылетало')
    await get_start(message, chat_handler, rest, state, command)


async def get_start(message: Message, chat_handler: ChatHistoryHandler, rest: RestHandler,
                    state: FSMContext, command: CommandObject | None = None) -> None:
    try:
        if command is None:
            payload = {
                'chat_id': message.chat.id,
                'full_name': message.from_user.full_name,
                'token': '',
            }
        else:
            payload = {
                'chat_id': message.chat.id,
                'full_name': message.from_user.full_name,
                'token': '' if command.args is None else command.args,
            }

        # user = await rest.post(url='users', data=payload)
        user = {
            "telegram_id": message.from_user.id,
            "telegram_fullname": message.from_user.full_name,
            "phone": '+77074862447',
            "address": {"loc": 76.945621, "lat": 43.242977},
            "exact_address": 'Квартира 42',
            "bonus": 1000,
            "role": "user",
            "blocked": False,
            "updated_at": '2023-01-13',
            "created_at": '2023-01-13'
        }
        await state.update_data(user=user)
        context = await state.get_data()
        order = context.get("order")
        await chat_handler.delete_messages(message.chat.id)
        await chat_handler.send_message(message,
                                        f"👋🏻 *Добро пожаловать в пиццерию "
                                        f"{'' if user['telegram_fullname'] is None else user['telegram_fullname']}!*\n"
                                        f"*В данный момент у вас:* {user['bonus']} бонусов!\n" +
                                        f"_При оформление заказа, вы сможете потратить эти бонусы_\n" +
                                        f"_Чтобы сделать предзаказ, воспользуйтесь кнопками._",
                                        reply_markup=get_main_reply_keyboard(order))
    except Exception as e:
        print(e)


@router.message(WithoutStateFilter(), lambda message: not message.web_app_data)
async def handle_all_messages(message: Message):
    print('Заглушка')
    ...
