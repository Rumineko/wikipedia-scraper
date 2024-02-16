import json
from requests import Session
from bs4 import BeautifulSoup
import re
import csv


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
        cookie = self.session.get(cookie_endpoint)
        return cookie

    def get_countries(self):
        country_endpoint = self.country_endpoint
        cookie = self.refresh_cookie()
        result = self.session.get(country_endpoint, cookies=cookie.cookies).json()
        return result

    def get_first_paragraph(self, wikipedia_url):
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
        # Use the with statement to open the file in write mode
        with open(filepath, "w", encoding="utf-8") as file:
            # Use the json.dump() function to write the dictionary to the file
            json.dump(self.get_leaders(), file, ensure_ascii=False, indent=1)

    def to_csv_files(self, infile: str, output_dir: str):
        with open(infile, "r", encoding="utf-8") as file:
            data = json.load(file)

        for key, value in data.items():
            csv_filename = f"{output_dir}/{key}.csv"
            with open(csv_filename, "w", encoding="utf-8", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(value[0].keys())  # Write header row
                for item in value:
                    writer.writerow(item.values())

    def sanitize(self, paragraph):
        paragraph = re.sub(
            r"<.*?>|\[.*?\]|\(.*?\)|\{.*?\}|\[.*?\]|\/.*?\/|\|.*?\|", "", paragraph
        )
        paragraph = re.sub(r"\s+", " ", paragraph)
        paragraph = re.sub(r" ,", ",", paragraph)
        return paragraph

    def get_leaders(self):
        check_url = self.base_url + "/check"
        check = self.session.get(check_url)
        countries = self.get_countries()
        if check.status_code != 200:
            cookies = self.refresh_cookie()
        leaders_per_country = self.leaders_data
        for country in countries:
            leaders_per_country[country] = self.session.get(
                self.leaders_endpoint + "?country=" + country, cookies=cookies.cookies
            ).json()
        for country in countries:
            for leader in leaders_per_country[country]:
                leader_url = leader["wikipedia_url"]
                first_paragraph = self.get_first_paragraph(leader_url)
                leader["first_paragraph"] = first_paragraph
        return leaders_per_country
