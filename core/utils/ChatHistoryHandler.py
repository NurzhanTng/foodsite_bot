import logging

from aiogram import Bot
from aiogram.types import Message


class ChatHistoryHandler:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.messages = {}

    def add_new_message(self, chat_id: int | str, message_id: int) -> None:
        chat_id = chat_id
        if chat_id in self.messages:
            self.messages[str(chat_id)].append(message_id)
        else:
            self.messages[str(chat_id)] = [message_id]

    async def delete_messages(self, chat_id: int | str, separator: str | None = None) -> None:
        logging.info(f'delete_messages: {chat_id}, {separator}, {self.messages.get(chat_id, [])}')
        if separator is None:
            telegram_chat_id = int(chat_id)
        else:
            telegram_chat_id = int(chat_id.split(separator)[0])

        message_ids = self.messages.get(str(chat_id), [])
        for message_id in message_ids:
            try:
                await self.bot.delete_message(chat_id=telegram_chat_id, message_id=message_id)
            except Exception as e:
                logging.error(f"Error when deleting messages: {e}")
        self.messages[str(chat_id)].clear()

    async def send_message(self, message: Message, text: str, *args, **kwargs) -> None:
        message_id = (await message.answer(text, *args, **kwargs)).message_id
        self.add_new_message(message.chat.id, message_id)
