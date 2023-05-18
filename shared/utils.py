import logging
import os


SCIENTISTS = ["Albert Einstein", "Isaac Newton", "Not A Real Scientist", "Marie Curie", "Charles Darwin", "Babadook"]

def createLogger(filename: str):
    """
    Creates a logger for the given filename.
    If only one file is logging, then logging can be done using robot.api.logger
    For multiple files, must use the returned logger.
    Returned logger also has information for which file called it at which line,
    robot.api.logger does not
    """
    LOG_FILE_PATH = f'output/{filename}.log'

    if os.path.exists(LOG_FILE_PATH):
        os.remove(LOG_FILE_PATH)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [{%(filename)s:%(lineno)d}] [%(levelname)s] - %(message)s",
        filename=LOG_FILE_PATH
    )
    
    return logging.getLogger(__name__)

    