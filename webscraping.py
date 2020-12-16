#pip3 install beautifulsoup4 
#pip3 install requests    
#pip3 install PyYAML
import requests
from bs4 import BeautifulSoup  
import yaml
import os


import time

URL = 'https://www.gsb.stanford.edu/exec-ed/programs?pid=1283113613.1598246549'   
page = requests.get(URL)
print('fetching list of urls.')   
soup = BeautifulSoup(page.content, 'html.parser')  
results = soup.findAll('div', {'class':'program-title'})  
print("found "+str(len(results))+" urls")
#print(results[0].prettify())   
all_data = []

for result in results[1:10]:
    el = result.find('a')
    
    URL = 'https://www.gsb.stanford.edu'+el['href'] 
    page = requests.get(URL)  
    soup = BeautifulSoup(page.content, 'html.parser')  
    obj = dict()
    
    obj['url'] = URL
    
    #start_date #end_date
    try:
        start_date = soup.findAll('h2', {'class':'instance-header'})[0]
        datetxt = str(start_date.findAll(text=True)[2])
        obj['date'] =  datetxt
    except IndexError:
        start_date = soup.findAll('h2', {'class':'instance-header'})[0]
        obj['date'] =  start_date.contents[0]+""
    
    #field-name-title document.getElementsByClassName('field-name-title')[0]
    try:
        faculty_name = soup.findAll('div', {'class':'field-name-title'})[0]
        obj['faculty_name'] = str(faculty_name.find('a').contents[0])
    except IndexError:
        obj['faculty_name'] = 'No Faculty'
    
    #faculty_image document.getElementsByClassName('field-type-image')[0]
    try:
        faculty_image = soup.findAll('div', {'class':'field-type-image'})[0]
        obj['faculty_image'] = faculty_image.find('img')['src']+""
    except IndexError:
        obj['faculty_image'] = 'No Faculty'
    
    #tution-amount Program fees
    try:
        tution_amount = soup.findAll('div', {'class':'tuition-amount'})[0]
        obj['tution_amount'] = tution_amount.contents[0]+""
    except IndexError:
        obj['tution_amount'].tution_amount = 'No Amount'
     
    all_data.append(obj)
    time.sleep(0.5)

print(all_data)
print(yaml.safe_dump(all_data))

fileName = 'assignment1.yaml'
file = os.path.expanduser("Desktop/"+fileName)
print("Your Output file is in Location:"+file)
with open('assignment1.yaml', 'w') as f:
    documents = yaml.dump(all_data, f)
