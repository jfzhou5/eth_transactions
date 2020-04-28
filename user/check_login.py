from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class CheckLoginMiddleware(MiddlewareMixin):
    """
    强制登录中间件
    """

    def process_request(self, request):
        print(f'request.path_info is    {request.path_info}')
        if request.path_info == '/user/login/' or request.path_info == '/user/login_form/':
            pass
        else:
            if request.session.get('address'):
                print(f"address is {request.session.get('address')}")
                pass
            else:
                return redirect('user:login')
