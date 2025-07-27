import requests
from bs4 import BeautifulSoup
import pandas as pd
import math

def scrap():
    search_part = input("enter search: ").replace(" " , "%20")
    url = 'https://wuzzuf.net/search/jobs/?a=navbg%7Cspbg&q=' + search_part
    response = requests.get(url)
    soup = BeautifulSoup(response.content , 'lxml')

    # pages
    pages = soup.find('li' , {'class':'css-8neukt'})
    pages_lst = pages.text.split()
    pages_number = math.ceil(int(pages_lst[-1]) / int(pages_lst[-3]))

    titles_lst=[]
    link_lst=[]
    companies_lst=[]
    Occupations_lst=[]
    Specs_lst=[]
    counter_page = 0
    while counter_page < pages_number :
        # Read Page content 
        response = requests.get(url+'&start='+str(counter_page))
        soup = BeautifulSoup(response.content , 'lxml')

        # Titles
        titles_tag = soup.find_all('h2' , {'class': 'css-m604qf'})
        for title in titles_tag:
            titles_lst.append(title.text)

        # Link (href)
        for title in titles_tag:
            link_lst.append(title.a['href'])

        # Companies
        companies_tag = soup.find_all('a' , {'class': 'css-17s97q8'})
        for company in companies_tag:
            companies_lst.append(company.text.replace(' -' , ''))

        # Occupations 
        Occupations = soup.find_all('div' , {'class' : 'css-1lh32fc'})
        for Occupation in Occupations:
            Occupations_lst.append(Occupation.text)

        # Specs 
        Specs = soup.find_all('div' , {'class': 'css-y4udm8'})
        for Spec in Specs:
            Specs_lst.append(Spec.text)

        datascarped = {}
        datascarped['Titles'] = titles_lst
        datascarped['Company'] = companies_lst
        datascarped['Occupation	'] = Occupations_lst
        datascarped['Description'] = Specs_lst
        datascarped['Link'] = link_lst

        # next page
        counter_page += 1

    # Create DataFrame
    df = pd.DataFrame(datascarped)

    # Save this in CSV File
    df.to_csv(f'{search_part}.csv'.replace('%20' , ' ') , index= False)
    print("successful Scrapping")



scrap()