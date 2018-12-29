
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, ALL_COMPLETED
from datetime import datetime
import os
import re
import time
import urllib

import boto3
from bs4 import BeautifulSoup
from environs import Env
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException



WEBSITE = r'https://www.hltv.org'
BASE_URL = WEBSITE + r'/results'
DEMO_FOLDER = os.getcwd() + r'/demos'
START_OFFSET = 0

last_update = datetime.min



top10_c9 = ['astralis', 'liquid', 'natus vincere', 'mibr', 'faze', 'mousesports', 'nip', 'nrg', 'big', 'north', 'cloud9']

executor = ThreadPoolExecutor(max_workers=2)

futures = []

def upload_demo(demo_file):
    env = Env()
    aws_access_key_id = env('AWS_ACCESS_KEY_ID')
    aws_secret_key_id = env('AWS_SECRET_ACCESS_KEY')
    region_name = env('REGION_NAME')
    bucket = env('BUCKET')

    file_path = DEMO_FOLDER + '\\' + demo_file
    try:
        s3_connection = boto3.resource('s3', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_key_id)
        s3_connection.Bucket(bucket).upload_file(file_path, demo_file)
        os.remove(file_path)
        return None
    except Exception:
        return demo_file

def parse_results_page(html):
    results_soup = BeautifulSoup(html, 'html.parser')

    # Ignore the featured results at the top of the page. We find the overall results div, then get the direct child
    # that is called results-holder
    all_results = results_soup.find('div', {'class': 'results'})
    no_featured = all_results.find('div', {'class': 'results-holder'}, recursive=False)

    entries = no_featured.find_all('div', {'class': 'result-con'})

    team1s = []
    team2s = []
    for e in entries:
        td = e.find('div', {'class': 'team1'})
        team1_div = td.find('div', {'class': 'team'})
        team1 = team1_div.text
        team1s.append(team1)

        td = e.find('div', {'class': 'team2'})
        team2_div = td.find('div', {'class': 'team'})
        team2 = team2_div.text
        team2s.append(team2)

    urls = [t.a['href'] for t in entries]
    assert len(team1s) == len(urls)
    jobs = []
    for i in range(len(team1s)):
        top10_game = team1s[i].lower() in top10_c9 or team2s[i].lower() in top10_c9
        if top10_game:
            jobs.append(urls[i])
    jobs = [WEBSITE + j for j in jobs]
    return jobs


def queue_demo_inferno(html):
    results_soup = BeautifulSoup(html, 'html.parser')

    played_maps = results_soup.findAll('div', {'class': 'played'})
    for 


def parse_result_page(html):
    result_soup = BeautifulSoup(html, 'html.parser')
    match_page = result_soup.find('div', {'class': 'match-page'})
    teams = match_page.find_all('div', {'class': 'team'})
    assert len(teams) == 2

    team_prefixes = ['team1', 'team2']
    # This will store the result for the match
    result = {}
    team_info = {}
    for t, prefix in zip(teams, team_prefixes):
        team_info['region'] = t.img['title'] if t.img is not None else None
        team_link = t.find('a')
        if team_link:
            a = re.search(r'team/(d+)', team_link['href'])
            team_info['id'] = a.group(1) if a else None
        else:
            team_info['id'] = None
        team_info['name'] = t.find('div', {'class': 'teamName'}).text
        team_info['score'] = t.find(prefix+'-gradient').find('div').text

        # Add the prefix to the above to eventually convert to flat
        temp_dict = {(prefix+k): team_info[k] for k in team_info}
        result = {**result, **temp_dict}
    
    time_and_event = match_page.find('div', {'class': 'timeAndEvent'})
    result['time'] = time_and_event.find('div', {'class': 'date'})['data-unix']
    
    event = time_and_event.find('div', {'class': 'event'})
    result['event'] = event.a.text
    event_id = re.search(r'/events/(\d+)', event.a['href'])
    result['event_id'] = event_id.group(1) if event_id else None




def block_until_free_thread():
    while(len(futures) >= 2):
        futures_part = wait(futures, FIRST_COMPLETED)
        futures = futures_part.not_done


def process_results_page(result_url):
    get_page(result_url)
    try:
        demo_stream_box = session.find_element_by_partial_link_text(r'GOTV Demo')
    except NoSuchElementException:
        print('No GOTV demo found for ' + result_url)
        return
    # Before we click let's get a list of the file names in the directory for later on. 
    # Use the new file not appearing in this list to know which file we got
    preclick_files = file_names = os.listdir(DEMO_FOLDER)
    demo_stream_box.click()
    #parse the result page

    #parse_result_page(html)
    
    
    # Sleep to give it some time to create the file
    time.sleep(20)
    # Firefox leaves a .rar.part file in the directory while it is downloading. The best way to detect if we are done downloading
    # if when we stop detecting that file in there.
    filtered = [None]
    while len(filtered) > 0:
        file_names = os.listdir(DEMO_FOLDER)
        filtered = [f for f in file_names if '.rar.part' in f]
    postclick_files = os.listdir(DEMO_FOLDER)
    new_file_set = set(postclick_files) - set(preclick_files)
    # How to handle?
    assert len(new_file_set) == 1

    new_file_name = new_file_set.pop() 
    # Now batch the file for uploading to s3 
    futures.append(executor.submit(upload_demo, new_file_name))
    



def get_page(url, params= None):
    if params is not None:
        param_str = '&'.join([p + '=' + str(params[p]) for p in params])    
        url_enc = url + '?' + param_str
    else:
        url_enc = url
    since_last_request = (datetime.now() - last_update).total_seconds()
    if since_last_request < 1:
        time.sleep(since_last_request) 
    session.get(url_enc)
    return session.page_source
    
if __name__ == '__main__':
    
    # See https://selenium-python.readthedocs.io/faq.html#how-to-auto-save-files-using-custom-firefox-profile
    fp = webdriver.FirefoxProfile()

    fp.set_preference("browser.download.folderList",2)
    fp.set_preference("browser.download.manager.showWhenStarting",False)
    fp.set_preference("browser.download.dir", DEMO_FOLDER)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-rar-compressed")


    session = webdriver.Firefox(firefox_profile=fp)
    offset = START_OFFSET

    while offset < 3000:
       
        text = get_page(BASE_URL, params={'offset':offset})
        jobs = parse_results_page(text)
        list(map(process_results_page, jobs))

        offset += 100
    
    wait(futures, ALL_COMPLETED)
    #r._from_results_page(r.text)