#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/4 下午4:09
# @File    : logers.py
import sys
from loguru._logger import *
from loguru import _defaults
from .mail_config import mail_config as _mail_config
from .mail_send import __MailSend as mail_send


class ELogger(Logger):
    email = False
    mail_config = _mail_config

    def add(
            self,
            sink,
            *,
            level=_defaults.LOGURU_LEVEL,
            format=_defaults.LOGURU_FORMAT,
            filter=_defaults.LOGURU_FILTER,
            colorize=_defaults.LOGURU_COLORIZE,
            serialize=_defaults.LOGURU_SERIALIZE,
            backtrace=_defaults.LOGURU_BACKTRACE,
            diagnose=_defaults.LOGURU_DIAGNOSE,
            enqueue=_defaults.LOGURU_ENQUEUE,
            catch=_defaults.LOGURU_CATCH,
            **kwargs
    ):
        if 'email' in kwargs:
            self.email = kwargs['email']
            mail_send.config = self.mail_config
            del kwargs['email']
        super(ELogger, self).add(sink=sink,
                                 level=_defaults.LOGURU_LEVEL,
                                 format=_defaults.LOGURU_FORMAT,
                                 filter=_defaults.LOGURU_FILTER,
                                 colorize=_defaults.LOGURU_COLORIZE,
                                 serialize=_defaults.LOGURU_SERIALIZE,
                                 backtrace=_defaults.LOGURU_BACKTRACE,
                                 diagnose=_defaults.LOGURU_DIAGNOSE,
                                 enqueue=_defaults.LOGURU_ENQUEUE,
                                 catch=_defaults.LOGURU_CATCH,
                                 **kwargs)

    def _log(self, level_id, static_level_no, from_decorator, options, message, args, kwargs):
        core = self._core

        if not core.handlers:
            return

        (exception, depth, record, lazy, colors, raw, capture, patcher, extra) = options

        frame = get_frame(depth + 2)

        try:
            name = frame.f_globals["__name__"]
        except KeyError:
            name = None

        try:
            if not core.enabled[name]:
                return
        except KeyError:
            enabled = core.enabled
            if name is None:
                status = core.activation_none
                enabled[name] = status
                if not status:
                    return
            else:
                dotted_name = name + "."
                for dotted_module_name, status in core.activation_list:
                    if dotted_name[: len(dotted_module_name)] == dotted_module_name:
                        if status:
                            break
                        enabled[name] = False
                        return
                enabled[name] = True

        current_datetime = aware_now()

        if level_id is None:
            level_icon = " "
            level_no = static_level_no
            level_name = "Level %d" % level_no
        else:
            try:
                level_name, level_no, _, level_icon = core.levels[level_id]
            except KeyError:
                raise ValueError("Level '%s' does not exist" % level_id) from None

        if level_no < core.min_level:
            return

        code = frame.f_code
        file_path = code.co_filename
        file_name = basename(file_path)
        thread = current_thread()
        process = current_process()
        elapsed = current_datetime - start_time

        if exception:
            if isinstance(exception, BaseException):
                type_, value, traceback = (type(exception), exception, exception.__traceback__)
            elif isinstance(exception, tuple):
                type_, value, traceback = exception
            else:
                type_, value, traceback = sys.exc_info()
            exception = RecordException(type_, value, traceback)
        else:
            exception = None
        log_record = {
            "elapsed": elapsed,
            "exception": exception,
            "extra": {**core.extra, **context.get(), **extra},
            "file": RecordFile(file_name, file_path),
            "function": code.co_name,
            "level": RecordLevel(level_name, level_no, level_icon),
            "line": frame.f_lineno,
            "message": str(message),
            "module": splitext(file_name)[0],
            "name": name,
            "process": RecordProcess(process.ident, process.name),
            "thread": RecordThread(thread.ident, thread.name),
            "time": current_datetime,
        }

        if lazy:
            args = [arg() for arg in args]
            kwargs = {key: value() for key, value in kwargs.items()}

        if capture and kwargs:
            log_record["extra"].update(kwargs)

        if record:
            if "record" in kwargs:
                raise TypeError(
                    "The message can't be formatted: 'record' shall not be used as a keyword "
                    "argument while logger has been configured with '.opt(record=True)'"
                )
            kwargs.update(record=log_record)

        if colors:
            if args or kwargs:
                colored_message = Colorizer.prepare_message(message, args, kwargs)
            else:
                colored_message = Colorizer.prepare_simple_message(str(message))
            log_record["message"] = colored_message.stripped
        elif args or kwargs:
            colored_message = None
            log_record["message"] = message.format(*args, **kwargs)
        else:
            colored_message = None

        if core.patcher:
            core.patcher(log_record)

        if patcher:
            patcher(log_record)

        for handler in core.handlers.values():
            handler.emit(log_record, level_id, from_decorator, raw, colored_message)
        return log_record

    def __call_email(self, log_record):
        if log_record and self.email:
            mail_send.config = self.mail_config
            log_str = ''
            split = ' | '
            if 'time' in log_record:
                log_str += str(log_record['time'])[:20] + split
            if 'level' in log_record:
                log_str += str(log_record['level'].name) + split
            if 'file' in log_record:
                log_str += str(log_record['file'].name) + split

            if 'line' in log_record:
                log_str += str(log_record['line']) + split
            if 'message' in log_record:
                log_str += str(log_record['message'])
            mail_send.send(log_str)

    def error(__self, __message, *args, **kwargs):
        log_record = __self._log("ERROR", None, False, __self._options, __message, args, kwargs)
        __self.__call_email(log_record)

    def debug(__self, __message, *args, **kwargs):
        log_record = __self._log("DEBUG", None, False, __self._options, __message, args, kwargs)
        __self.__call_email(log_record)

    def trace(__self, __message, *args, **kwargs):
        r"""Log ``message.format(*args, **kwargs)`` with severity ``'TRACE'``."""
        log_record = __self._log("TRACE", None, False, __self._options, __message, args, kwargs)
        __self.__call_email(log_record)

    def info(__self, __message, *args, **kwargs):
        r"""Log ``message.format(*args, **kwargs)`` with severity ``'INFO'``."""
        log_record = __self._log("INFO", None, False, __self._options, __message, args, kwargs)
        __self.__call_email(log_record)

    def success(__self, __message, *args, **kwargs):
        r"""Log ``message.format(*args, **kwargs)`` with severity ``'SUCCESS'``."""
        log_record = __self._log("SUCCESS", None, False, __self._options, __message, args, kwargs)
        __self.__call_email(log_record)

    def warning(__self, __message, *args, **kwargs):
        r"""Log ``message.format(*args, **kwargs)`` with severity ``'WARNING'``."""
        log_record = __self._log("WARNING", None, False, __self._options, __message, args, kwargs)
        __self.__call_email(log_record)

    def critical(__self, __message, *args, **kwargs):
        r"""Log ``message.format(*args, **kwargs)`` with severity ``'CRITICAL'``."""
        log_record = __self._log("CRITICAL", None, False, __self._options, __message, args, kwargs)
        __self.__call_email(log_record)

    def exception(__self, __message, *args, **kwargs):
        r"""Convenience method for logging an ``'ERROR'`` with exception information."""
        options = (True,) + __self._options[1:]
        log_record = __self._log("ERROR", None, False, options, __message, args, kwargs)
        __self.__call_email(log_record)
