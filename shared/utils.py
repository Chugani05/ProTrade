import json

from django.http import JsonResponse


def required_get_method(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.method != 'GET':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return func(*args, **kwargs)
    return wrapper


def required_post_method(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.method != 'POST':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return func(*args, **kwargs)
    return wrapper


# def check_json_body(func):
#     def wrapper(*args, **kwargs):
#         request = args[0]
#         try:
#             json.loads(request.body)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON body'}, status=400)
#         return func(*args, **kwargs)
#     return wrapper


# def get_json_fields(*fields: str):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             request = args[0]
#             json_body = json.loads(request.body)
#             for field in fields:
#                 if field not in json_body.keys():
#                     return JsonResponse({'error': 'Missing required fields'}, status=400)
#             return func(*args, **kwargs)
#         return wrapper
#     return decorator


def get_valid_json(*fields: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            request = args[0]
            try:
                request.data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON body'}, status=400)
            body_fields = request.data.keys()
            for field in fields:
                if field not in body_fields:
                    return JsonResponse({'error': 'Missing required fields'}, status=400)
            return func(*args, **kwargs)

        return wrapper

    return decorator