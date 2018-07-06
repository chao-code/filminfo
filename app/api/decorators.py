from functools import wraps

def cross_origin(origin='*'):
    def decorater(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            response = f(*args, **kwargs)
            response.headers.add('Access-Control-Allow-Origin', origin)
            return response
        return wrapper
    return decorater
