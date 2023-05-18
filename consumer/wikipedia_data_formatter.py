from robot.api import logger

from datetime import datetime, timedelta
from io import TextIOWrapper
import math
import json
import traceback

from shared.custom_typing import JSONData
from shared.TalkativeRobot import TalkativeRobot


class RobotConsumer(TalkativeRobot):
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print("Hello, my name is " + self.name)
        print("As a consumer robot, my job is to consume jobs created by the consumer robot.")
        print("For this task, I will navigate to the consumer robot's data directory, retrieve the individual data for each scientist,")
        print("and combine it into a single markdown file.")

    def say_goodbye(self):
        print("Now that I have created the markdown file, my job is done.")
        print("Goodbye Mr.Fregeau.")

    def _get_json(self, filename: str) -> JSONData or None:
        """
        Loads a json file located in ../producer/data/
        Parameters:
            filename (str): file to load
        Returns:
            JSONData if successful else None
        """
        logger.info(f"...Reading {filename}.json...", also_console=True)

        try:
            with open(f"../producer/data/{filename}.json", encoding="UTF-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            logger.info(f"There was an error accessing {filename}.json", also_console=True)
            logger.error(traceback.format_exc())
            return None
        except Exception:
            logger.info(f"There was an error with _get_json", also_console=True)
            logger.error(traceback.format_exc())
            return None
        
        return data
    
    def _calculate_age_at_death(self, data: JSONData) -> timedelta or None:
        """
        Calculates the timedelta between extracted_death_date and extracted_birth_date
        Parameters:
            data (JSONData): Dict which contains data["infobox"]["extracted_birth_date"] & data["infobox"]["extracted_death_date"]
        Returns timedelta if successful else None
        """
        logger.info(f"...Calculating age at death...", also_console=True)

        try:
            birth_date = data["infobox"]["extracted_birth_date"]
            death_date = data["infobox"]["extracted_death_date"]
        except KeyError:
            logger.info(f"There was an error accessing the extracted_birth_date or extracted_death_date keys in JSONData\n", also_console=True)
            logger.error(traceback.format_exc())
            return None
        except Exception:
            logger.info(f"There was an error with _calculate_age_at_death\n", also_console=True)
            logger.error(traceback.format_exc())
            return None

        delta = datetime.strptime(death_date, "%Y-%m-%d") - datetime.strptime(birth_date, "%Y-%m-%d")

        return delta
    
    def write_to_file(self, scientist_name: str, file: TextIOWrapper):
        """
        Writes the name, length of life, and short description for a scientist to the given file.
        Does minimal formatting and expects the file to be saved as a markdown file.
        Parameters:
            scientist_name (str): string to use as key for finding data and writing to file
            file (TextIOWrapper): file to write to
        """
        data = self._get_json(scientist_name)
        delta = self._calculate_age_at_death(data)
        
        # If there was an error with _get_json or _calculate_age_at_death, skip writting to file
        if data is None or delta is None:
            return

        logger.info(f"...Writing to unified file...\n", also_console=True)

        file.write(f"### {scientist_name}\n")
        file.write(f"*Lived for {math.floor(delta.days / 365.25)} years and {round(delta.days % 365.25)} days*\n")
        file.write(data["first_paragraph"])
        file.write("\n\n")
