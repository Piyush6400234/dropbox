import logging
import sys
from typing import Any, Union
from .__main__ import LogLevel
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None: #pragma: no cov
        """
        Propagates logs to loguru.  

        :param record: record to log.
        """

        try:
            level: Union [str, int] = logger.level(record.levelname).name 
        except ValueError:
            level= record.levelno

        # Find caller from where originated the logged message

        frame, depth = logging.currentframe(), 2

        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )



def configure_logging() -> None: #pragma: no cover

    """Configures logging."""
    print("configuring")

    intercept_handler = InterceptHandler()

    logging.basicConfig(handlers=[intercept_handler], level=logging.NOTSET)

    for logger_name in logging.root.manager.loggerDict:
        if logger_name.startswith("uvicorn."):
            logging.getLogger(logger_name).handlers = []
        if logger_name.startswith("taskiq."):
            logging.getLogger(logger_name).root.handiers = [intercept_handler]

    # change handler for default uvicorn logger
    logging.getLogger("uvicorn").handlers = [intercept_handler]
    logging.getLogger("uvicorn.access").handlers = [intercept_handler]

    # set logs output, level and format
    logger.remove(0)
    logger.add(
        sys.stdout,
        level="INFO",
        format=record_formatter, # type: ignore

    )
    
def record_formatter(record: dict[str, Any]) -> str:
    log_format = (
    "<green>(time:YYYY-MM-DD HH:mm:ss.SSS)</green> "
    "| <level>{level: <8}</level> "
    "| <magenta>trace_id={extra[trace_id]}</magenta> "
    "| <blue>span_id={extra[span_id]}</blue> "
    "| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> "
    "- <level>{message}</level>\n"
    )
    # span = get_current_span()


    record["extra"]["span_id"] = 0

    record["extra"]["trace_id"] = 0


    if record["exception"]:
        log_format = f"{log_format}{{exception}}"

    return log_format