
from datetime import datetime
import time

from bs4 import BeautifulSoup
import cfscrape



BASE_URL = r'https://www.hltv.org/results'
START_OFFSET = 0

last_update = datetime.min

session = cfscrape.Session()

top10_c9 = ['astralis', 'liquid', 'natus vincere', 'mibr', 'faze', 'mousesports', 'nip', 'nrg', 'big', 'north', 'cloud9']

def parse_results_page(html):
    results_soup = BeautifulSoup(html, 'html.parser')

        # Ignore the featured results at the top of the page by grabbing just the result-all dib
    no_featured = results_soup.find('div', {'class': 'results-all'})

    entries = no_featured.find_all('div', {'class': 'result-con'})

    team1s = []
    team2s = []
    for e in entries:
        td = e.find('div', {'class': 'team1'})
        team1_div = td.find('div', {'class': 'team'})
        team1 = team1_div.div.text
        team1s.append(team1)

        td = e.find('div', {'class': 'team2'})
        team2_div = td.find('div', {'class': 'team'})
        team2 = team2_div.div.text
        team2s.append(team2)

    urls = [t.a['href'] for t in entries]
    assert len(team1s) == len(urls)
    jobs = []
    for i in range(len(team1s)):
        top10_game = team1s[i] in top10_c9 or team2s[i] in top10_c9
        if top10_game:
            jobs.append(urls[i])
    return jobs

def get_page(url, params):
    since_last_request = (datetime.now() - last_update).total_seconds()
    if since_last_request < 1:
        time.sleep(since_last_request) 
    r = session.get(url, params=params)
    return r
    
if __name__ == '__main__':
    offset = START_OFFSET

    while offset < 200:
       
        r = get_page('https://www.hltv.org/results', params={'offset':offset})
        jobs = parse_results_page(r.text)



        offset += 100

    r._from_results_page(r.text)