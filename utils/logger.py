import logging

def get_logger(name="AIDetector"):
    """
    Initialize and return a customized logger.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
    return logger
