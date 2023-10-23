import os

import requests
from django.conf import settings
from django.core.paginator import Paginator
from dotenv import load_dotenv


load_dotenv()


def paginator(request, obj):
    paginator = Paginator(obj, settings.PAGINATOR_VIEW_NUM)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def send_telegram_message(text):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_ids = [i.strip() for i in os.getenv('CHAT_IDS').split(',')]
    link = 'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}'
    for chat_id in chat_ids:
        requests.get(link.format(token=token, chat_id=chat_id, text=text))
