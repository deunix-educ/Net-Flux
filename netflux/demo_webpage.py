#!../.venv/bin/python

from threading import Event
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from flux import tools

service = Service('/usr/local/bin/chromedriver')
settings = tools.yaml_load('urls.yaml')

options = webdriver.ChromeOptions()
chrome_prefs = {}
options.experimental_options["prefs"] = chrome_prefs
options.binary_location = "/usr/bin/chromium"
options.add_argument("--start-fullscreen")
options.add_argument("--disable-infobars")
chrome_prefs["profile.default_content_settings"] = {"javascript": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"javascript": 2}


#options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)
while True:
    try:
        for url in settings.get('urls'):
            print(url)
            driver.get(url)
            Event().wait(settings.get('timeout', 10))
    except Exception as e:
        print(f'\n{e}')
