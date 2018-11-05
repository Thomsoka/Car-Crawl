import requests 
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
import csv


fields = [
    ['price', {'itemprop': 'price'}],
    ['CarTitle', {'class': 'title-2323565163'}],
    ['PostDate', {'itemprop': 'datePosted'}],
    ['Location', {'itemtype': 'http://schema.org/PostalAddress'}],
    ['Brand', {'itemprop': 'brand'}],
    ['model', {'itemprop': 'model'}],
    ['year', {'itemprop': 'vehicleModelDate'}]
    #['kilometers', {'itemprop': 'kilometers'}]
]

# Returns detail value based on the 3 parameters

def Soup_Get_Detail(WebPage, attributes):
    Soup1 = BeautifulSoup(WebPage, "lxml")
    value = Soup1.find_all(attrs=attributes)
    if not len(value):
        return 'null'
    else:
        return value[0].contents[0]

#  Function that returns all from html
def Kijiji_Get_All_Details(WebPage):
    result = {}
    for field in fields:
        result[field[0]]= Soup_Get_Detail(WebPage,field[1])
    return result

    
# Now to use the functions
#html = requests.get('https://www.kijiji.ca/v-classic-cars/hamilton/1968-dodge-dart/1392288231?enableSearchNavigationFlag=true').content
#print(Kijiji_Get_All_Details(html))

# Finds all post links based on search page
def Kijiji_Search_Page_GetLinks(WebPageSearch):
    Page1 = requests.get(WebPageSearch).content
    Soup2 = BeautifulSoup(Page1, "lxml")
    links1 = Soup2.find_all(attrs={'class','title enable-search-navigation-flag '})
    post_links = []

    for x in links1:
        bigLink = 'https://www.kijiji.ca' + x.attrs['href']
        post_links.append(bigLink)
    return post_links

Page_Links = Kijiji_Search_Page_GetLinks('https://www.kijiji.ca/b-cars-trucks/ontario/used/page-2/c174l9004a49')

#
def get_page(link):
    html = requests.get(link).content
    return Kijiji_Get_All_Details(html)

with Pool(processes=20) as thread_pool:
    results = thread_pool.map(get_page, Page_Links)

with open('results.csv', 'w+') as result_file:
    writer = csv.DictWriter(result_file, fieldnames=results[0].keys())
    writer.writerows(results)

    