import functools
import traceback

from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.views import View

JSON_DUMPS_PARAMS = {
    'ensure_ascii': False
}


def ret(json_object, status=200):
    """
    Отдаёт JSON c правильным HTTP заголовками и в читаемом в
    браузере виде в случае с кириллицей.
    """
    return JsonResponse(
        json_object,
        status=status,
        safe=not isinstance(json_object, list),
        json_dumps_params=JSON_DUMPS_PARAMS
    )


def error_response(exception):
    """Форматирует HTTP ответ с описанием ошибки и Traceback'ом"""
    if settings.DEBUG:
        res = {
            "message": str(exception),
            # здесь мы должны проверить, чтобы debug был true и тогда возвращаем (traceback)
            # т.к. это не безопастно (traceback -> это показывает на какой строчке кода ошибка и т.д.)
            "traceback": traceback.format_exc()
        }
    else:
        res = {
            "errorMessage": str(exception),
        }
    return ret(res, status=400)


def base_view(fn):
    """Декоратор для всех views, обрабатывает исключения"""

    @functools.wraps(fn)
    def inner(request, *args, **kwargs):
        try:
            with transaction.atomic():
                return fn(request, *args, **kwargs)
        except Exception as e:
            return error_response(e)

    return inner


class BaseView(View):
    """Базовый класс для всех views, обрабатывает исключения"""

    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            return self._response({'errorMessage': e.message}, status=400)

        if isinstance(response, (dict, list)):
            return self._response(response)
        else:
            return response

    @staticmethod
    def _response(data, *, status=200):
        return JsonResponse(
            data,
            status=status,
            safe=not isinstance(data, list),
            json_dumps_params=JSON_DUMPS_PARAMS
        )
