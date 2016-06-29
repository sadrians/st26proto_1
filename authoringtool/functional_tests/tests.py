from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000/sequencelistings')

assert 'st26protxo - Index' in browser.title