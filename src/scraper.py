import json
from requests import Session
from bs4 import BeautifulSoup
import re
import csv
from multiprocessing import Pool


# Our WikipediaScraper class!!!
class WikipediaScraper:
    # The init method initializes the WikipediaScraper object with the base URL, endpoints, leaders data, and cookie
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
        """
        Function that refreshes the cookie by sending a GET request to the cookies endpoint, only called if the cookie is expired

        :return: Cookie object
        """
        cookie_endpoint = self.cookies_endpoint
        cookie = self.session.get(cookie_endpoint)
        return cookie

    def get_countries(self):
        """
        Function that retrieves the list of countries by sending a GET request to the country endpoint in the API

        :return: Countries list
        """
        country_endpoint = self.country_endpoint
        cookie = self.refresh_cookie()
        result = self.session.get(country_endpoint, cookies=cookie.cookies).json()
        return result

    def get_first_paragraph(self, wikipedia_url):
        """
        Function that retrieves the first paragraph of text from a Wikipedia page. This method is called for each leader in the leaders data
        :param wikipedia_url: Wikipedia URL
        :return: First paragraph of the Wikipedia page, sanitized (no HTML tags, brackets, extra spaces, etc.)
        """
        response = self.session.get(wikipedia_url)
        soup = BeautifulSoup(response.text, "html.parser")
        for paragraph in soup.find_all("p"):
            text = paragraph.get_text().strip()
            if text and paragraph.find("b"):
                first_paragraph = text
                first_paragraph = self.sanitize(first_paragraph)
                break
        return first_paragraph

    def to_json_file(self, filepath: str):
        """
        Function that writes the leaders data to a JSON file for the specified file path, using UTF-8 encoding and indentation so that in case it is written in a different language, it will still be readable
        :param filepath: File path to write the JSON file to
        :return: None, just writes the JSON file
        """
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(self.get_leaders(), file, ensure_ascii=False, indent=1)

    def to_csv_files(self, infile: str, output_dir: str):
        """
        Function that converts the leaders data from a JSON file to multiple CSV files. Each CSV file is named after the country and contains the leaders data for that country
        :param infile: File path to the JSON file
        :param output_dir: Directory to write the CSV files to
        :return: None, just writes the CSV files
        """
        with open(infile, "r", encoding="utf-8") as file:
            data = json.load(file)

        for key, value in data.items():
            csv_filename = f"{output_dir}/{key}.csv"
            with open(csv_filename, "w", encoding="utf-8", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(
                    value[0].keys()
                )  # Write header row with keys as column names
                for item in value:
                    writer.writerow(item.values())

    def sanitize(self, paragraph):
        """
        Function that sanitizes a paragraph of text by removing HTML tags, brackets, extra spaces and other shenanigans
        :param paragraph: Paragraph of text
        :return: Sanitized paragraph of text (no phonetics, no HTML tags, no brackets, no extra spaces, etc.)
        """
        paragraph = re.sub(
            r"<.*?>|\[.*?\]|\(.*?\)|\{.*?\}|\[.*?\]|\/.*?\/|\|.*?\|", "", paragraph
        )
        paragraph = re.sub(r"\s+", " ", paragraph)
        paragraph = re.sub(r" ,", ",", paragraph)
        return paragraph

    def process_leader(self, leader):
        """
        Function that processes a leader by retrieving the first paragraph of text from a Wikipedia page and adding it to the leader data
        :param leader: Leader data
        :return: Leader data with first paragraph added
        """
        leader_url = leader["wikipedia_url"]
        first_paragraph = self.get_first_paragraph(leader_url)
        leader["first_paragraph"] = first_paragraph
        return leader

    def get_leaders(self):
        """
        Function that retrieves the leaders data for each country by sending requests in parallel (using multiprocessing to speed up the process)
        :return: Leaders data for each country
        """
        check_url = self.base_url + "/check"
        check = self.session.get(check_url)
        countries = self.get_countries()
        if check.status_code != 200:
            cookies = self.refresh_cookie()
        leaders_per_country = self.leaders_data

        with Pool() as pool:
            for country in countries:
                leaders = self.session.get(
                    self.leaders_endpoint + "?country=" + country,
                    cookies=cookies.cookies,
                ).json()
                leaders_per_country[country] = pool.map(self.process_leader, leaders)

        return leaders_per_country
