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
    for scientist in SCIENTISTS:
        robot.extract_scientist_data(scientist)

def conclude():
    robot.say_goodbye()


if __name__ == "__main__":
    introduce_yourself()
    main()
    conclude()
