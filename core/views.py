from django.shortcuts import render


def permission_denied(request, exception):
    context = {'path': request.path, 'status_code': 403}
    return render(request, 'core/403.html', context, status=403)


def page_not_found(request, exception):
    context = {'path': request.path, 'status_code': 404}
    return render(request, 'core/404.html', context, status=404)


def server_error(request):
    context = {'path': request.path, 'status_code': 500}
    return render(request, 'core/500.html', context, status=500)


def csrf_failure(request, reason=''):
    return render(request, 'core/403csrf.html')
