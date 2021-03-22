import logging
import traceback
from functools import wraps

from flask import request

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(filename="kiot.log", filemode="a",
                    format="%(asctime)s - %(message)s",
                    level=logging.DEBUG)


def get_log(func, api, msg='', trace=''):
    """
    Get method and IP of an api call.

    Arguments:
    func: function
        the function need to be logged
    api: string
        the endpoint name that the function process
    msg: string
        the error message (default '')
    trace: string
        the trace of the error code (default '')

    Return: dictionary
        contains ip, method, api_name, trace ans message
    """

    k = func.__name__
    method = k

    if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
        ip = request.environ["REMOTE_ADDR"]
    else:
        ip = request.environ["HTTP_X_FORWARDED_FOR"]

    return {
        "ip": ip,
        "method": method,
        "api_name": api,
        "trace": trace,
        "message": msg
    }


def log_and_capture(endpoint, code=400):
    """
    A decorator used with any api calls for logging into a file

    Arguments:
    endpoint: string
        the name of the logged endpoint
    code: int
        code for return when meet error
    """

    def inner(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            try:
                # If everything alright, we do not need traceback
                result = f(*args, **kwargs)
                log_obj = get_log(f, endpoint)
            except Exception as e:
                # If there is an error, we need its msg and traceback
                msg = str(e)
                result = {"error": msg}, code
                trace = traceback.format_exc()
                log_obj = get_log(f, endpoint, msg, trace=trace)
            logging.info(log_obj)
            return result
        return decorator
    return inner
