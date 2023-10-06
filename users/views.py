from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm, ProfileForm


User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    if user != request.user:
        return redirect('goods:index')
    form = ProfileForm(
        request.POST or None,
        instance=user,
    )
    context = {
        'form': form,
        'user_data': user,
    }
    if not form.is_valid():
        return render(request, 'users/profile.html', context)
    form.save()
    messages.success(request, 'Данные профиля успешно изменены')
    return render(request, 'users/profile.html', context)
