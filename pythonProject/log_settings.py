log_config = {
    "version": 1,
    "formatters": {
        "stream_formater": {
            "format": "%(levelname)s - %(message)s"
        },
        "file_formater": {
            "format": "%(asctime)s - %(levelname)s - %(message)s",
            "datefmt": '%d %m %Y - %H:%M'
        },
    },
    "handlers": {
        "stream_handler": {
            "class": "logging.StremHandler",
            "formatter": "stream_formater",
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "formatter": "file_formater",
            "filename": "bot.log",
            "encoding": "UTF-8",
            "mode": "w"
        },
    },
    "loggers": {
        "main": {
            "handlers": ["stream_handler", "file_handler"],
            "level": "DEBUG",
        },
    },
}