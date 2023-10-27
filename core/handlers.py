from logging import Handler

from core.utils import send_telegram_message


class TelegramBotHandler(Handler):
    def emit(self, record):
        send_telegram_message(self.format(record))
