import os

import django
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

os.environ['DJANGO_SETTINGS_MODULE'] = 'alcomarket.settings'
django.setup()

from feedbacks.models import Feedback
from goods.models import Good
from orders.models import Order


load_dotenv()


def start(update, context):
    chat = update.effective_chat
    buttons = [['🛒 Товары'], ['Новые заказы и сообщения']]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Добрый день!',
        reply_markup=reply_markup,
    )


def goods(update, context):
    chat = update.effective_chat
    goods = Good.objects.filter(active=True)
    goods_info = [
        f'{good.name} - {good.price} ₽ - {good.stock} шт.' for good in goods]
    goods_list = "\n".join(goods_info)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Список всех товаров:\n{goods_list}'
    )


def new_goods_feedbacks(update, context):
    chat = update.effective_chat
    new_feedbacks = Feedback.objects.filter(is_processed=False).count()
    new_orders = Order.objects.filter(status='1_PENDING').count()
    context.bot.send_message(
        chat_id=chat.id,
        text=(f'Новых сообщений: {new_feedbacks}\n'
              + f'Новых заказов: {new_orders}')
    )


def handle_text(update, context):
    text = update.message.text
    if text == '🛒 Товары':
        return goods(update, context)
    elif text == 'Новые заказы и сообщения':
        return new_goods_feedbacks(update, context)


if __name__ == '__main__':
    updater = Updater(os.getenv('TELEGRAM_TOKEN'), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(
        Filters.text & ~Filters.command, handle_text))
    updater.start_polling()
    updater.idle()
