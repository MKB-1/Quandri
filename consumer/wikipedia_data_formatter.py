from robot.api import logger

from datetime import datetime, timedelta
from io import TextIOWrapper
import math
import json
import traceback

from shared.custom_typing import JSONData


class RobotConsumer:
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

    def _get_json(self, filename: str) -> JSONData:
        with open(f"../producer/data/{filename}.json", encoding="UTF-8") as file:
            data = json.load(file)
            
        return data
    
    def _calculate_age_at_death(self, data: JSONData) -> timedelta:
        try:
            birth_date = data["infobox"]["extracted_birth_date"]
            death_date = data["infobox"]["extracted_death_date"]
        except KeyError:
            logger.info(f"There was an error accessing the extracted_birth_date or extracted_death_date keys in JSONData", also_console=True)
            logger.error(traceback.format_exc())
        except Exception:
            logger.info(f"There was an error with JSONData", also_console=True)
            logger.error(traceback.format_exc())

        delta = datetime.strptime(death_date, "%Y-%m-%d") - datetime.strptime(birth_date, "%Y-%m-%d")

        return delta
    
    def write_to_file(self, scientist_name: str, file: TextIOWrapper):
        data = self._get_json(scientist_name)
        delta = self._calculate_age_at_death(data)

        file.write(f"### {scientist_name}\n")
        file.write(f"* Lived for {math.floor(delta.days / 365.25)} years and {delta.days % 365.25} days *\n")
