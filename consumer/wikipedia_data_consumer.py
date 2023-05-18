from robot.api import logger

import os

from wikipedia_data_formatter import RobotConsumer
from shared.utils import createLogger, SCIENTISTS

filename = os.path.basename(__file__).split('.')[0]
createLogger(filename)

robot = RobotConsumer("Victorito-Consumer")

def introduce_yourself():
    robot.say_hello()

def main():
    with open("data/test.md", "w", encoding="UTF-8") as file:
        file.write("# SCIENTISTS\n")
        for scientist in SCIENTISTS:
            logger.info(f"Consuming {scientist} data...", also_console=True)
            robot.write_to_file(scientist, file)

def conclude():
    robot.say_goodbye()

if __name__ == "__main__":
    introduce_yourself()
    main()
    conclude()
