import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time
import pdb

#MAIN THINGS TO EXTRACT:
#[_] Job Title
#[_] Company Name
#[_] Location
#[_] Job Summary

def main():
	URL = 'https://ca.indeed.com/jobs?q=data%20scientist&l=toronto'
	#conducting a request of the stated URL above:
	page = requests.get(URL)
	#specifying a desired format of “page” using the html parser - this allows python to read the various components of the page, rather than treating it as one long string.
	soup = BeautifulSoup(page.text, 'html.parser')
	#printing soup in a more structured tree format that makes for easier reading
	# print(soup.prettify())

	#Each job posting is nested inside of a <div> with class="row result"
	#Trying to pull job titles:
	#1. Pull out <div class="row result">
	#2. Pull out <div class="title">
	#3. Pull out <a title=(title)>

	job_titles = []
	for outter_div in soup.find_all(name='div', attrs={"class":["row", "result"]}):
		for inner_div in outter_div.find_all(name='div', attrs={"class": "title"}):
			for a in inner_div.find_all(name="a", attrs={"class":"jobtitle"}):
				job_titles.append(a.get_text().strip())

	#Getting company name:
	#1. Pull out <div class="row result">
	#2. Pull out <div class="sjcl">
	#3. Pull out <span class="company">
	company_names = []
	for outter_div in soup.find_all(name='div', attrs={"class":["row",'result']}):
		for inner_div in outter_div.find_all(name="div", attrs={"class":"sjcl"}):
			company_name = inner_div.find(name="span", attrs={"class":"company"}).get_text().strip()
			company_names.append(company_name)

	#Getting locations:
	#1. Pull out <div class="row result">
	#2. Pull out <div class="sjcl">
	#3. Pull out <div class="location">
	locations = []
	for outter_div in soup.find_all(name='div', attrs={"class":["row","result"]}):
		for inner_div in outter_div.find_all(name="div",attrs={"class":"sjcl"}):
			# pdb.set_trace()
			print(inner_div.get_text)
			location = inner_div.find(name="div",attrs={"class":"location"})
			if location:
				locations.append(location.get_text().strip())
			else:
				location = inner_div.find(name="div",attrs={"data-rc-loc":True}).next_sibling.next_sibling.text
				# pdb.set_trace()
				locations.append(location.strip())

	print(len(job_titles), len(company_names))

	for i in range(len(job_titles)):
		print("{} - {}".format(job_titles[i],company_names[i]))

	pdb.set_trace()


if __name__ == '__main__':
	main()