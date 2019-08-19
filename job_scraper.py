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

job_titles = []
company_names = []
locations = []
job_summaries = []

def getJobTitles(soup):
	#Each job posting is nested inside of a <div> with class="row result"
	#Trying to pull job titles:
	#1. Pull out <div class="row result">
	#2. Pull out <div class="title">
	#3. Pull out <a title=(title)>
	global job_titles
	for outter_div in soup.find_all(name='div', attrs={"class":["row", "result"]}):
		for inner_div in outter_div.find_all(name='div', attrs={"class": "title"}):
			for a in inner_div.find_all(name="a", attrs={"class":"jobtitle"}):
				job_titles.append(a.get_text().strip())

def getCompanyNames(soup):
	#Getting company name:
	#1. Pull out <div class="row result">
	#2. Pull out <div class="sjcl">
	#3. Pull out <span class="company">
	global company_names
	for outter_div in soup.find_all(name='div', attrs={"class":["row",'result']}):
		for inner_div in outter_div.find_all(name="div", attrs={"class":"sjcl"}):
			company_name = inner_div.find(name="span", attrs={"class":"company"}).get_text().strip()
			company_names.append(company_name)

def getLocations(soup):
	#Getting locations:
	#1. Pull out <div class="row result">
	#2. Pull out <div class="sjcl">
	#3. Pull out <div class="location">
	global locations
	for outter_div in soup.find_all(name='div', attrs={"class":["row","result"]}):
		for inner_div in outter_div.find_all(name="div",attrs={"class":"sjcl"}):
			location = inner_div.find(name="div",attrs={"class":"location"})
			if location:
				locations.append(location.get_text().strip())
			else:
				location = inner_div.find(name="div",attrs={"data-rc-loc":True}).next_sibling.next_sibling.text
				locations.append(location.strip())


def getJobLinks(soup):
	job_links = []
	for outter_div in soup.find_all(name='div', attrs={"class":["row","result"]}):
		for inner_div in outter_div.find_all(name='div', attrs={"class": "title"}):
			job_link = inner_div.a.get('href')
			job_links.append("https://ca.indeed.com"+job_link)
	return job_links

def getJobSummary(URL):
	page = requests.get(URL)
	soup = BeautifulSoup(page.text, 'html.parser')
	job_summary = soup.find(name='div', attrs={"id":"jobDescriptionText"}).get_text().lower()
	return job_summary

def main():
	df = pd.DataFrame(columns=['job_title','company','location','job_summary'])

	for i in range(10):
		print("working...")
		URL = 'https://ca.indeed.com/jobs?q=data+scientist&l=toronto&start=' + str(i*10)
		page = requests.get(URL)
		soup = BeautifulSoup(page.text, 'html.parser')
		getJobTitles(soup)
		getLocations(soup)
		getCompanyNames(soup)
		job_links = getJobLinks(soup)
		global job_summaries
		for job_link in job_links:
			job_summaries.append(getJobSummary(job_link))

	df.job_title = job_titles
	df.company = company_names
	df.location = locations
	df.job_summary = job_summaries
	df.to_csv('./data/jobs.csv')

if __name__ == '__main__':
	main()



