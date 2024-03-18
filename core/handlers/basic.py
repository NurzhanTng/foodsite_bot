from aiogram import Bot, Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.keyboards.inline import get_main_inline_keyboard, get_manager_inline_keyboard
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
    # await message.answer('Верхний текст для показа пользователям. Он нужен, чтобы в некоторых телефонах не вылетало')
    await get_start(message, chat_handler, rest, state, command)


async def get_start(message: Message, chat_handler: ChatHistoryHandler, rest: RestHandler,
                    state: FSMContext, command: CommandObject | None = None, delete_previous_messages: bool = True) \
        -> None:
    try:
        promo = ""
        if command is not None:
            promo = command.args

        payload = {
            'telegram_id': message.chat.id,
            'telegram_fullname': message.from_user.full_name,
            'promo': promo
        }

        context = await state.get_data()
        user = context.get("user")
        if user is None:
            user = await rest.post(url=f'/auth/register/', data=payload)
            await state.update_data(user=user)
            
        if user["role"] == "manager":
            await chat_handler.send_message(message,
                                            f"👋🏻 *Добро пожаловать на главную страницу менеджера*"
                                            f"_Чтобы увидеть заказы, воспользуйтесь кнопками_",
                                            reply_markup=get_manager_inline_keyboard())

        if user["role"] == "client":
            await chat_handler.send_message(message,
                                            f"👋🏻 *Добро пожаловать в пиццерию "
                                            f"{'' if user['telegram_fullname'] is None else user['telegram_fullname']}"
                                            f"!*\n*В данный момент у вас:* {user['bonus']} бонусов!\n" +
                                            f"_При оформление заказа, вы сможете потратить эти бонусы_\n" +
                                            f"_Чтобы сделать предзаказ, воспользуйтесь кнопками._",
                                            reply_markup=get_main_inline_keyboard())
    except Exception as e:
        print(e)


@router.message(WithoutStateFilter(), lambda message: not message.web_app_data)
async def handle_all_messages(message: Message):
    print('Заглушка')
    ...
