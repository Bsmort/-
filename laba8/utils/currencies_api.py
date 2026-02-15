# функция get_currenciesimport requests
from xml.etree import ElementTree as ET
from typing import List
from models.currency import Currency

def get_currencies() -> List[Currency]:
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    try:
        response = requests.get(url)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        
        currencies = []
        for valute in root.findall("Valute"):
            currency = Currency(
                id=int(valute.attrib["ID"]),
                num_code=valute.find("NumCode").text,
                char_code=valute.find("CharCode").text,
                name=valute.find("Name").text,
                value=float(valute.find("Value").text.replace(",", ".")),
                nominal=int(valute.find("Nominal").text)
            )
            currencies.append(currency)
        return currencies
    except Exception as e:
        raise RuntimeError(f"Failed to fetch currencies: {e}")
