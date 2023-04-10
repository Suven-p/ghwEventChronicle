from dotenv import load_dotenv
import os
import requests
from utils import parse_date


def get_events():
    calendar_id = os.environ['GOOGLE_CALENDAR_ID']
    api_key = os.environ['GOOGLE_API_KEY']
    url = f'https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events?key={api_key}&maxResults=200'
    response = requests.get(url).json()
    events = []
    for event in response['items']:
        try:
            events.append({
                'title': event.get('summary', ''),
                'start': parse_date(event['start']['dateTime']),
                'end': parse_date(event['end']['dateTime']),
                'location': event.get('location', ''),
            })
        except Exception as e:
            print(f"Error when processing {event}", e)
            if event['status'] != 'cancelled':
                raise
    return events


def main():
    print(get_events())


if __name__ == '__main__':
    load_dotenv()
    main()
