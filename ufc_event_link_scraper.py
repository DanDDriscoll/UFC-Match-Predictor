from bs4 import BeautifulSoup as bs
import lxml
import requests
from pathlib import Path
import pickle
from file_paths import EVENT_LINKS_PICKLE, MATCH_LINKS_PICKLE
import time

def create_dir(dirname):
    current_dir = Path.cwd()
    path = current_dir/dirname
    try:
        Path(path).mkdir()
    except:
        print(f'{path} exists')
    else:
        print(f'Created{path} directory')


def scrape_match_links(new_event_dict):
    if not MATCH_LINKS_PICKLE.exists():
        print('No Match Links Exist, Creating Match Links')
        match_dict = {}
    else:
        print('Fetched Match Links')
        with open(MATCH_LINKS_PICKLE, 'rb') as fp:
            match_dict = pickle.load(fp)
        if not new_event_dict:
            return match_dict

    events = new_event_dict

    new_match_dict = {}
    for event, url in events:
        response = requests.get(url)
        html = response.content
        doc = bs(html, 'lxml')
        match_links = doc.find('tbody')
        match_links = match_links.find_all('tr')
        match_count = 0
        for link in match_links:
            match_name = f'{match_count}_{event}'
            new_match_dict[match_name] = link.get('data-link')
            match_count += 1

    match_dict.update(new_event_dict)
    with open(MATCH_LINKS_PICKLE, 'wb') as fp:
        pickle.dump(match_dict, fp)


def create_valid_filename(filename):
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c == ' ']).rstrip()


def scrape_event_links():
    """Scrapes ALL UFC Event links from ufcstats.com. May write these to classes to be callable for updates?"""
    url = 'http://ufcstats.com/statistics/events/completed?page=all'
    response = requests.get(url)
    doc = bs(response.content, 'lxml')
    event_links = doc.find('tbody')
    event_links = event_links.find_all('a')

    if not EVENT_LINKS_PICKLE.exists():
        print('does not exist')
        event_dict = {}
    else:
        print('exists')
        with open(EVENT_LINKS_PICKLE, 'rb') as fp:
            event_dict = pickle.load(fp)
            print(event_dict)
    new_event_dict = {}
    for link in event_links:
        event_name = create_valid_filename(link.string.strip())
        if event_name not in event_dict:
            new_event_dict[event_name] = link.get('href')

    event_dict.update(new_event_dict)
    with open(EVENT_LINKS_PICKLE, 'wb') as fp:
        pickle.dump(event_dict, fp)

    return new_event_dict
#     write_event_htmls(new_event_dict)
#
#
# # i dont need to wite htmls???? can just pass links lol wtf
# def write_event_htmls(new_event_dict):
#     start = time.time()
#     count = 1
#
#     for event, url in new_event_dict.items():
#         response = requests.get(url)
#         html = response.content
#         doc = bs(html, 'lxml')
#
#         with open(f'event_htmls/{event}.html', 'w', encoding='utf-8') as f:
#             f.write(str(doc))
#             print(f'Writing event {count} of {len(new_event_dict)}')
#     print(time.time() - start)


if __name__ == '__main__':
    new_event_dict = scrape_event_links()


