from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from orders.models import OrderGood
from users.forms import CreationForm, ProfileForm


User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('goods:index')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        # form.instance.is_active = False
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    if user != request.user:
        return redirect('goods:index')
    context = {
        'orders': user.orders.order_by('-created_at').prefetch_related(
            Prefetch('ordergood_set',
                     queryset=OrderGood.objects.select_related('good'))),
    }
    return render(request, 'users/profile.html', context)


@login_required
def profile_edit(request, username):
    user = get_object_or_404(User, username=username)
    if user != request.user:
        return redirect('goods:index')
    form = ProfileForm(
        request.POST or None,
        instance=user,
    )
    context = {
        'form': form,
    }
    if not form.is_valid():
        return render(request, 'users/profile_edit.html', context)
    form.save()
    messages.success(request, 'Данные профиля успешно изменены')
    return render(request, 'users/profile_edit.html', context)


def age_check(request):
    if request.method == 'POST':
        request.session['is_adult'] = True
        return redirect(request.GET.get('next', '/'))
    return render(request, 'users/age_check.html')
