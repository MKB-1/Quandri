from RPA.Browser.Selenium import Selenium
from robot.api import logger
from SeleniumLibrary.errors import ElementNotFound
from selenium.webdriver.remote.webelement import WebElement

import json
import traceback
from typing import List

from shared.custom_typing import InfoboxDict, JSONData
from shared.TalkativeRobot import TalkativeRobot

br = Selenium()

class RobotProducer(TalkativeRobot):
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print("Hello, my name is " + self.name)
        print("As a producer robot, my job is to create jobs for the consumer robot.")
        print("For this task, I will navigate to the appropriate wikipedia articles, extract the relevant data, preprocess the data, and save it as a json file.\n")
        

    def say_goodbye(self):
        print("Now that I've retrieved all the data, my job is done. Don't forget to run the consumer robot!")

    def extract_scientist_data(self, scientist_name: str):
        """
        Opens a new browser, searches wikipedia for scientist name, extracts first paragraph & infobox data, and closes browser.
        Parameters:
            scientist_name (str): string to use as key for searching Wikipedia and naming file with extracted data.
        """
        logger.info(f"Producing {scientist_name} data...", also_console=True)
        self._search_wikipedia(scientist_name)
        self._extract_data_from_wikipedia_webpage(scientist_name)
        br.close_browser()
        

    def _search_wikipedia(self, search_term: str):
        """
        Opens wikipedia in the English language and navigates to the search term page.
        Searching on wikipedia can result in 4 cases:
        Case 1. Search results in a wikipedia article which is a person
                e.g. Marie Curie -> https://en.wikipedia.org/wiki/Marie_Curie
        Case 2. Search results in a wikipedia article which is not a person
                e.g. Pisa -> https://en.wikipedia.org/wiki/Pisa
        Case 3. Search results in a wikipedia article with Category: Disambiguation pages
                e.g. Marie -> https://en.wikipedia.org/wiki/Marie
        Case 4. Search results in a wikipedia search with links to articles
                e.g. Search for me -> https://en.wikipedia.org/w/index.php?search=search+for+me&title=Special%3ASearch&ns0=1

        Parameters:
            search_term (str): string to search in Wikipedia
        """

        br.open_available_browser("https://www.wikipedia.org/")

        search_box: WebElement = br.find_element(locator="id:searchInput")
        search_btn: WebElement = br.find_element(locator="xpath://div[3]/form/fieldset/button")
        
        br.input_text_when_element_is_visible(locator=search_box, text=search_term)
        br.click_button(search_btn)

    def _extract_data_from_wikipedia_webpage(self, title: str) -> None:
        """
        Navigates to a wikipedia article and extracts the first paragraph and key-value pairs from the infobox.
        Saves data as a json file at data/title.json
        Parameters:
            title (str): string to use as file name for extracted data.
        """
        data: JSONData = {}

        # If _search_wikipedia results in a page with different formatting (i.e. Case 3 & 4), throw an error and log it
        # This is a pretty lazy implementation but it allows us to submit new searches without worrying about crashing the robot
        try:
            decoded_string = self._get_first_paragraph()
            infobox_data = self._get_infobox()
        except Exception:
            logger.info(f"There was an error retrieving {title} from Wikipedia\n", also_console=True)
            logger.error(traceback.format_exc())
            return

        data['first_paragraph'] = decoded_string
        data["infobox"] = infobox_data

        # Save data to a file (to simulate a database) to simulate parallel computing of producer & consumer
        logger.info("...Saving data to json...\n", also_console=True)
        with open(f"data/{title}.json", "w") as file:
            json.dump(data, file, indent=4)
    
    def _get_first_paragraph(self) -> str:
        """
        Retrieves the first paragraph of a wikipedia article by selecting the first non-empty <p> in the div with id="bodyContent".
        Finds the first non-empty <p> by selecting first <p> without class="mw-empty-elt"
        Returns:
            str: Text contained in <p>
        """
        body_content_web_element: WebElement = br.find_element(locator="id:bodyContent")
        first_paragraph_web_element: WebElement = br.find_element(locator='xpath:.//p[not(@class="mw-empty-elt")][1]', parent=body_content_web_element)
        first_paragraph_text: str = br.get_text(first_paragraph_web_element)
        return first_paragraph_text
    
    def _get_infobox(self) ->InfoboxDict:
        """
        Finds infobox table, iterates through its rows, and extracts data as a dict.
        Does not properly extract data for every row because there are too many different cases to account for.
        If the header of the row is known, preprocessing can be done within this method.
        Data preprocessing should be done within this method because it is easier to do on WebElements than on strings.
        Returns
            InfoBoxDict: Dict with the webscrapped data
        """
        infobox_data: InfoboxDict = {}
        tbody_web_element: WebElement = br.find_element(locator='xpath://table[contains(@class, "infobox")]/tbody[1]')
        tr_list: List[WebElement] = br.find_elements(locator="xpath:.//tr", parent=tbody_web_element)

        # We will iterate over all rows of the table and save the data in a dict
        # Rows usually have 1 th and 1 td, which will be the key: value pair of our dict
        # Note that the value in td must be found. 
        #   Case 1. Td contains a combination of text & html elements (e.g. <a>University of Zurich</a>, Zurich, <span>Switzerland</span>)
        #   Case 2. Td contains an unordered list of list items. Each list item can have a combination of text and html elements within.
        #   Case 3. Tr contains only th or only td. (ignored)
        #   Case 4. Td contains ul but relevant text is not inside ul. (ignored) (e.g. Albert Einstein Spouses)

        for tr in tr_list:
            # If Case 3, continue
            try:
                th = br.find_element(locator="xpath:.//th", parent=tr)
                td = br.find_element(locator="xpath:.//td", parent=tr)
            except ElementNotFound:
                continue
            except Exception:
                logger.error(traceback.format_exc())


            th_text = th.get_attribute("innerText")
            
            # If Case 2 or 4, then iterate through list items and get innerText for each
            # Else if Case 1, then get innerText of td
            li_list = br.find_elements(locator="xpath:.//ul/li", parent=td)
            if li_list:
                td_val = [li.get_attribute("innerText") for li in li_list]
            else:
                td_val = td.get_attribute("innerText")
            
            infobox_data[th_text] = td_val

            # Since we're interested in the length of life, we're extracting the necessary information when we encounter it
            # For both Born and Died we can find a date string in the format "YYYY-MM-DD" within a <span>
            if th_text == 'Born':
                logger.info("...Preprocessing birth date...", also_console=True)
                # birth_date format: YYYY-MM-DD
                birth_date = br.find_element(locator='xpath:.//span[@class="bday"]', parent=td).get_attribute("innerHTML")
                infobox_data["extracted_birth_date"] = birth_date
            elif th_text == 'Died':
                logger.info("...Preprocessing death date...", also_console=True)
                death_date = br.find_element(locator='xpath:.//span', parent=td).get_attribute("innerHTML")
                # death_date format: (YYYY-MM-DD)
                infobox_data["extracted_death_date"] = death_date[1:-1]  # remove parenthesis around death_date
            

        return infobox_data
        