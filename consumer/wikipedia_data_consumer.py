import os
import pprint as pp

from wikipedia_data_formatter import RobotConsumer
from shared.utils import createLogger, SCIENTISTS

filename = os.path.basename(__file__).split('.')[0]
createLogger(filename)

robot = RobotConsumer("Victorito-Consumer")

def main():
    with open("data/test.txt", "w", encoding="UTF-8") as file:
        file.write("# SCIENTISTS")
        robot.write_to_file(SCIENTISTS[0], file)

if __name__ == "__main__":
    main()
