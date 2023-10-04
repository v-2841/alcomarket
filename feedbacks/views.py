from django.shortcuts import render

from feedbacks.forms import FeedbackForm


def feedback_create(request):
    form = FeedbackForm(request.POST or None)
    context = {
        'form': form,
    }
    if not form.is_valid():
        return render(request, 'feedbacks/feedback_create.html', context)
    form.save()
    return render(request, 'feedbacks/feedback_created.html', context)
