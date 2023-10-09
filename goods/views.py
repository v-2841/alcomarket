from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from core.utils import paginator
from goods.models import Good, UserShoppingCart


def index(request):
    page_obj = paginator(request, Good.objects.filter(
        active=True).order_by('-created_at').select_related(
            'category', 'manufacturer').prefetch_related(
                'is_in_shopping_cart'))
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'goods/index.html', context)


@login_required
def add_to_cart(request, good_id):
    if request.method == 'POST':
        good = get_object_or_404(Good, id=good_id)
        user = request.user
        if not UserShoppingCart.objects.filter(user=user, good=good).exists():
            UserShoppingCart.objects.create(user=user, good=good)
            return JsonResponse({'message': 'Товар добавлен в корзину'},
                                status=200)
        else:
            return JsonResponse({'message': 'Товар уже в корзине'}, status=200)
    return JsonResponse({'error': 'Метод не разрешен'}, status=405)


@login_required
def remove_from_cart(request, good_id):
    if request.method == 'POST':
        good = get_object_or_404(Good, id=good_id)
        user = request.user
        if UserShoppingCart.objects.filter(user=user, good=good).exists():
            UserShoppingCart.objects.filter(user=user, good=good).delete()
            return JsonResponse({'message': 'Товар удален из корзины'},
                                status=200)
        else:
            return JsonResponse({'message': 'Товар не найден в корзине'},
                                status=200)
    return JsonResponse({'error': 'Метод не разрешен'}, status=405)
