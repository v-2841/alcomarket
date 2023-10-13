from django.http import JsonResponse
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from core.utils import paginator
from goods.forms import SortForm
from goods.models import Good, UserShoppingCart, Category, Manufacturer
from goods.utils import sort_util


def index(request):
    goods = Good.objects.filter(active=True).select_related(
        'category', 'manufacturer').order_by('name')
    sort_form = SortForm(request.GET or None)
    goods = sort_util(request, goods)
    page_obj = paginator(request, goods)
    context = {
        'page_obj': page_obj,
        'sort_form': sort_form,
        'count_all': goods.count(),
    }
    if request.user.is_authenticated:
        context['shopping_cart'] = request.user.shopping_cart.all()
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


def categories(request):
    categories = Category.objects.annotate(
        num_active_goods=Count('good', filter=Q(good__active=True))).filter(
            num_active_goods__gt=0).order_by('name')
    return render(request, 'goods/categories.html', {'categories': categories})


def manufactureres(request):
    manufactureres = Manufacturer.objects.annotate(
        num_active_goods=Count('good', filter=Q(good__active=True))).filter(
            num_active_goods__gt=0).order_by('name')
    return render(request, 'goods/manufactureres.html', {
        'manufactureres': manufactureres})
