#AustinJob.py Script to scrap webpage for austin references
import re
import requests
#sUrl = input("URL to search for Austin:")
sUrl = "https://ideagist.com/list-of-startup-accelerators-and-incubators-in-texas-usa/"
print("Searching site: {}".format(sUrl))

#Open website and place text contents into page object
r = requests.get(sUrl)
c = r.content

from bs4 import BeautifulSoup
#Create a soup object
soup = BeautifulSoup(c)

#find the location element on the webpage
main_content = soup.find('td', attrs = {'width':'169'})
content = main_content.find
page = r.text
#Finds all the url's inside of hyperlinks places them in an array
urls = re.findall('href=[\'"]?([^\'" >]+)',page)



cnt = 0
for url in urls:
    print(url)
    cnt+=1
print("Done [{}]".format(cnt))