# --- Functions that scrape the parsed webpage for metadata ---
import json
import re


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
        log.info(f"Volume Number element: {str(element)}")
    except Exception as e:
        log.info(f"No volume number scraped, leaving blank ({metadata['input_folder']}) | {e}")

    return metadata


def scrape_goodreads(parsed, metadata, log):
    # Scrape a Goodreads.com book page for metadata

    try:
        meta_json = json.loads(parsed.select_one('#__NEXT_DATA__').contents[0])
        print(json.dumps(meta_json, indent=4))
        bs4 = False
        bs4_element = False
    except Exception as e:
        log.info(f"No json loadable element, using bs4 ({metadata['input_folder']}) | {e}")
        bs4 = True

    # --- Author ---
    if bs4 == False:
        try:
            element = meta_json['author'][0]['name']
            metadata['author'] = element
            log.info(f"author element: {str(element)}")
        except Exception as e:
            log.info(f"No author in json, trying with bs4 ({metadata['input_folder']}) | {e}")
            bs4_element = True

    if (bs4 == True) or (bs4_element == True):
        try:
            element = parsed.select_one('.ContributorLinksList > span:nth-child(1) > a:nth-child(1) > span:nth-child(1)')
            metadata['author'] = element.getText()
        except Exception as e:
            log.info(f"No author in bs4, using '_unknown_' ({metadata['input_folder']}) | {e}")
            print(f" - Warning: No author scraped, placing in author folder '_unknown_': {metadata['input_folder']}")
            metadata['author'] = '_unknown_'  # If no author is found, use the name '_unknown_'
        bs4_element = False

    # --- Title ---
    if bs4 == False:
        try:
            element = meta_json['title'][0]['name']
            metadata['title'] = element
            log.info(f"title element: {str(element)}")
        except Exception as e:
            log.info(f"No title in json, trying with bs4 ({metadata['input_folder']}) | {e}")
            bs4_element = True

    if (bs4 == True) or (bs4_element == True):
        try:
            element = parsed.select_one('h1.Text')
            metadata['title'] = element.getText()
        except Exception as e:
            log.info(f"No title in bs4, using '_unknown_' ({metadata['input_folder']}) | {e}")
            print(f" - Warning: No title scraped, placing in title folder '_unknown_': {metadata['input_folder']}")
            metadata['title'] = metadata['input_folder']  # If no title is found, use original foldername
            bs4_element = False

    # --- Summary ---
    if bs4 == False:
        try:
            element = meta_json['summary'][0]['name']
            metadata['summary'] = element
            log.info(f"summary element: {str(element)}")
        except Exception as e:
            log.info(f"No summary in json, trying with bs4 ({metadata['input_folder']}) | {e}")
            bs4_element = True

    if (bs4 == True) or (bs4_element == True):
        try:
            element = parsed.select_one('.TruncatedContent__text--large > div:nth-child(1) > div:nth-child(1)')
            metadata['summary'] = element.getText()
        except Exception as e:
            log.info(f"No summary in bs4, leaving blank ({metadata['input_folder']}) | {e}")
        bs4_element = False

    # --- Series ---
    if bs4 == False:
        try:
            element = meta_json['series'][0]['name']
            metadata['series'] = element
            log.info(f"series element: {str(element)}")
        except Exception as e:
            log.info(f"No series in json, trying with bs4 ({metadata['input_folder']}) | {e}")
            bs4_element = True

    if (bs4 == True) or (bs4_element == True):
        try:
            element = parsed.select_one('.WorkDetails > div:nth-child(2) > dd:nth-child(2) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)')
            metadata['series'] = element.getText()
        except Exception as e:
            log.info(f"No series in bs4, leaving blank ({metadata['input_folder']}) | {e}")
        bs4_element = False

    return metadata
