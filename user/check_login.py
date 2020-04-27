from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class CheckLoginMiddleware(MiddlewareMixin):
    """
    强制登录中间件
    """

    def process_request(self, request):
        if request.session.get('euser_id'):
            pass
        else:
            return redirect('user:login')