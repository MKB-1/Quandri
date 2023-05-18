from robot.api import logger

import os

from shared.utils import createLogger, SCIENTISTS
from wikipedia_scraper import RobotProducer


filename = os.path.basename(__file__).split('.')[0]
createLogger(filename)

robot = RobotProducer("Victorito-Producer")

def introduce_yourself():
    robot.say_hello()

def main():
    introduce_yourself()
    for scientist in SCIENTISTS:
        robot.extract_scientist_data(scientist)

    robot.say_goodbye()
    
if __name__ == "__main__":
    main()
