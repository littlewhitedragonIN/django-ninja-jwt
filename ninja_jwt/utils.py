from calendar import timegm
from datetime import datetime
from functools import wraps
from importlib import import_module

from django.conf import settings
from django.utils.functional import lazy
from django.utils.timezone import is_naive, make_aware, utc
from six import string_types

from ninja_jwt import exceptions


def token_error(func):
    @wraps(func)
    def _wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exceptions.TokenError as tex:
            raise exceptions.InvalidToken(str(tex))

    return _wrap


def import_callable(path_or_callable):
    if hasattr(path_or_callable, "__call__"):
        return path_or_callable
    else:
        assert isinstance(path_or_callable, string_types)
        package, attr = path_or_callable.rsplit(".", 1)
        packages = import_module(package)
        return getattr(packages, attr)


def make_utc(dt):
    if settings.USE_TZ and is_naive(dt):
        return make_aware(dt, timezone=utc)

    return dt


def aware_utcnow():
    return make_utc(datetime.utcnow())


def datetime_to_epoch(dt):
    return timegm(dt.utctimetuple())


def datetime_from_epoch(ts):
    return make_utc(datetime.utcfromtimestamp(ts))


def format_lazy(s, *args, **kwargs):
    return s.format(*args, **kwargs)


format_lazy = lazy(format_lazy, str)
