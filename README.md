# :book: BadaBoomBooks :bomb:

Quickly organize audiobooks using the terminal and a web-browser

# Dependencies
* A web-browser
* Python 3.8+
* `pip install -r requirements.txt`

# Description
The inconsistencies between audiobooks don't make for reliable matches using fully-automated solutions. This semi-automatic process means that you can be sure your books are matched properly, while only taking a couple clicks and a few seconds per book.

After calling the script and passing it audiobook folders, it will read the ID3 tags of your audiobook and make a websearch for `{title} by {author}` in your web browser.

All you need to do is select the correct web-page, copy the URL, and the folder will be added to the queue. The whole process usually only takes only a few seconds per book.

Once every folder you passed has been added to the queue, the organization will begin, at which point no further user-input is required.

# Usage
Move and organize audiobook folders into `{author}/{title}` using scraped metadata

`$ python ./BadaBoomBooks.py '/Path/to/Audiobook-1/' '/Path/to/Audiobook-2/' ...`

# Tips
* The default behaviour is to RENAME the audiobook folders, pass the `-c` flag to copy instead.
* The process is smoother if you have the terminal and browser side-by-side.
* The terminal can sometimes have a character limit, avoid going over it by breaking up large jobs into smaller batches.

```
$ python ./BadaBoomBooks.py --help

=========================================================================================

    ______           _      ______                      ______             _
    | ___ \         | |     | ___ \                     | ___ \           | |
    | |_/ / __ _  __| | __ _| |_/ / ___   ___  _ __ ___ | |_/ / ___   ___ | | _____
    | ___ \/ _` |/ _` |/ _` | ___ \/ _ \ / _ \| '_ ` _ \| ___ \/ _ \ / _ \| |/ / __|
    | |_/ / (_| | (_| | (_| | |_/ / (_) | (_) | | | | | | |_/ / (_) | (_) |   <\__ \
    \____/ \__,_|\__,_|\__,_\____/ \___/ \___/|_| |_| |_\____/ \___/ \___/|_|\_\___/

                            An audioBook organizer (v0.2)

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
