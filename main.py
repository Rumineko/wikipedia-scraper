from src.scraper import WikipediaScraper

base_url = "https://country-leaders.onrender.com"
leaders_endpoint = base_url + "/leaders"
cookie_endpoint = base_url + "/cookie"
check_endpoint = base_url + "/check"
country_endpoint = base_url + "/countries"
output = "leaders.json"
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second


def main():
    wiki = WikipediaScraper(
        base_url=base_url,
        country_endpoint=country_endpoint,
        leaders_endpoint=leaders_endpoint,
        cookies_endpoint=cookie_endpoint,
        leaders_data={},
        cookie=None,
    )
    wiki.to_json_file(output)


if __name__ == "__main__":
    main()
