# :book: BadaBoomBooks :bomb:

Quickly organize audiobooks using a terminal and a web-browser

# Dependencies
* A web-browser
* Python 3.8+
* `pip install -r requirements.txt`

# Description
After calling the script and passing it audiobook folders, it will read the ID3 tags of your audiobook and make a websearch for `{title} by {author}` in your web browser. 

All you need to do is select the right web-page, copy the URL, and the folder will be added to the queue. The whole process takes only a few seconds per book, meaning you can organize even a very large library in very little time.

Once every folder you passed has been added to the queue, the organization will begin, at which point no further user-input is required.

The inconsistencies between audiobooks don't make for reliable matches using fully-automated solutions. This semi-automatic process means that you can be sure your books are matched properly, and it only takes a couple clicks and a few seconds.

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
