from typing import Dict, List, Union, TypedDict

InfoboxDict = Dict[str, Union[str, List[str]]]

class JSONData(TypedDict):
    first_paragraph: str
    infobox: InfoboxDict