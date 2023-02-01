# :book: BadaBoomBooks :bomb:

Quickly organize audiobooks using the terminal and a web-browser


# Dependencies
* A web-browser
* [Python 3.8+](https://www.python.org/)
* `pip install -r requirements.txt`


# Description
The inconsistencies between audiobooks don't make for reliable matches using fully-automated solutions. This program is a semi-automatic process, that way you can be sure your books are matched properly, while only taking a couple clicks and a few seconds per book.

After calling the script and passing it audiobook folders, it will read the ID3 tags of your audiobook and make a websearch for `{title} by {author}` in your web browser. If the tags are blank it'll fallback to the folder name.

All you need to do is select the correct web-page, copy the URL, and the folder will be added to the queue. The whole process usually only takes a few seconds per book.

Once every folder you passed has been added to the queue, the organization will begin, at which point no further user-input is required. By default, folders are outputted to `./_BadaBoomBooks_/` in the same directory as the input folder, this way you can keep track of which ones you've already processed.

# Examples

### - Basic - 

This is is the most basic usage, only folders are renamed, filenames will be unnaffected. For first-timers, I recommend running this on a copy of your audiobook to see how it works.

ℹ️ Rename (move) audiobook folders to  `{author}/{title}` structure

`$ python ./BadaBoomBooks.py '/Path/to/Audiobook-1/' '/Path/to/Audiobook-2/' ...`

### - AudioBookShelf (Recommended) -
The ASIN from Audible will be saved to a `metadata.opf` file, which AudioBookShelf will read during a library scan. Using that ASIN number, AudioBookShelf will be able to perform a perfect quick-match, which means you'll have the exact metadata corresponding to this book. The `info.txt` file is used by SmartAudioBookPlayer to display a summary, doesn't cost us anything to include it.

ℹ️ Flatten folders, rename files to `{author}/{title}/## - {title}`, generate `metadata.opf`, and generate `info.txt`.

`$python ./BadaBoomBooks.py -f -r -o -i '/Path/to/Audiobook-1/' '/Path/to/Audiobook-2/' ...`


# Tips
* The default behaviour is to RENAME the audiobook folders, pass the `-c` flag to copy instead.
* The process is smoother if you have the terminal and browser side-by-side.
* The terminal can sometimes have a character limit, avoid going over it by breaking up large jobs into smaller batches.
* 

```
$ python ./BadaBoomBooks.py --help

=========================================================================================

    ______           _      ______                      ______             _
    | ___ \         | |     | ___ \                     | ___ \           | |
    | |_/ / __ _  __| | __ _| |_/ / ___   ___  _ __ ___ | |_/ / ___   ___ | | _____
    | ___ \/ _` |/ _` |/ _` | ___ \/ _ \ / _ \| '_ ` _ \| ___ \/ _ \ / _ \| |/ / __|
    | |_/ / (_| | (_| | (_| | |_/ / (_) | (_) | | | | | | |_/ / (_) | (_) |   <\__ \
    \____/ \__,_|\__,_|\__,_\____/ \___/ \___/|_| |_| |_\____/ \___/ \___/|_|\_\___/

                            An audioBook organizer (v0.35)

=========================================================================================

usage: python BadaBoomBooks.py [-h] [-O OUTPUT] [-c] [-d] [-f] [-i] [-o] [-r] [-s] [-v] folder [folder ...]

Organize audiobook folders through webscraping metadata

positional arguments:
  folder         Audiobook folder(s) to be organized

optional arguments:
  -h, --help     show this help message and exit
  -O OUTPUT      Path to place organized folders
  -c, --copy     Copy folders instead of renaming them
  -d, --debug    Enable debugging to log file
  -f, --flatten  Flatten book folders, useful if the player has issues with multi-folder books
  -i, --infotxt  Generate 'info.txt' file, used by SmartAudioBookPlayer to display book summary
  -o, --opf      Generate 'metadata.opf' file, used by Audiobookshelf to import metadata
  -r, --rename   Rename audio tracks to '## - {title}' format
  -s , --site    Specify the site to perform initial searches [audible, goodreads, both]
  -v, --version  show program's version number and exit

Cheers to the community for providing our content and building our tools!

----------------------------------- INSTRUCTIONS --------------------------------------

1) Call the script and pass it the audiobook folders you would like to process, including any optional arguments...
    python BadaBoomBooks.py "C:\Path\To\Audiobook_folder1" "C:\Path\To\Audiobook_folder2" ...
    python BadaBoomBooks.py -s audible -c -o -i "C:\Path\To\Audiobook_folder1" "C:\Path\To\Audiobook_folder2" ...

2) Your browser will open and perform a web search for the current book, simply select the correct web-page and copy the url to your clipboard.

3) After building the queue, the process will start and folders will be organized accordingly. Cheers!

```
