# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

import uuid


def uuid4_hex():
    return uuid.uuid4().get_hex()
