import logging
import os
import traceback
from enum import Enum
from logging.handlers import RotatingFileHandler

from asgi_correlation_id import CorrelationIdFilter
from pythonjsonlogger import json

from src.core.config import get_settings
from src.core.context_var import task_uuid_var


class LogLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    DEBUG = "debug"
    EXCEPTION = "exception"


def log_with_content_var(
    msg: str, level: LogLevel = LogLevel.INFO, error: Exception = None, **kwargs
):
    """
    通用日志方法。
    自动拼接 task_uuid，并支持完整异常信息(error)。
    建议在 task 上下文可能使用到的地方使用此方法记录日志。
    """
    task_uuid = task_uuid_var.get() or ""

    extra = " ".join(f"{k}={v}" for k, v in kwargs.items())
    extra_str = f" {extra}" if extra else ""

    if task_uuid:
        full_msg = f"[task_uuid={task_uuid}] {msg}{extra_str}"
    else:
        full_msg = f"{msg}{extra_str}"

    # --- 错误情况 ---
    if error:
        tb = traceback.format_exc()
        full_msg = f"{full_msg}\n{tb}"

        # EXCEPTION = 自动调用 exception()
        if level == LogLevel.EXCEPTION:
            logger.exception(full_msg)
        else:
            logger.error(full_msg)
        return

    # --- 正常情况 ---
    log_map = {
        LogLevel.INFO: logger.info,
        LogLevel.WARNING: logger.warning,
        LogLevel.ERROR: logger.error,
        LogLevel.DEBUG: logger.debug,
    }

    if level == LogLevel.EXCEPTION:
        logger.error(full_msg)
    else:
        log_map.get(level, logger.info)(full_msg)


def setup_logger(module: str = "aigc"):
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/{module}.log"
    cid_filter = CorrelationIdFilter()
    root_logger = logging.getLogger()
    if get_settings().app_env.is_not_prod():
        # Development or beta environment - use human-readable format
        formatter = logging.Formatter(
            "[%(correlation_id)s] -  %(asctime)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d -  "
            "%(message)s"
        )
    else:
        # Production environment - use JSON format
        formatter = json.JsonFormatter(
            "%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d %(correlation_id)s %(message)s",
            json_ensure_ascii=False,
        )
    level = logging.INFO
    # if get_settings().app_env.is_dev():
    #     level = logging.DEBUG
    if log_file:
        file_handler = RotatingFileHandler(
            log_file, mode="a", maxBytes=10 * 1024 * 1024, backupCount=3
        )
        file_handler.setFormatter(formatter)
        file_handler.addFilter(cid_filter)
        root_logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.addFilter(cid_filter)
    root_logger.setLevel(level)
    root_logger.addHandler(stream_handler)
    return root_logger


logger = logging.getLogger()
