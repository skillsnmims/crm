"""Not in use now, Kept for later use"""


from django.utils import timezone
from .models import User


class UpdateLastActivityMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user'), "Middleware not installed properly."
        if request.user.is_authenticated:
            User.objects.filter(id=request.user.id).update(last_activity=timezone.now())
