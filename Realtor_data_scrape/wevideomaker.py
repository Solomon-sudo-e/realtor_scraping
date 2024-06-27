import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import os
import wget

while True:
    chrome_options = Options()
    # Add any other options you need

    chrome_service = ChromeService(executable_path='insert your chrome driver')
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    driver.get("https://www.wevideo.com/sign-in")

