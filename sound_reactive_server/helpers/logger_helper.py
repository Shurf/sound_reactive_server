from ..models.server_log_entry import ServerLogEntry
import datetime
import typing
import inspect
import pytz
import threading
import os
from .interface_helper import InterfaceHelper

import logging
logger = logging.getLogger(__name__)


class LoggerHelper:

    __MINIMUM_DB_LOG_LEVEL = logging.INFO

    @staticmethod
    def info(text: str):
        return LoggerHelper.log(
            log_level=logging.INFO, text=text, function=inspect.stack()[1].function)


    @staticmethod
    def debug(text: str):
        return LoggerHelper.log(
            log_level=logging.DEBUG, text=text, function=inspect.stack()[1].function)


    @staticmethod
    def warning(text: str):
        return LoggerHelper.log(
            log_level=logging.WARNING, text=text, function=inspect.stack()[1].function)


    @staticmethod
    def error(text: str):
        return LoggerHelper.log(
            log_level=logging.ERROR, text=text, function=inspect.stack()[1].function)

    @staticmethod
    def log(
            log_level: int,
            text: str,
            function: str = None,
            log_time: datetime.datetime = None,
            thread_id: typing.Optional[int] = None,
            process_id: typing.Optional[int] = None):

        if function is None:
            function = inspect.stack()[1].function
        if log_time is None:
            log_time = datetime.datetime.now(pytz.timezone(InterfaceHelper.TIMEZONE))
        if thread_id is None:
            thread_id = threading.get_ident()
        if process_id is None:
            process_id = os.getpid()

        formatted_time = log_time.strftime(InterfaceHelper.DATETIME_FORMAT)
        logger_message = f'[{formatted_time}][{process_id}:{thread_id}][{function}] {text}'
        logger.log(level=log_level, msg=logger_message)

        if log_level < LoggerHelper.__MINIMUM_DB_LOG_LEVEL:
            return

        ServerLogEntry.add_log_entry(
            log_level=log_level,
            text=text,
            log_function=function,
            log_datetime=log_time,
            process_id=process_id,
            thread_id=thread_id
        )
