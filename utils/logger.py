import logging


class BasicFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[0;36m",  # Cyan
        logging.INFO: "\033[0;32m",  # Green
        logging.WARNING: "\033[0;33m",  # Yellow
        logging.ERROR: "\033[0;31m",  # Red
        logging.CRITICAL: "\033[1;31m",  # Bright Red
    }
    RESET = "\033[0m"

    def format(self, record):
        log_fmt = (
            f"{self.COLORS.get(record.levelno)}%(levelname)s:{self.RESET} %(message)s"
        )
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class CustomFormatter(logging.Formatter):
    cyan_format = "\033[0;36m%s\033[0m"
    green_format = "\033[0;32m%s\033[0m"
    yellow_format = "\033[0;33m%s\033[0m"
    red_format = "\033[0;31m%s\033[0m"
    bright_red_format = "\033[1;31m%s\033[0m"

    def format(self, record):
        if record.levelno == logging.DEBUG:
            return self.cyan_format % super().format(record)
        elif record.levelno == logging.INFO:
            return self.green_format % super().format(record)
        elif record.levelno == logging.WARNING:
            return self.yellow_format % super().format(record)
        elif record.levelno == logging.ERROR:
            return self.red_format % super().format(record)
        elif record.levelno == logging.CRITICAL:
            return self.bright_red_format % super().format(record)
        return super().format(record)


cli_logger = logging.getLogger("cli")
cli_logger.propagate = False
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
cli_logger.addHandler(handler)
