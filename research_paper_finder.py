from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import os
import urllib.request
import requests
import json

PATH_PAPER = os.getcwd()
PATH_PAPER = PATH_PAPER + '/Research_Paper/'

if not os.path.isdir(PATH_PAPER) :
    os.mkdir(PATH_PAPER)

options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
# options.add_argument('--headless')
driver = webdriver.Chrome(options = options)

def download_file(download_url, filename):
    r = requests.get(download_url, stream = True)
    filename = PATH_PAPER + f"{filename}.pdf"
    with open(filename,"wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
            # writing one chunk at a time to pdf file
            if chunk:
                pdf.write(chunk)

val = 'machine learning'
# val = input("Enter your value: ") 
val = val.replace(" ","%20")

if val is not None: 
    # PATH = "C:\Program Files (x86)\chromedriver.exe"
    for page_num in range(1,2):

        url = "https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText="+str(val)+"&highlight=true&returnFacets=ALL&returnType=SEARCH&matchPubs=true&pageNumber="+str(page_num)
        driver.get(url)
        data = []
        time.sleep(5)

        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        st_divs_all = soup.find_all('div',{"class" : "List-results-items"})
        print(len(st_divs_all))

        for st_divs in st_divs_all :

            TITLE = ''
            PROFILE_URL = ''
            DOI = ''
            PDF_URL = ''
            DOI_URL = ''

            print("*"*20)
            # st_divs = soup.find_all('div',{"class" : "List-results-items"})[i]
            abstract = st_divs.find('i',{"class" : "icon-caret-abstract color-xplore-blue"})

            if abstract is not None : 

                title = st_divs.find('a').text
                url_profile = st_divs.find('a')['href']
                url_profile = "https://ieeexplore.ieee.org" + url_profile
                print(title,'****',url_profile)
                TITLE = title
                PROFILE_URL = url_profile
                time.sleep(5)

                driver.get(url_profile)
                content = driver.page_source
                soup_doi = BeautifulSoup(content, "html.parser")
                st_divs = soup_doi.find('div',{"class" : "u-pb-1 stats-document-abstract-doi"})
                if st_divs is not None :

                    doi = st_divs.find('a',{"target" : "_blank"}).text
                    DOI = doi
                    print(doi)
                    try : 
                        url_doi = "https://sci-hub.do/" + doi
                        print(url_doi)
                        DOI_URL = url_doi
                        time.sleep(5)

                        r_doi = requests.get(url_doi)
                        content = r_doi.text
                        soup_pdf = BeautifulSoup(content, "html.parser")
                        url_pdf = soup_pdf.find('iframe',{"id" : "pdf"})['src']
                        if 'https' not in url_pdf:
                            url_pdf = "https:" + url_pdf
                        print(url_pdf)
                        PDF_URL = url_pdf
                        # download_file(url_pdf,title)
                    
                    except Exception as e:
                        print(e)
                        pass
                    time.sleep(5)
                    
            scraper_data = {}
            scraper_data['title'] = TITLE
            scraper_data['profile_url'] = PROFILE_URL
            scraper_data['doi'] = DOI
            scraper_data['doi_url'] = DOI_URL
            scraper_data['pdf_url'] = PDF_URL
            print(scraper_data)
            data.append(scraper_data)

        with open('research_paper_scraper_test.json','w') as file :
            json.dump(data,file,ensure_ascii=False, indent=1)
        print("*"*20)

    driver.quit()