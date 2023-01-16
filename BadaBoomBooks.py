__version__ = 0.3

from pathlib import Path
import argparse
import base64
import configparser
import json
import logging as log
import re
import shutil
import sys
import time
import webbrowser

root_path = Path(sys.argv[0]).resolve().parent
sys.path.append(str(root_path))
from scrapers import http_request, api_audible, scrape_goodreads
from optional import create_opf, create_info, flatten_folder, rename_tracks

from bs4 import BeautifulSoup
from tinytag import TinyTag
import pyperclip
import requests

# --- Define globals ---
config_file = root_path / 'queue.ini'
debug_file = root_path / 'debug.log'
opf_template = root_path / 'template.opf'
default_output = '_BadaBoomBooks_'  # In the same directory as the input folder

# --- Logging configuration ---
log.basicConfig(level=log.DEBUG, filename=str(debug_file), filemode='w', style='{', format="Line: {lineno} | Level: {levelname} |  Time: {asctime} | Info: {message}")

# --- Configuring queue.ini ---
config = configparser.ConfigParser()
config.optionxform = lambda option: option
config['urls'] = {}
log.debug(config_file)

# --- Book processing results ---
failed_books = []
skipped_books = []
success_books = []


print(fr"""

=========================================================================================

    ______           _      ______                      ______             _
    | ___ \         | |     | ___ \                     | ___ \           | |
    | |_/ / __ _  __| | __ _| |_/ / ___   ___  _ __ ___ | |_/ / ___   ___ | | _____
    | ___ \/ _` |/ _` |/ _` | ___ \/ _ \ / _ \| '_ ` _ \| ___ \/ _ \ / _ \| |/ / __|
    | |_/ / (_| | (_| | (_| | |_/ / (_) | (_) | | | | | | |_/ / (_) | (_) |   <\__ \
    \____/ \__,_|\__,_|\__,_\____/ \___/ \___/|_| |_| |_\____/ \___/ \___/|_|\_\___/

                            An audioBook organizer (v{__version__})

=========================================================================================
""")

parser = argparse.ArgumentParser(prog='python BadaBoomBooks.py', formatter_class=argparse.RawTextHelpFormatter, description='Organize audiobook folders through webscraping metadata', epilog=f"""
Cheers to the community for providing our content and building our tools!

----------------------------------- INSTRUCTIONS --------------------------------------

1) Call the script and pass it the audiobook folders you would like to process, including any optional arguments...
    python BadaBoomBooks.py "C:\Path\To\Audiobook_folder1\" "C:\Path\To\Audiobook_folder2" ...
    python BadaBoomBooks.py -s audible -c -o -i "C:\Path\To\Audiobook_folder1\" "C:\Path\To\Audiobook_folder2\" ...

2) Your browser will open and perform a web search for the current book, simply select the correct web-page and copy the url to your clipboard.

3) After building the queue, the process will start and folders will be organized accordingly. Cheers!
""")

# ===== Prepare vaild arguments =====
parser.add_argument('-O', dest='output', metavar='OUTPUT', help='Path to place organized folders')
parser.add_argument('-c', '--copy', action='store_true', help='Copy folders instead of renaming them')
parser.add_argument('-d', '--debug', action='store_true', help='Enable debugging to log file')
parser.add_argument('-f', '--flatten', action='store_true', help="Flatten book folders, useful if the player has issues with multi-folder books")
parser.add_argument('-i', '--infotxt', action='store_true', help="Generate 'info.txt' file, used by SmartAudioBookPlayer to display book summary")
parser.add_argument('-o', '--opf', action='store_true', help="Generate 'metadata.opf' file, used by Audiobookshelf to import metadata")
parser.add_argument('-r', '--rename', action='store_true', help="Rename audio tracks to '## - {title}' format")
parser.add_argument('-s', '--site', metavar='',  default='both', choices=['audible', 'goodreads', 'both'], help="Specify the site to perform initial searches [audible, goodreads, both]")
parser.add_argument('-v', '--version', action='version', version=f"Version {__version__}")
parser.add_argument('folders', metavar='folder', nargs='+', help='Audiobook folder(s) to be organized')

args = parser.parse_args()

if args.output:
    test_output = Path(args.output).resolve()
    if not test_output.is_dir():
        log.debug(f"Output is not a directory/exists: {test_output}")
        print(f"\nThe output path is not a directory or does not exist: {test_output}")
        input("\nPress enter to exit...")
        sys.exit()


if not args.debug:
    # --- Logging disabled ---
    log.disable(log.CRITICAL)


def clipboard_queue(folder, config):
    # ----- Search for audibooks then monitor clipboard for URL -----

    book_path = folder.resolve()
    # - Try for search terms from id3 tags

    title = False
    author = False

    for file in book_path.glob('**/*'):
        if file.suffix in ['.mp3', '.m4a', '.m4b', '.wma', '.flac']:
            log.debug(f"TinyTag audio file: {file}")
            track = TinyTag.get(str(file))
            try:
                title = re.sub(r"\&", 'and', track.album).strip()
                if title == '':
                    title = False
                author = re.sub(r"\&", 'and', track.artist).strip()
                if author == '':
                    author = False
                break
            except Exception as e:
                log.debug("Couldn't get search term metadata from ID3 tags, using foldername ({file})")

    if title and author:
        search_term = f"{title} by {author}"
    elif title:
        search_term = title
    else:
        search_term = str(book_path.name)

    # - Prompt user to copy AudioBook url
    log.info(f"Search term: {search_term}")
    if args.site == 'audible':
        webbrowser.open(f"https://duckduckgo.com/?t=ffab&q=site:audible.com {search_term}", new=2)
    elif args.site == 'goodreads':
        webbrowser.open(f"https://duckduckgo.com/?t=ffab&q=site:goodreads.com {search_term}", new=2)
    elif args.site == 'both':
        webbrowser.open(f"https://duckduckgo.com/?t=ffab&q=audible.com goodreads.com {search_term}", new=2)

    clipboard_old = pyperclip.paste()
    log.debug(f"clipboard_old: {clipboard_old}")

    if (re.search(r"http.+goodreads.+book/show/\d+", clipboard_old)) or (re.search(r"http.+audible.+/pd/[\w-]+Audiobook/\w+\??", clipboard_old)) or (re.search(r"skip", clipboard_old)):  # Remove old script contents from clipboard
        clipboard_old = '__clipboard_cleared__'
        pyperclip.copy(clipboard_old)

    # - Wait for  url to be coppied
    print(f"\nCopy the Audible or Goodreads URL for \"{book_path.name}\"\nCopy 'skip' to skip the current book...           ", end='')
    while True:
        time.sleep(1)
        clipboard_current = pyperclip.paste()

        if clipboard_current == clipboard_old:  # Clipboard contents have not yet changed
            continue
        elif clipboard_current == 'skip':  # user coppied 'skip' to clipboard
            log.info(f"Skipping: {book_path.name}")
            print(f"\n\nSkipping: {book_path.name}")
            skipped_books.append(book_path.name)
            break
        elif re.search(r"^http.+audible.+/pd/[\w-]+Audiobook/\w{10}", clipboard_current):
            # --- A valid Audible URL ---
            log.debug(f"Clipboard Audible match: {clipboard_current}")

            audible_url = re.search(r"^http.+audible.+/pd/[\w-]+Audiobook/\w{10}", clipboard_current)[0]
            b64_folder = base64.standard_b64encode(bytes(str(book_path.resolve()), 'utf-8')).decode()
            b64_url = base64.standard_b64encode(bytes(audible_url, 'utf-8')).decode()

            log.debug(f"b64_folder: {b64_folder}")
            log.debug(f"b64_url: {b64_url}")

            config['urls'][b64_folder] = b64_url
            print(f"\n\nAudible URL: {audible_url}")
            break
        elif re.search(r"^http.+goodreads.+book/show/\d+", clipboard_current):
            # --- A valid Goodreads URL
            log.debug(f"Clipboard GoodReads match: {clipboard_current}")

            goodreads_url = re.search(r"^http.+goodreads.+book/show/\d+", clipboard_current)[0]
            b64_folder = base64.standard_b64encode(bytes(str(book_path.resolve()), 'utf-8')).decode()
            b64_url = base64.standard_b64encode(bytes(goodreads_url, 'utf-8')).decode()

            log.debug(f"b64_folder: {b64_folder}")
            log.debug(f"b64_url: {b64_url}")

            config['urls'][b64_folder] = b64_url
            print(f"\n\nGoodreads URL: {goodreads_url}")
            break
        else:
            continue

    pyperclip.copy(clipboard_old)
    return config


# ==========================================================================================================
# ==========================================================================================================

# ===== Create Path() objects for each argument folder =====
folders = [Path(argument).resolve() for argument in args.folders]

for folder in folders:
    # --- Verify integrity of input folders ---
    exists = folder.is_dir()
    if not exists:
        print(f"The input folder '{folder.name}' does not exist or is not a directory...")
        input('Press enter to exit...')
        sys.exit()

log.debug(folders)


# ===== Build the queue using the .ini =====
for folder in folders:
    folder = folder.resolve()
    config = clipboard_queue(folder, config)
    print('\n-------------------------------------------')

print('\n===================================== PROCESSING ====================================')

with config_file.open('w', encoding='utf-8') as file:
    config.write(file)

# ===== Process all keys (folders) in .ini file =====
config.read(config_file, encoding='utf-8')
for key, value in config.items('urls'):
    log.debug(f"Key: '{key}' ({type(key)}) - Value: '{value}' ({type(value)}")
    try:
        folder = base64.standard_b64decode(bytes(key, 'utf-8')).decode()
        url = base64.standard_b64decode(bytes(value, 'utf-8')).decode()
        log.debug(f"Folder: {folder} - URL: {url}")
    except Exception as exc:
        log.debug(f"Exception: {exc}")
        continue

    # ----- Scrape metadata -----
    folder = Path(folder).resolve()

    metadata = {
        'author': '',
        'authors_multi': '',
        'title': '',
        'summary': '',
        'subtitle': '',
        'narrator': '',
        'publisher': '',
        'publishyear': '',
        'genres': '',
        'isbn': '',
        'asin': '',
        'series': '',
        'sereis_multi': '',
        'volumenumber': '',
        'url': url,
        'skip': False,
        'failed': False,
        'failed_exception': '',
        'input_folder': str(folder.resolve().name)
    }

    print(f"\n----- {metadata['input_folder']} -----")

    # --- Request Metadata ---
    while True:

        if 'audible.com' in metadata['url']:
            # --- ASIN ---
            metadata['asin'] = re.search(r"^http.+audible.+/pd/[\w-]+Audiobook/(\w{10})", metadata['url'])[1]
            query = {'response_groups': 'contributors,product_desc,series,product_extended_attrs,media'}
            metadata, response = http_request(metadata, log, f"https://api.audible.com/1.0/catalog/products/{metadata['asin']}", query)
            if metadata['skip'] is True:
                break
            page = response.json()['product']
            metadata = api_audible(metadata, page, log)
            break

        elif 'goodreads.com' in metadata['url']:
            metadata, response = http_request(metadata, log)
            if metadata['skip'] is True:
                break
            parsed = BeautifulSoup(response.text, 'html.parser')
            if parsed.select_one('#bookTitle') is not None:
                metadata = scrape_goodreads(parsed, metadata, log)
                break

    if metadata['failed'] is True:
        failed_books.append(f"{metadata['input_folder']} ({metadata['failed_exception']})")
    if metadata['skip'] is True:
        continue

    print(f"""
Title: {metadata['title']}
Author: {metadata['author']}
URL: {metadata['url']}""")

    # ----- [--output] Prepare output folder -----
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = folder.parent / f"{default_output}/"

    # - Clean paths -
    author_clean = re.sub(r"[^\w\-\.\(\) ]+", ' ', metadata['author'])
    title_clean = re.sub(r"[^\w\-\.\(\) ]+", ' ', metadata['title'])
    author_folder = output_path / f"{author_clean}/"
    author_folder.resolve()
    author_folder.mkdir(parents=True, exist_ok=True)
    final_output = author_folder / f"{title_clean}/"
    metadata['final_output'] = final_output.resolve()

    print(f"\nOutput: {metadata['final_output']}")

    # ----- [--copy] Copy/move book folder ---
    if args.copy:
        print(f"\nCopying...")
        shutil.copytree(folder, metadata['final_output'], dirs_exist_ok=True, copy_function=shutil.copy2)
    else:  # - Move folder (defult) -
        print(f"\nMoving...")
        try:
            folder.rename(metadata['final_output'])
        except Exception as e:
            log.info(f"Couldn't move folder directly, performing copy-move (metadata['title']) | {e}")
            shutil.copytree(folder, metadata['final_output'], dirs_exist_ok=True, copy_function=shutil.copy2)
            shutil.rmtree(folder)

    # ----- [--flatten] Flatten Book Folders -----
    if args.flatten:
        print('\nFlattening...')
        flatten_folder(metadata, log)

    # ----- [--rename] Rename audio tracks -----
    if args.rename:
        print('\nRenaming...')
        rename_tracks(metadata, log)

    # ----- [--opf] Create .opf file -----
    if args.opf:
        print("\nCreating 'metadata.opf'")
        create_opf(metadata, opf_template)

    # ----- [--i] Create info.txt file -----
    if args.infotxt:
        print("\nCreating 'info.txt'")
        create_info(metadata)

    # ---- Folder complete ----
    print(f"\nDone!")
    success_books.append(f"{folder.stem}/ --> {output_path.stem}/{metadata['author']}/{metadata['title']}/")


# ===== Summary =====
if failed_books:
    log.critical(f"Failed metadata scrapes: {','.join(failed_books)}")
    print('\n\n====================================== FAILURES ======================================')
    for failure in failed_books:
        print(f"\nFailed: {failure}", end='')
    print()
    if skipped_books:
        print('\n\n====================================== SKIPPED ======================================')
        for skipped in skipped_books:
            print(f"\nSkipped: {skipped}", end='')
        print()
    if success_books:
        print('\n\n====================================== SUCCESS ======================================')
        for book in success_books:
            print(f"\nSuccess: {book}", end='')
    print('\n\n====================================== WARNING ======================================')
    print('\nSome books did not get processed successfully...\n')
    input('press enter to exit...')
    sys.exit()
else:
    log.info('Completed without errors')
    if skipped_books:
        print('\n\n====================================== SKIPPED ======================================')
        for skipped in skipped_books:
            print(f"\nSkipped: {skipped}", end='')
        print()
    print('\n\n====================================== SUCCESS ======================================')
    for book in success_books:
        print(f"\nSuccess: {book}", end='')
    print('\n\n====================================== COMPLETE ======================================')
    print('\nCheers to the community providing our content and building our tools!\n')
    input('Press enter to exit...')
    sys.exit()
