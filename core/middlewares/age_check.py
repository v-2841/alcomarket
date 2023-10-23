from django.shortcuts import redirect
from django.urls import reverse


class AgeCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (request.path != reverse('age_check')
                and not request.session.get('is_adult', False)):
            return redirect(f"{reverse('age_check')}?next={request.path}")
        return self.get_response(request)
