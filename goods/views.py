import json

from django.http import JsonResponse
from django.shortcuts import render

from goods.models import Good


def test(request):
    a = json.loads(request.body)
    return JsonResponse(a)


def index(request):
    return render(request, 'goods/index.html', {'goods': Good.objects.all()})
