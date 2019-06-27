#!/usr/bin/env python
# -*- coding: utf-8 -*-

from application.models import user, todo


def all():
    result = []
    models = [user, todo]

    for m in models:
        result += m.__all__

    return result


__all__ = all()
