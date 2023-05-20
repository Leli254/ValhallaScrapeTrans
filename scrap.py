import codecs
import re
import os
import requests
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from webdriver_manager.chrome import ChromeDriverManager


# Set up the Selenium driver / create a webdriver object
options = webdriver.ChromeOptions()
options.binary_location = '/usr/bin/google-chrome'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Load the home page
driver.get("https://www.classcentral.com/")

# Wait for the page to fully load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

# Click the "Courses" button to open the navigation menu
nav_trigger_container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-name='MAIN_NAV_TRIGGER_CONTAINER']")))
nav_trigger = nav_trigger_container.find_element(By.CSS_SELECTOR, "button[data-name='LARGE_UP_MAIN_NAV_TRIGGER']")
nav_trigger.click()

# Wait for the navigation menu to fully load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "main-nav-dropdown__index")))

# Find all the links in the navigation menu
links = driver.find_elements(By.CSS_SELECTOR, ".main-nav-dropdown__index a")





# Define a function to save a page's HTML, along with any resources it uses
def save_page(driver, url):
    # Load the page
    driver.get(url)
    # Wait for the page to fully load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    # Get the HTML of the page
    html = driver.page_source
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    # Find all the resources (images, CSS, and JavaScript) used by the class central website
    resources = []
    for element in soup.find_all(["img", "link", "script"]):
        # Ignore any elements that don't have a src or href attribute
        if "src" not in element.attrs and "href" not in element.attrs:
            continue
        # Get the URL of the resource
        if "src" in element.attrs:
            resource_url = element["src"]
        else:
            resource_url = element["href"]
        # Ignore any resources that are already absolute URLs
        if urlparse(resource_url).scheme != "":
            continue
        # Construct the absolute URL of the resource
        base_url = urlparse(url).scheme + "://" + urlparse(url).hostname
        #resource_url = base_url + resource_url
        resource_url = base_url + "/" + resource_url

        # Add the resource to the list
        resources.append(resource_url)
    # Save the HTML and resources to disk
    filename = re.sub(r"[^\w]+", "-", url) + ".html"
    with codecs.open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    for resource_url in resources:
        resource_filename = os.path.basename(urlparse(resource_url).path)
        

        with open(resource_filename, "wb") as f:
            f.write(requests.get(resource_url).content)
        time.sleep(5)

   
    # Find all the links in the dropdown menu
    nav_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".main-nav-dropdown")))
    nav_links = nav_dropdown.find_elements(By.TAG_NAME, "a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

    # Scrape each linked page
    for link in nav_links:
        url = link.get_attribute("href")
        if url is None:
            continue
        if urlparse(url).hostname != "www.classcentral.com":
            continue
        save_page(driver, url)
        time.sleep(5)



# Scrape the home page
save_page(driver, "https://www.classcentral.com/")

# Find all the links on the home page
links = driver.find_elements(By.TAG_NAME, "a")
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

# Scrape each linked page
for link in links:
    url = link.get_attribute("href")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
    if url is None:
        continue
    #if urlparse(url).hostname != "www.classcentral.com":
    if urlparse(url).hostname not in ["www.classcentral.com", "www.classcentral.com/collection"]:
        continue
    save_page(driver, url)
    time.sleep(5)

# Close the driver
driver.quit()






