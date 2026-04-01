import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin


def get_soup(url):
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, "html.parser")
    return soup


def parse_data(soup, page, url):
    quotes = soup.find_all("div", class_="quote")
    quotes_data = []
    for quote in quotes:

        contents = quote.find("span", class_="text").text.strip()

        author = quote.find("small", class_="author").text.strip()

        tags = quote.div.find_all("a", class_="tag")
        tags_data = []
        for tag in tags:
            tags_data.append(tag.text)
        if tags_data:
            tag_text = ",".join(tags_data)
        else:
            tag_text = "No tags"

        quote_length = len(contents)

        tags_count = len(tags_data)

        part = {"Contents": contents, "Author": author, "Tags": tag_text, "Length": quote_length,
                "Amount of tags": tags_count, "Page": page}
        quotes_data.append(part)
    return quotes_data


def get_page(soup, current_url):
    next_but = soup.find("li", class_="next")
    if next_but:
        next_href = next_but.find("a")["href"]
        next_url = urljoin(current_url, next_href)
        return next_url
    return None


def save_to_csv(data):
    with open("dane-quotes.csv", "w", encoding="utf-8", newline="") as f:
        fieldnames = data[0].keys()

        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)
    return f

if __name__ == "__main__":
    url = "https://quotes.toscrape.com/"
    all_data = []
    page = 1

    while url:
        soup = get_soup(url)
        quotes = parse_data(soup, page, url)
        all_data.extend(quotes)

        url = get_page(soup, url)
        page += 1
    save_to_csv(all_data)
