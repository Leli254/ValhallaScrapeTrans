This project contains two Python scripts, scrap.py and translators.py, that allow users to scrape text from a website and translate it into multiple languages using Google Translate API.
Requirements

    Python 3.x
    Beautiful Soup 4
    Selenium
    Chrome Web Driver
    

Installation

    Clone this repository to your local machine
    Install required packages by running pip install -r requirements.txt
    Download and install Chrome Web Driver from here and save it in a directory on your local machine
   

Usage
scrap.py

scrap.py allows users to scrape text from a website and save it to a file. To use scrap.py, follow these steps:

    Open scrap.py in a text editor of your choice
    Replace the url variable with the URL of the website you want to scrape
    Replace the output_file variable with the name of the file you want to save the scraped text to
    Run python scrap.py

translators.py

translators.py allows users to translate text scraped from a website into multiple languages using Google Translate API. To use translators.py, follow these steps:

    Open translators.py in a text editor of your choice
    Replace the input_file variable with the name of the file containing the scraped text you want to translate
    Replace the output_directory variable with the name of the directory you want to save the translated files to
    Replace the languages list with the languages you want to translate the text into
    Run python translators.py

Credits

This project was created by Michael Leli.
