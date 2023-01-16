# --- Functions that scrape the parsed webpage for metadata ---
import json
import re
import requests
from bs4 import BeautifulSoup

def parse_webpage(metadata, log):
    # --- Parse a webpage for scraping ---

    log.info(f"Metadata URL for get() request: {metadata['url']}")

    # --- Request webpage ---
    timer = 2
    failed = False
    while True:
        try:
            html_response = requests.get(metadata['url'], headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'})
        except Exception as exc:
            log.error(f"Requests HTML get error: {exc}")
            if timer == 2:
                print('\n\nBad response from webpage, retrying for up-to 25 seconds...')
            elif timer >= 10:
                log.error(f"Requests HTML get error: {exc}")
                print(f"Failed to get webpage page, skipping {metadata['input_folder']}...")
                metadata['skip'] = True
                failed_books.append(f"{metadata['input_folder']}: Requests HTML get error: {exc}")
                failed = True
                break
            time.sleep(timer)
            timer = timer * 1.5
        else:
            break

    if failed:
        return metadata

    log.info(f"Requests Status code: {str(html_response.status_code)}")
    if html_response.status_code != requests.codes.ok:
        log.error(f"Requests error: {str(html_response.status_code)}")
        print(f"Bad requests status code, skipping {folder.name}: {html_response.status_code}")
        metadata['skip'] = True
        failed_books.append(f"{folder.name}: Requests status code = {html_response.status_code}")
        return metadata

    try:
        html_response.raise_for_status()
    except Exception as exc:
        log.error(f"Requests status error: {exc}")
        print(f"Requests raised an error, skipping {folder.name}: {exc}")
        metadata['skip'] = True
        failed_books.append(f"{folder.name}: Requests raised status = {exc}")
        return metadata
    else:
        # --- Parse webpage for scraping ---
        parsed = BeautifulSoup(html_response.text, 'html.parser')

    return parsed


def scrape_audible(parsed, metadata, log):
    # ----- Scrape a Audible.com book page for metadata -----

    try:
        meta_json = json.loads(parsed.select_one('#bottom-0').find('script').contents[0])[0]
        # print(json.dumps(meta_json, indent=4))
        bs4 = False
        bs4_element = False
    except Exception as e:
        log.info("No json loadable element, using bs4 ({metadata['input_folder']}) | {e}")
        bs4 = True

    # --- ASIN ---
    metadata['asin'] = re.search(r"^http.+audible.+/pd/[\w-]+Audiobook/(\w{10})", metadata['url'])[1]

    # --- Author ---
    if bs4 == False:
        try:
            element = meta_json['author'][0]['name']
            metadata['author'] = element
            log.info(f"author element: {str(element)}")
        except Exception as e:
            log.info("No author in json, trying with bs4 ({metadata['input_folder']}) | {e}")
            bs4_element = True

    if (bs4 == True) or (bs4_element == True):
        try:
            element = parsed.select_one('li.authorLabel > a:nth-child(1)')
            metadata['author'] = element.getText()
        except Exception as e:
            log.info("No author in bs4, using '_unknown_' ({metadata['input_folder']}) | {e}")
            print(f" - Warning: No author scraped, placing in author folder '_unknown_': {metadata['input_folder']}")
            metadata['author'] = '_unknown_'  # If no author is found, use the name '_unknown_'
        bs4_element = False


    # --- Title ---
    if bs4 == False:
        try:
            element = meta_json['name']
            metadata['title'] = element
            log.info(f"title element: {str(element)}")
        except Exception as e:
            log.info(f"No title in json, trying with bs4 ({metadata['input_folder']}) | {e}")
            bs4_element = True

    if (bs4 == True) or (bs4_element == True):
        try:
            element = parsed.select_one('.bc-size-large')
            metadata['title'] = element.getText()
        except Exception as e:
            log.info("No title in bs4, using folder name ({metadata['input_folder']}) | {e}")
            print(f" - Warning: No title scraped, using folder name: {metadata['input_folder']}")
            metadata['title'] = metadata['input_folder']  # If no title is found, use original foldername
        bs4_element = False


    # --- Summary ---
    try:
        # element = meta_json['description']
        # metadata['summary'] = element
        element = parsed.select_one('div.bc-spacing-s2:nth-child(2)')
        metadata['summary'] = element.getText()
        log.info(f"summary element: {str(element)}")
    except Exception as e:
        log.info(f"No summary scraped, leaving blank ({metadata['input_folder']}")
        print(f" - Warning: No summary scraped, leaving blank ({metadata['input_folder']}) | {e}")

    # --- Subtitle ---
    try:
        element = parsed.select_one('span.bc-size-medium')
        log.info(f"subtitle element: {str(element)}")
        metadata['subtitle'] = element.getText()
    except Exception as e:
        log.info(f"No subtitle scraped, leaving blank ({metadata['input_folder']}) | {e}")
        print(f" - Warning: No subtitle scraped, leaving blank ({metadata['input_folder']}) | {e}")

    # --- Narrator ---
    if bs4 == False:
        try:
            element = meta_json['readBy'][0]['name']
            metadata['narrator'] = element
            log.info(f"Narrator element: {str(element)}")
        except Exception as e:
            log.info(f"No narrator in json, trying with bs4 ({metadata['input_folder']}) | {e}")
            bs4_element = True

    if (bs4 == True) or (bs4_element == True):
        try:
            element = parsed.select_one('li.narratorLabel')
            metadata['narrator'] = element.getText()
        except Exception as e:
            log.info("No narrator in bs4, leaving blank ({metadata['input_folder']}) | {e}")
        bs4_element = False

    # --- Publisher ---
    if bs4 == False:
        try:
            element = meta_json['publisher']
            metadata['publisher'] = element
            log.info(f"Publisher element: {str(element)}")
        except Exception as e:
            log.info(f"No publisher in json, leaving blank({metadata['input_folder']}) | {e}")

    # --- Publish Year ---
    if bs4 == False:
        try:
            element = meta_json['datePublished']
            metadata['publishyear'] = re.search(r"(\d{4})", element)[1]
            log.info(f"Publish year element: {str(element)}")
        except:
            log.info(f"No publish year scraped, leaving blank ({metadata['input_folder']}) | {e}")

    # --- Genres ---
    # try:
    #     # element = meta_json['datePublished']
    #     # metadata['genres'] = element
    #     # !!! element = parsed.select_one('li.narratorLabel > a:nth-child(1)')
    #     # !!! metadata['publisheryear'] = element.getText()
    #     log.info(f"Genres element: {str(element)}")
    # except:
    #     log.info(f"No genres scraped, leaving blank ({metadata['input_folder']}) | {e}")
    #     print(f" - Warning: No genres scraped, leaving blank ({metadata['input_folder']}) | {e}")

    # --- Series ---
    try:
        element = parsed.select_one('.seriesLabel > a:nth-child(1)')
        metadata['series'] = element.getText()
        log.info(f"Series element: {str(element)}")
    except Exception as e:
        log.info(f"No series scraped, leaving blank ({metadata['input_folder']}) | {e}")

    # --- Volume Number ---
    try:
        element = parsed.select_one('.seriesLabel').getText()
        element = re.search(r", Book (\d+)", element)[1]
        metadata['volumenumber'] = element
        log.info(f"Volume number element: {str(element)}")
    except Exception as e:
        log.info(f"No volume number scraped, leaving blank ({metadata['input_folder']}) | {e}")

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
