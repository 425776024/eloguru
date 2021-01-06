#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/5 11:18 下午
# @File    : __init__.py.py

import atexit as _atexit
import sys as _sys

from loguru import _defaults
from loguru._logger import Core as _Core
from .elogger import ELogger as _ELogger

__version__ = "0.0.1"

__all__ = ["elogger"]

elogger = _ELogger(_Core(), None, 0, False, False, False, False, True, None, {})

if _defaults.LOGURU_AUTOINIT and _sys.stderr:
    elogger.add(_sys.stderr)

_atexit.register(elogger.remove)
