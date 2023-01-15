# :book: BadaBoomBooks :bomb:

#### Quickly organize audiobooks using a terminal and a web-browser

# Dependencies
* Python 3.8+
* `pip install -r requirements.txt`

# Usage
Move and organize audiobook folders into `{author}/{title}` using Audible metadata

`$ python ./BadaBoomBooks.py '/Path/to/Audiobook-1/' '/Path/to/Audiobook-2/' ...`

# Help
```
$ python ./BadaBoomBooks.py --help 

=========================================================================================

    ______           _      ______                      ______             _
    | ___ \         | |     | ___ \                     | ___ \           | |
    | |_/ / __ _  __| | __ _| |_/ / ___   ___  _ __ ___ | |_/ / ___   ___ | | _____
    | ___ \/ _` |/ _` |/ _` | ___ \/ _ \ / _ \| '_ ` _ \| ___ \/ _ \ / _ \| |/ / __|
    | |_/ / (_| | (_| | (_| | |_/ / (_) | (_) | | | | | | |_/ / (_) | (_) |   <\__ \
    \____/ \__,_|\__,_|\__,_\____/ \___/ \___/|_| |_| |_\____/ \___/ \___/|_|\_\___/

                            An audioBook organizer (v0.1)

=========================================================================================

usage: python BadaBoomBooks.py [-h] [-f] [-O OUTPUT] [-c] [-d] [-i] [-o] [-s] [-v] folder [folder ...]

Organize audiobook folders through webscraping metadata

positional arguments:
  folder         Audiobook folder(s) to be organized

optional arguments:
  -h, --help     show this help message and exit
  -f, --flatten  Flatten book folders, useful if the player has issues with multi-folder books
  -O OUTPUT      Path to place organized folders
  -c, --copy     Copy folders instead of renaming them
  -d, --debug    Enable debugging to log file
  -i, --infotxt  Generate 'info.txt' file, used by SmartAudioBookPlayer to display book summary
  -o, --opf      Generate 'metadata.opf' file, used by Audiobookshelf to import metadata
  -s , --site    Specify the site to perform initial searches [audible]
  -v, --version  show program's version number and exit

Cheers to the community for providing our content and building our tools!

----------------------------------- INSTRUCTIONS --------------------------------------

1) Call the script and pass it the audiobook folders you would like to process, including any optional arguments...
    python BadaBoomBooks.py "C:\Path\To\Audiobook_folder1" "C:\Path\To\Audiobook_folder2" ...
    python BadaBoomBooks.py -c -i -o "C:\Path\To\Audiobook_folder1" "C:\Path\To\Audiobook_folder2" ...

2) Your browser will open and perform a web search for the current book, simply open the Audible page and copy the url to your clipboard.

3) After building the queue, the process will start and folders will be organized accordingly. Cheers!
```
