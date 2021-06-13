from flask import Flask
from flask import request, jsonify
import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--headless')
driver = webdriver.Chrome(options = options)

def scraper_google_news():
    
    r = requests.get("https://news.google.com/search?q=nri&hl=en-IN&gl=IN&ceid=IN%3Aen")
    print(r.status_code)
    content = r.text
    soup = BeautifulSoup(content, "html.parser")

    st_divs1 = soup.find_all('div',{"class" : "NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc"})
    print(len(st_divs1))

    data = []

    for i in range(len(st_divs1)) :
        # print('*'*40)
        st_divs = soup.find_all('div',{"class" : "NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc"})[i]
        detail = st_divs.find('h3',{"class" : "ipQwMb ekueJc RD0gLb"}).text
        description = st_divs.find('span',{"class" : "xBbh9"}).text
        date_time = st_divs.find('time',{"class" : "WW6dff uQIVzc Sksgp"})['datetime']
        image = 'https://moonvillageassociation.org/wp-content/uploads/2018/06/default-profile-picture1.jpg'
        try:
            image_url = st_divs.find('img',{"class" : "tvs3Id QwxBBf"})['src']
        except Exception as e:
            print(e)
            pass

        # print(detail,description,date_time,image_url)
        # print('*'*40)

        scraper_data = {}
        scraper_data['details'] = detail
        scraper_data['description'] = description
        scraper_data['date_time'] = date_time
        scraper_data['image_url'] = image_url

        data.append(scraper_data)

        with open('google_news_scraper.json','w') as file :
            json.dump(data,file,ensure_ascii=False, indent=1)
            print("*"*20)

    # print(data)
    return data

def scraper_research_paper(val):

    if val is not None: 
    # PATH = "C:\Program Files (x86)\chromedriver.exe"
        for page_num in range(1,2):

            url = "https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText="+str(val)+"&highlight=true&returnFacets=ALL&returnType=SEARCH&matchPubs=true&pageNumber="+str(page_num)
            driver.get(url)
            data = []
            time.sleep(5)

            content = driver.page_source
            soup = BeautifulSoup(content, "html.parser")
            st_divs_len = soup.find_all('div',{"class" : "List-results-items"})
            print(len(st_divs_len))

            for i in range(len(st_divs_len)):

                TITLE = ''
                PROFILE_URL = ''
                DOI = ''
                PDF_URL = ''
                DOI_URL = ''

                print("*"*20)
                st_divs = soup.find_all('div',{"class" : "List-results-items"})[i]
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

            with open('research_paper_scraper.json','w') as file :
                json.dump(data,file,ensure_ascii=False, indent=1)
            print("*"*20)

        return data

@app.route('/<string:type1>/',methods=['GET','POST'])
def hello_world(type1):
    print(type1)
    if type1 == 'google_news':
        scraper = scraper_google_news()
        return jsonify(scraper)
    elif type1 == 'research_paper':
        keyword = request.args.get('keyword')
        print(keyword)
        scraper = scraper_research_paper(keyword)
        return jsonify(scraper)


if __name__ == '__main__':
    app.run()