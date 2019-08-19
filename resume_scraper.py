from selenium import webdriver
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time
import pdb



def main():
	URL = "https://resumes.indeed.com/search?q=data+scientist&l=&searchFields="
	browser = webdriver.Firefox(executable_path="./webdriver/geckodriver")
	browser.get(URL)
	html = browser.page_source
	soup = BeautifulSoup(html,'html.parser')
	results = soup.find_all(name="div", attrs={"class":"rezemp-ResumeDisplaySection"})
	print(results)
	browser.close()

if __name__ == '__main__':
	main()