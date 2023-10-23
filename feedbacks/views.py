from django.shortcuts import render

from feedbacks.forms import FeedbackForm
from core.utils import send_telegram_message


def feedback_create(request):
    form = FeedbackForm(request.POST or None)
    context = {
        'form': form,
    }
    if not form.is_valid():
        return render(request, 'feedbacks/feedback_create.html', context)
    form.save()
    send_telegram_message('Пришло новое сообщение по форме обратной связи')
    return render(request, 'feedbacks/feedback_created.html', context)
