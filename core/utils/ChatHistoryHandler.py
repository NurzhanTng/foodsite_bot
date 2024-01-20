from aiogram import Bot
from aiogram.types import Message


class ChatHistoryHandler:
    def __init__(self, bot:Bot) -> None:
        self.bot = bot
        self.messages = {}

    def add_new_message(self, user_id: int, message_id: int) -> None:
        if user_id in self.messages:
            self.messages[user_id].append(message_id)
        else:
            self.messages[user_id] = [message_id]

    async def delete_messages(self, chat_id: int) -> None:
        try:
            message_ids = self.messages.get(chat_id, [])
            if message_ids:
                await self.bot.delete_messages(chat_id=chat_id, message_ids=message_ids)
                self.messages[chat_id].clear()
        except Exception as e:
            print("Error when deleting messages: ", e)

    async def send_message(self, message: Message, text: str, *args, **kwargs) -> None:
        message_id = (await message.answer(text, *args, **kwargs)).message_id
        self.add_new_message(message.chat.id, message_id)
