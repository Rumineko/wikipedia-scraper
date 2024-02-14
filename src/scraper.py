import json
from requests import Session
from bs4 import BeautifulSoup
import re


class WikipediaScraper:
    def __init__(
        self,
        base_url: str,
        country_endpoint: str,
        leaders_endpoint: str,
        cookies_endpoint: str,
        leaders_data: dict,
        cookie: object,
    ):
        self.base_url = base_url
        self.country_endpoint = country_endpoint
        self.leaders_endpoint = leaders_endpoint
        self.cookies_endpoint = cookies_endpoint
        self.leaders_data = leaders_data
        self.cookie = cookie
        self.session = Session()

    def refresh_cookie(self):
        cookie_endpoint = self.cookies_endpoint
        session = Session()
        cookie = session.get(cookie_endpoint)
        return cookie

    def get_countries(self):
        session = Session()
        country_endpoint = self.country_endpoint
        cookie = self.refresh_cookie()
        result = session.get(country_endpoint, cookies=cookie.cookies).json()
        return result

    def get_first_paragraph(self, wikipedia_url):
        self.wikipedia_url = wikipedia_url
        session = Session()
        response = session.get(wikipedia_url)
        soup = BeautifulSoup(response.text, "html.parser")
        for paragraph in soup.find_all("p"):
            text = paragraph.get_text().strip()
            if text and paragraph.find("b"):
                first_paragraph = text
                first_paragraph = self.sanitize(first_paragraph)
                break
        return first_paragraph

    def get_leaders(self):
        leaders_endpoint = self.leaders_endpoint
        check_url = self.base_url + "/check"
        session = Session()
        check = session.get(check_url)
        countries = self.get_countries()
        if check.status_code != 200:
            cookies = self.refresh_cookie()
        leaders_per_country = self.leaders_data
        for country in countries:
            leaders_per_country[country] = session.get(
                leaders_endpoint + "?country=" + country, cookies=cookies.cookies
            ).json()
        for country in countries:
            for leader in leaders_per_country[country]:
                leader_url = leader["wikipedia_url"]
                first_paragraph = self.get_first_paragraph(leader_url)
                leader["first_paragraph"] = first_paragraph
        return leaders_per_country

    def to_json_file(self, filepath: str):
        self.filepath = filepath
        # Use the with statement to open the file in write mode
        with open(filepath, "w", encoding="utf-8") as file:
            # Use the json.dump() function to write the dictionary to the file
            json.dump(self.get_leaders(), file, ensure_ascii=False)

    def sanitize(self, paragraph):
        self.paragraph = paragraph
        paragraph = re.sub(
            r"<.*?>|\[.*?\]|\(.*?\)|\{.*?\}|\[.*?\]|\/.*?\/|\|.*?\|", "", paragraph
        )
        paragraph = re.sub(r"\s+", " ", paragraph)
        paragraph = re.sub(r" ,", ",", paragraph)
        return paragraph
