import logging
try:
    import colorama
    from colorama import Fore, Style
    colorama.init()
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False

def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        
        if HAS_COLORAMA:
            formatter = logging.Formatter(
                f"%(asctime)s - {Fore.GREEN}%(name)s{Style.RESET_ALL} - %(levelname)s - %(message)s"
            )
        else:
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger
