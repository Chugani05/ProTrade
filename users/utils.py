import re

from django.http import JsonResponse

from .models import Token


def auth_required(func):
    BEARER_TOKEN_REGEX = (
        r'Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})'
    )

    def wrapper(request, *args, **kwargs):
        if not (m := re.fullmatch(BEARER_TOKEN_REGEX, request.headers.get('Authorization', ''))):
            return JsonResponse({'error': 'Invalid authentication token'}, status=400)
        try:
            token = Token.objects.get(key=m['token'])
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Unregistered authentication token'}, status=401)
        request.user = token.user
        return func(request, *args, **kwargs)

    return wrapper