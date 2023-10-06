import json

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from goods.models import Good, UserShoppingCart


def test(request):
    a = json.loads(request.body)
    return JsonResponse(a)


def index(request):
    return render(request, 'goods/index.html', {
        'goods': Good.objects.order_by('-created_at')})


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


@login_required
def check_cart_status(request, good_id):
    if request.method == 'GET':
        good = get_object_or_404(Good, id=good_id)
        user = request.user
        is_in_cart = UserShoppingCart.objects.filter(
            user=user, good=good).exists()
        return JsonResponse({'is_in_cart': is_in_cart}, status=200)
    return JsonResponse({'error': 'Метод не разрешен'}, status=405)
