#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/5 11:18 下午
# @File    : __init__.py.py

import atexit as _atexit
import sys as _sys

from loguru import _defaults
from loguru._logger import Core as _Core
from .eloguru import ELoguru as _ELoguru

__version__ = "0.0.1"

__all__ = ["eloguru"]

eloguru = _ELoguru(_Core(), None, 0, False, False, False, False, True, None, {})

if _defaults.LOGURU_AUTOINIT and _sys.stderr:
    eloguru.add(_sys.stderr)

_atexit.register(eloguru.remove)
