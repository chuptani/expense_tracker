import logging


def setup_logging():
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the logging level

    # Create a file handler and set the log level
    file_handler = logging.FileHandler("cli.log")
    file_handler.setLevel(logging.DEBUG)

    # Create a stream handler to log to stdout
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    # Create a formatter and set the format for the log messages
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    formatter2 = logging.Formatter("\033[38;5;160m%(levelname)s\033[0m: %(message)s")

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter2)

    # Add the file handler and stream handler to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def main():
    # Set up logging
    logger = setup_logging()

    # Log some example messages
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")


if __name__ == "__main__":
    main()
