from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import pdb
import csv

#Login to linkedin
def login(browser):

	username = None
	password = None

	#Grab username and password from csv file
	file = open('./credentials.csv','r')
	reader = csv.reader(file)
	for line in reader:
		username = line[0]
		password = line[1]

	username_field = browser.find_element_by_id("username")
	password_field = browser.find_element_by_id("password")

	username_field.send_keys(username)
	password_field.send_keys(password)

	login_button = browser.find_element_by_class_name("login__form_action_container").find_element_by_xpath("//button")
	login_button.click()
	sleep(2)

#Search linkedin profiles on google and return a list of linkedin urls
def search(browser):
	URL = 'https://www.google.com/'
	search_query = 'site:linkedin.com/in/ AND "data scientist" AND "Toronto"'
	browser.get(URL)
	sleep(3)

	search_field = browser.find_element_by_name('q')
	search_field.send_keys(search_query)
	search_field.send_keys(Keys.RETURN)
	sleep(2)

	# pdb.set_trace()
	linkedin_urls = browser.find_elements_by_class_name('iUh30')
	linkedin_urls = [urls.text for urls in linkedin_urls]

	#Get second page results
	for i in range(2, 6):
		aria_label = '"Page ' + str(i) + '"'
		next_page = browser.find_element_by_xpath('//a[@aria-label={}]'.format(aria_label))
		next_page.click()
		sleep(2)
		urls = browser.find_elements_by_class_name('iUh30')
		linkedin_urls += [url.text for url in urls]

	return linkedin_urls

#Extract information from linkedin profiles
def extract(browser, linkedin_urls):
	#Get the names of the profiles from url
	names = [url.split('/')[-1] for url in linkedin_urls]

	data = {name: {} for name in names}

	#Extract experience data
	users_experiences = []
	for url in linkedin_urls:
		name = url.split('/')[-1]
		experience_section = None
		browser.get(url)
		sleep(2)

		try:
			experience_section = browser.find_element_by_id("experience-section").text
			data[name]['experience'] = experience_section
		except:
			continue

		try:
			education_section = browser.find_element_by_id("education-section").text
			data[name]['education'] = education_section

		except:
			continue

	return data




def main():
	#Use selenium to navigate to linkedin homepage
	URL = "https://www.linkedin.com/login"
	browser = webdriver.Firefox(executable_path="./webdriver/geckodriver")
	browser.get(URL)

	#Log into linkedIn
	login(browser)

	#Search google for linkedin profiles
	linkedin_urls = search(browser)
	
	#Extract information from linkedin profiles
	data = extract(browser,linkedin_urls)
	print(data)
	df = pd.DataFrame.from_dict(data, orient="index")
	df.to_csv("./data/profiles.csv")
	browser.close()

if __name__ == '__main__':
	main()