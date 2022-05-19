from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect

"""To be changed according to new crm"""


class CheckUserType(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user'), "Middleware not installed properly."
        if request.user.is_authenticated:
            request_path = request.path
            if request.user.is_visitor:
                visitor_allowed_paths = [reverse_lazy("prospects:list"),
                                         reverse_lazy("prospects:create"),
                                         reverse_lazy("prospects:detail", kwargs={"id": 1})[:-2],
                                         reverse_lazy("prospects:format_file_download"),
                                         reverse_lazy("accounts:logout"),
                                         ]
                if request_path not in visitor_allowed_paths:
                    if request_path[:request_path.rfind("/", 0, -1) + 1] != reverse_lazy("prospects:detail", kwargs={"id": 1})[:-2]:
                        return redirect("prospects:list")
            elif request_path.split("/")[1] != "accounts" and request.user.is_agent and request_path.split("/")[1] != "call":
                return redirect("portal:calling_page")
            # if request.user.is_staff and not is_admin_url:
            #     return redirect("/admin/")
