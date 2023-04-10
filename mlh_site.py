from bs4 import BeautifulSoup
from requests_html import HTMLSession
import re

from utils import parse_date

mlh_sites = [
    "https://organize.mlh.io/participants/events/9508-ghw-api-week-opening-ceremony",
    "https://organize.mlh.io/participants/events/9509-ghw-api-week-stack-overflow-workshop",
    "https://organize.mlh.io/participants/events/9511-ghw-api-week-technical-stream",
    "https://organize.mlh.io/participants/events/9510-ghw-api-week-tetris-tournament",
    "https://organize.mlh.io/participants/events/9512-ghw-api-week-technical-stream",
    "https://organize.mlh.io/participants/events/9513-ghw-api-week-developing-an-app-to-interact-with-the-spotify-api-part-1",
    "https://organize.mlh.io/participants/events/9514-ghw-api-week-scribbl-io-mini-event",
    "https://organize.mlh.io/participants/events/9515-ghw-api-week-your-first-api-documentation",
    "https://organize.mlh.io/participants/events/9516-ghw-api-week-technical-session",
    "https://organize.mlh.io/participants/events/9517-ghw-api-week-technical-session",
    "https://organize.mlh.io/participants/events/9518-ghw-api-week-bob-ross-ms-paint",
    "https://organize.mlh.io/participants/events/9530-ghw-api-week-technical-session"
]

session = HTMLSession()


def get_event_data(url):
    r = session.get(url)
    title_selector = 'body > div.d-flex.flex-column.bg-near-white > div.participation.bg-near-white.pt-5.position-relative > div.header.container.d-flex.align-items-stretch.px-0.mt-3.border.border-bottom-0.border-black-20.border-radius-top-3.position-relative > div > div.event-details.col-lg-4.px-0.bg-white.d-flex.flex-column.justify-content-between > div.px-4.pt-4 > div:nth-child(1) > h1'
    title = r.html.find(title_selector)
    title = title[0].text
    date_selector = 'body > div.d-flex.flex-column.bg-near-white > div.participation.bg-near-white.pt-5.position-relative > div.header.container.d-flex.align-items-stretch.px-0.mt-3.border.border-bottom-0.border-black-20.border-radius-top-3.position-relative > div > div.event-details.col-lg-4.px-0.bg-white.d-flex.flex-column.justify-content-between > div.px-4.pt-4 > div:nth-child(2) > div.d-flex.align-items-center.mb-4 > div.my-1 > div.text-dark-gray.text-semibold.lh-title'
    start_date = r.html.find(date_selector)
    start_date = start_date[0].text
    time_selector = 'body > div.d-flex.flex-column.bg-near-white > div.participation.bg-near-white.pt-5.position-relative > div.header.container.d-flex.align-items-stretch.px-0.mt-3.border.border-bottom-0.border-black-20.border-radius-top-3.position-relative > div > div.event-details.col-lg-4.px-0.bg-white.d-flex.flex-column.justify-content-between > div.px-4.pt-4 > div:nth-child(2) > div.d-flex.align-items-center.mb-4 > div.my-1 > div.text-dark-gray.font-size-6'
    time = r.html.find(time_selector)
    time = time[0].text.strip().split()
    if len(time) == 4:
        starts, _, ends, zone = time
        end_date = start_date
    elif len(time) == 6:
        starts = time[0]
        ends = time[4]
        zone = time[5]
        end_date = f"{time[2]} {time[3]} {start_date.split()[-1]}"
    else:
        raise ValueError(f"Unexpected time format {time}")

    starts = f"{start_date} {starts} {zone}"
    ends = f"{end_date} {ends} {zone}"

    event = {
        "title": title,
        "starts": parse_date(starts),
        "ends": parse_date(ends),
        "zone": zone,
        "url": url,
        "raw_data": {
            "starts": starts,
            "ends": ends,
        }
    }
    return event


def main():
    for site in mlh_sites[:1]:
        data = get_event_data(site)
        print(data)


if __name__ == "__main__":
    main()
