from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import json

def remove_spaces(spaces):
    spaces = spaces.strip().replace(" +","")
    spaces = " ".join(spaces.split())
    return spaces

PATH = os.getcwd()
JSON_FILEPATH = os.path.join(PATH,'linkedin_job_finder.json')
if os.path.exists(JSON_FILEPATH) :
    flag = 0
    with open(JSON_FILEPATH, 'r') as f:
        data_master = json.load(f)
else:
    flag = 1
    with open(JSON_FILEPATH, 'w') as fp:
        pass


options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--headless')
driver = webdriver.Chrome(options = options)

data = []

url ="https://www.linkedin.com/jobs/search/?currentJobId=2599978326&jobPostingId=2599472731&pivotType=similarJobs"
driver.get(url)
content = driver.page_source
soup = BeautifulSoup(content, "html.parser")

st_divs1 = soup.find_all('div',{"class" : "base-card base-card--link base-search-card base-search-card--link job-search-card"})
print(len(st_divs1))

for divs in st_divs1 :

    print("*"*20)

    JOBID = ""
    TITLE = ""
    COMPANY = ""
    PLACE = ""
    DATE = ""
    LINK = ""
    DESCRIPTION = ""
    JOB_FUNCTION = ""
    EMPLOYMENT_TYPE = ""
    INDUSTRIES = ""

    job_id = divs['data-entity-urn'].split(':')[-1]
    job_id = remove_spaces(job_id)
    print(job_id)
    JOBID = job_id

    links = divs.find('a',{"class" :"base-card__full-link"})['href']
    links = remove_spaces(links)
    print(links)
    LINK = links

    title = divs.find('h3',{"class" : "base-search-card__title"}).text
    title = remove_spaces(title)
    print(title)
    TITLE = title

    company = divs.find('h4',{"class" : "base-search-card__subtitle"}).text
    company = remove_spaces(company)
    print(company)
    COMPANY = company

    location = divs.find('span',{"class" : "job-search-card__location"}).text
    location = remove_spaces(location)
    print(location)
    PLACE = location

    try :
        date_time = divs.find('time',{"class" : "job-search-card__listdate--new"})['datetime']
        date_time = remove_spaces(date_time)
        print(date_time)
        DATE = date_time

    except Exception as e :
        print(e)
        pass


    driver.get(links)
    content = driver.page_source
    soup_1 = BeautifulSoup(content, "html.parser")
    time.sleep(3)
    
    try :
        description = soup_1.find('div',{"class" : "show-more-less-html__markup"}).text
        description = remove_spaces(description)
        print(description)
        DESCRIPTION = description

    except Exception as e :
        print(e)
        pass

    try :
        info_div = soup_1.find_all('li',{"class" : "description__job-criteria-item"})
        for info in info_div :
            employment_type = remove_spaces(info.find('h3').text)
            employment_desc = remove_spaces(info.find('span').text)
            print(employment_type,employment_desc)
            if 'employment' in employment_type.lower() :
                EMPLOYMENT_TYPE = employment_desc
            elif 'job' in employment_type.lower() :
                JOB_FUNCTION = employment_desc
            elif 'industries' in employment_type.lower() :
                INDUSTRIES = employment_desc

    except Exception as e:
        print(e)
        pass

    scraper_data = {}
    scraper_data['job_id'] = JOBID
    scraper_data['title'] = TITLE
    scraper_data['company'] = COMPANY
    scraper_data['place'] = PLACE
    scraper_data['date'] = DATE
    scraper_data['link'] = LINK
    scraper_data['description'] = DESCRIPTION
    scraper_data['job_function'] = JOB_FUNCTION
    scraper_data['employment_type'] = EMPLOYMENT_TYPE
    scraper_data['industries'] = INDUSTRIES
    data.append(scraper_data)

if data == [] :
    raise Exception('The data object is empty . Please run the Python File once again ')

if flag == 0 :
    for x in data :
        if x not in data_master:
            data_master.append(x)

    seen = []
    for x in data_master:
        if x not in seen:
            seen.append(x)

    with open(JSON_FILEPATH,'w') as file :
        json.dump(seen,file,ensure_ascii=False, indent=1)

elif flag == 1 :
    with open(JSON_FILEPATH,'w') as file :
        json.dump(data,file,ensure_ascii=False, indent=1)

driver.quit()
