from src.scraper import WikipediaScraper
import time

start_time = time.time()
base_url = "https://country-leaders.onrender.com"
leaders_endpoint = base_url + "/leaders"
cookie_endpoint = base_url + "/cookie"
check_endpoint = base_url + "/check"
country_endpoint = base_url + "/countries"
output = "leaders.json"
csvoutput = "countries"


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
    wiki.to_csv_files(output, csvoutput)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
