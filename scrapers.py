# --- Functions that scrape the parsed webpage for metadata ---
import json
import re
import requests
from bs4 import BeautifulSoup

def http_request(metadata, log, url=False, query=False):
    # --- Parse a webpage for scraping ---

    log.info(f"Metadata URL for get() request: {metadata['url']}")

    # --- Request webpage ---
    timer = 2
    failed = False
    while True:
        try:
            if url and query:
                html_response = requests.get(url, params=query, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'})
            else:
                html_response = requests.get(metadata['url'], headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'})
        except Exception as exc:
            log.error(f"Requests HTML get error: {exc}")
            if timer == 2:
                print('\n\nBad response from webpage, retrying for up-to 25 seconds...')
            elif timer >= 10:
                log.error(f"Requests HTML get error: {exc}")
                print(f"Failed to get webpage page, skipping {metadata['input_folder']}...")
                metadata['skip'] = True
                metadata['failed'] = True
                metadata['failed_exception'] = f"{metadata['input_folder']}: Requests HTML get error: {exc}"
                break
            time.sleep(timer)
            timer = timer * 1.5
        else:
            break

    if metadata['failed']:
        return metadata, html_response

    log.info(f"Requests Status code: {str(html_response.status_code)}")
    if html_response.status_code != requests.codes.ok:
        log.error(f"Requests error: {str(html_response.status_code)}")
        print(f"Bad requests status code, skipping {metadata['input_folder']}: {html_response.status_code}")
        metadata['skip'] = True
        metadata['failed'] = True
        metadata['failed_exception'] = f"{metadata['input_folder']}: Requests status code = {html_response.status_code}"
        return metadata, html_response

    try:
        html_response.raise_for_status()
    except Exception as exc:
        log.error(f"Requests status error: {exc}")
        print(f"Requests raised an error, skipping {metadata['input_folder']}: {exc}")
        metadata['skip'] = True
        metadata['failed'] = True
        metadata['failed_exception'] = f"{metadata['input_folder']}: Requests raised status = {exc}"
        return metadata, html_response
    else:
        # --- Parse webpage for scraping ---
        return metadata, html_response



def api_audible(metadata, page, log):
    # ----- Get metadata from Audible.com API -----


    # --- Author ---
    try:
        authors = page['authors']
        if len(authors) == 1:
            metadata['author'] = page['authors'][0]['name']
        if len(authors) > 1:
            authors_list = []
            for author in authors:
                author_list.append(author)
            metadata['author'] = page['authors'][0]['name']
            metadata['authors_multi'] = authors_list

    except Exception as e:
        log.info("No author in json, using '_unknown_' ({metadata['input_folder']}) | {e}")
        print(f" - Warning: No author found, placing in author folder '_unknown_': {metadata['input_folder']}")
        metadata['author'] = '_unknown_'  # If no author is found, use the name '_unknown_'


    # --- Title ---
    try:
        metadata['title'] = page['title']
    except Exception as e:
        log.info("No title in json, using folder name ({metadata['input_folder']}) | {e}")
        print(f" - Warning: No title found, using folder name: {metadata['input_folder']}")
        metadata['title'] = metadata['input_folder']  # If no title is found, use original foldername


    # --- Summary ---
    try:
        summary_dirty = BeautifulSoup(page['publisher_summary'], 'html.parser')
        metadata['summary'] = summary_dirty.getText()
        log.info(f"summary element: {str(element)}")
    except Exception as e:
        log.info(f"No summary in json, leaving blank ({metadata['input_folder']} | {e}")

    # --- Subtitle ---
    try:
        metadata['subtitle'] = page['subtitle']
    except Exception as e:
        log.info(f"No subtitle scraped, leaving blank ({metadata['input_folder']}) | {e}")

    # --- Narrator ---
    try:
        narrators = page['narrotors']
        if len(narrators) == 1:
            metadata['narrator'] = page['narrators'][0]['name']
        elif len(narrators) > 1:
            narrators_list = []
            for narrator in narrators:
                narrators_list.append(narrator)
            metadata['narrator'] = page['narrators'][0]['name']
            metadata['narrators_multi'] = narrators_list

    except Exception as e:
        log.info("No narrator in json, leaving blank ({metadata['input_folder']}) | {e}")

    # --- Publisher ---
    try:
        metadata['publisher'] = page['publisher_name']
        log.info(f"Publisher: {metadata['publisher']}")
    except Exception as e:
        log.info(f"No publisher in json, leaving blank({metadata['input_folder']}) | {e}")

    # --- Publish Year ---
    try:
        metadata['publishyear'] = re.search(r"(\d{4})", page['release_date'])[1]
        log.info(f"Publish year: {metadata['publishyear']}")
    except Exception as e:
        log.info(f"No publish year in json, leaving blank ({metadata['input_folder']}) | {e}")

    # --- Genres ---
    # try:
    #     # element = meta_json['datePublished']
    #     # metadata['genres'] = element
    #     # !!! element = parsed.select_one('li.narratorLabel > a:nth-child(1)')
    #     # !!! metadata['publisheryear'] = element.getText()
    #     log.info(f"Genres element: {str(element)}")
    # except:
    #     log.info(f"No genres in json, leaving blank ({metadata['input_folder']}) | {e}")

    # --- Series ---
    try:
        series = page['series']
        if len(series) == 1:
            metadata['series'] = page['series'][0]['title']
        if len(series) > 1:
            series_list = []
            for serie in series:
                series_list.append(serie)
            metadata['series'] = page['series'][0]['title']
            metadata['series_multi'] = series_list
    except Exception as e:
        log.info(f"No series in json, leaving blank ({metadata['input_folder']}) | {e}")

    # --- Volume Number ---
    try:
        metadata['volumenumber'] = page['series'][0]['sequence']
        log.info(f"Volume number element: {str(element)}")
    except Exception as e:
        log.info(f"No volume number in json, leaving blank ({metadata['input_folder']}) | {e}")

    return metadata


def scrape_goodreads(parsed, metadata, log):
    # ----- Scrape a Goodreads.com book page for metadata -----

    # --- Author ---
    try:
        element = parsed.select_one('#bookAuthors')
        log.info(f"Author element: {str(element)}")
        element = element.find('a')
        metadata['author'] = element.getText(strip=True)
    except Exception as e:
        log.info(f"No author in bs4, using '_unknown_' ({metadata['input_folder']}) | {e}")
        print(f" - Warning: No author scraped, placing in author folder '_unknown_': {metadata['input_folder']}")
        metadata['author'] = '_unknown_'  # If no author is found, use the name '_unknown_'

    # --- Title ---
    try:
        element = parsed.select_one('#bookTitle')
        log.info(f"Title element: {str(element)}")
        metadata['title'] = element.getText(strip=True)
    except Exception as e:
        log.info(f"No title scraped, using '_unknown_' ({metadata['input_folder']}) | {e}")
        print(f" - Warning: No title scraped, using folder name: {metadata['input_folder']}")
        metadata['title'] = metadata['input_folder']  # If no title is found, use original foldername

    # --- Summary ---
    try:
        element = parsed.select_one('#description')
        log.info(f"Summary element: {str(element)}")
        summary = element.find_all('span')[1]
        if summary is None:
            summary = element.find('span')
        metadata['summary'] = summary.getText()
    except Exception as e:
        log.info(f"No summary scraped, leaving blank ({metadata['input_folder']}) | {e}")

    # --- Series ---
    try:
        element = parsed.select_one('#bookSeries')
        log.info(f"Series element: {str(element)}")
        if element is not None:
            series = re.search('(\w.+),? #\d+', element.getText(strip=True))
            metadata['series'] = series[1]
    except Exception as e:
        log.info(f"No series scraped, leaving blank ({metadata['input_folder']}) | {e}")

    # --- Series Number ---
    if metadata['series'] != '':
        try:
            element = parsed.select_one('#bookSeries')
            log.info(f"Volume number element: {str(element)}")
            if element is not None:
                number = re.search('\w.+,? #([\d\.]+)', element.getText(strip=True))
                metadata['volumenumber'] = number[1]
        except Exception as e:
            log.info(f"No volume number scraped, leaving blank ({metadata['input_folder']}) | {e}")


    return metadata
