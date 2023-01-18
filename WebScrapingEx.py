####################################
#            HTML Pages            #
#          BeautifulSoup           #
####################################

#How to get the HTML
import requests
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://webscraper.io/test-sites/e-commerce/allinone/phones/touch'

page = requests.get(url)
page

soup = BeautifulSoup(page.text, 'lxml')
soup

#find
soup.find('header')

soup.header.attrs

soup.find('div', {'class':'container test-site'})

soup.find('h4', {'class':'pull-right price'})


#find_all - part 1
soup.find_all('h4', {'class':'pull-right price'})[6:]

soup.find_all('a', class_ = 'title')

soup.find_all('p', class_ = 'pull-right')


#find_all - part 2
soup.find_all(['h4','p','a'])

soup.find_all(id = True)

soup.find_all(string = 'Iphone')

import re

soup.find_all(string = re.compile('Nok'))

soup.find_all(string = ['Iphone', 'Nokia 123'])

soup.find_all(class_ = re.compile('pull'))

soup.find_all('p', class_ = re.compile('pull'))

soup.find_all('p', class_ = re.compile('pull'), limit = 3)


#find_all - part 3
product_name = soup.find_all('a', class_ = 'title')
product_name

price = soup.find_all('h4', class_ = 'pull-right price')
price

reviews = soup.find_all('p', class_ = re.compile('pull'))
reviews

description = soup.find_all('p', class_ = 'description')
description


product_name_list = []
for i in product_name:
    name = i.text
    product_name_list.append(name)


price_list = []
for i in price:
    price2 = i.text
    price_list.append(price2)


reviews_list = []
for i in reviews:
    reviews2 = i.text
    reviews_list.append(reviews2)


descriptions_list = []
for i in description:
    descriptions2 = i.text
    descriptions_list.append(descriptions2)

table = pd.DataFrame({'Product Name':product_name_list, 'Description':descriptions_list,
                      'Price':price_list, 'Reviews':reviews_list})


#extracted data from nested HTML tags
boxes = soup.find_all('div', class_ = 'col-sm-4 col-lg-4 col-md-4')[6] 
boxes
  
boxes.find('a').text    
    
boxes.find('p', class_ = 'description').text   
    
box2 = soup.find_all('ul', class_ = 'nav', id = 'side-menu')[0]    
    
box2.find_all('li')[1].text

####################################
#       Scrapping a Table          #
####################################


import requests
from bs4 import BeautifulSoup
import pandas as pd

#Imports the HTML into python
url = 'https://www.worldometers.info/world-population/'
requests.get(url)
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

#Subsets the HTML to only get the HTML of our table needed
table = soup.find('table', class_ = 'table table-striped table-bordered table-hover table-condensed table-list')

#Gets all the column headers of our table
headers = []
for i in table.find_all('th'):
    title = i.text.strip()
    headers.append(title)
    
#Creates a dataframe using the column headers from our table
df = pd.DataFrame(columns = headers)

#gets all our data within the table and adds it to our dataframe
for j in table.find_all('tr')[1:]:
    row_data = j.find_all('td')
    row = [tr.text for tr in row_data]
    length = len(df)
    df.loc[length] = row
    
#exports the data as a csv
df.to_csv('A/File/Path/file_name.csv')

####################################
#       NFL exercice               #
#       Scrapping a Table          #
####################################

import requests
from bs4 import BeautifulSoup
import pandas as pd

#Imports the HTML into python
url = 'https://www.nfl.com/standings/league/2019/reg/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')


#Subsets the HTML to only get the HTML of our table needed
table = soup.find('table', {'summary':'Standings - Detailed View'})

#Gets all the column headers of our table
headers = []
for i in table.find_all('th'):
    title = i.text.strip()
    headers.append(title)

#Creates a dataframe using the column headers from our table
df = pd.DataFrame(columns = headers)

#gets all our data within the table and adds it to our dataframe
for row in table.find_all('tr')[1:]:
    #line below fixes the formatting issue we had with the team names
    first_td = row.find_all('td')[0].find('div', class_ = 'd3-o-club-fullname').text.strip()
    data = row.find_all('td')[1:]
    row_data = [td.text.strip() for td in data]
    row_data.insert(0,first_td)
    length = len(df)
    df.loc[length] = row_data

####################################
#       Car exercice               #
#  Scrapping Multiple pages        #
####################################

import requests
from bs4 import BeautifulSoup
import pandas as pd

#Imports the HTML into python
page = requests.get('https://www.carpages.ca/used-cars/search/?num_results=50&fueltype_id%5b0%5d=3&fueltype_id%5b1%5d=7&p=3')
soup = BeautifulSoup(page.text, 'lxml')
soup

#Creating our dataframe
df = pd.DataFrame({'Link':[''], 'Name':[''], 'Price':[''], 'Color':['']})

counter = 0
#This loop goes through the first 10 pages and grabs all the details of each posting
while counter < 10:
    
    #gets the HTML of all the postings on the page
    postings = soup.find_all('div', class_ = 'media soft push-none rule')

    #grabs all the details for each posting and adds it as a row to the dataframe
    for post in postings:
        link = post.find('a', class_ = 'media__img media__img--thumb').get('href')
        link_full = 'https://www.carpages.ca' +link
        name = post.find('h4', class_ = 'hN').text.strip()
        price = post.find('strong', class_ = 'delta').text
        color = post.find_all('div', class_ = 'grey l-column l-column--small-6 l-column--medium-4')[1].text.strip()
        df = df.append({'Link':link_full, 'Name':name, 'Price':price, 'Color':color}, ignore_index = True)
    
    #grabs the url of the next page
    next_page = soup.find('a', class_ = 'nextprev').get('href')
    
    #Imports the next pages HTML into python
    page = requests.get(next_page)
    soup = BeautifulSoup(page.text, 'lxml')
    counter += 1

####################################
#         JavaScript WebPages      #
#            Selenium              #
####################################

#Starts up our Driver and loads up our starting webpage
#Ctrl F to check xPath on inspect page to check at div level

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('C:/Web Scraping course/chromedriver.exe')

driver.get('https://www.google.com/')

#inputting text into a box
box = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
box.send_keys('web scraping')
box.send_keys(Keys.ENTER)


#clicking on a button
button = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[3]/center/input[1]')
button.click()
link = driver.find_element_by_xpath('//*[@id="rso"]/div[3]/div/div[1]/a/h3').click()
data_scraping = driver.find_element_by_xpath('//*[@id="mw-content-text"]/div[1]/p[1]/a[1]').click()


#taking a screenshot
driver.save_screenshot('C:\Web Scraping course\screenshot.png')
driver.find_element_by_xpath('//*[@id="rso"]/div[3]/div/div[1]/a/h3').screenshot('C:\Web Scraping course\screenshot2.png')

#full example - uses inputting text into a box, clicking on a button, and taking a screenshot
driver = webdriver.Chrome('C:/Web Scraping course/chromedriver.exe')
driver.get('https://www.google.com/')
box = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
box.send_keys('giraffe')
box.send_keys(Keys.ENTER)
driver.find_element_by_xpath('//*[@id="hdtb-msb-vis"]/div[2]/a').click()
driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[3]/a[1]/div[1]/img').screenshot('C:\Web Scraping course\giraffe.png')

#self scrolling
#Return the height of the document
driver.execute_script('return document.body.scrollHeight')
driver.execute_script('window.scrollTo(0,6000)')
while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')


#wait times
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_condition as EC
import time

box = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
box.send_keys('giraffe')
box.send_keys(Keys.ENTER)
time.sleep(3)
driver.find_element_by_xpath('//*[@id="hdtb-msb-vis"]/div[2]/a').click()

element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'cntratet')))

####################################
#         Infinite scrolling       #
####################################

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

#Starts the driver and goes to our starting webpage
driver = webdriver.Chrome(
        'C:/Web Scraping course/chromedriver.exe')

driver.get('https://www.nike.com/ca/w/sale-3yaep')

#Will keep scrolling down the webpage until it cannot scroll no more
#Get Current page Height
last_height = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(3)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    last_height = new_height

#Imports the HTML of the webpage into python  
soup = BeautifulSoup(driver.page_source, 'lxml')

#grabs the HTML of each product
product_card = soup.find_all('div', class_ = 'product-card__body')

#Creates a dataframe
df = pd.DataFrame({'Link':[''], 'Name':[''], 'Subtitle':[''], 'Price':[''], 'Sale Price':['']})

#Grabs the product details for every product on the page and adds each product as a row in our dataframe
for product in product_card:
    try:
        link = product.find('a', class_ = 'product-card__link-overlay').get('href')
        name = product.find('div', class_ = 'product-card__title').text
        subtitle = product.find('div', class_ = 'product-card__subtitle').text
        full_price = product.find('div', class_ = 'product-price css-1h0t5hy').text
        sale_price = product.find('div', class_ = 'product-price is--current-price css-s56yt7').text
        df = df.append({'Link':link, 'Name':name, 'Subtitle':subtitle, 'Price':full_price, 'Sale Price':sale_price},
                       ignore_index = True)
    except:
        pass

#exports the dataframe as a csv
df.to_csv('A/File/Path/file_name.csv')

####################################
#             Exercice             #
#         Infinite scrolling       #
####################################

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

#Starts the driver and goes to our starting webpage
driver = webdriver.Chrome(
    'C:/Web Scraping course/chromedriver.exe'
)

driver.get('https://store.unionlosangeles.com/collections/outerwear')

#Will keep scrolling down the webpage until it cannot scroll no more
last_height = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(3)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if last_height == new_height:
        break
    last_height = new_height

#Imports the HTML of the webpage into python      
soup = BeautifulSoup(driver.page_source, 'lxml')

#Grabs the section of the HTML that has all our products
section = soup.find('div', {'id':'main', 'role':'main'})

#grabs the HTML of each product
postings = section.find_all('li')

#Creates a dataframe
df = pd.DataFrame({'Link':[''], 'Vendor':[''],'Title':[''], 'Price':['']})

#Grabs the product details for every product on the page and adds each product as a row in our dataframe
for post in postings:
    try:
        link = post.find('a').get('href')
        vendor = post.find(class_ = 'cap-vendor').text
        title = post.find(class_ = 'cap-title').text
        price = post.find(class_ = 'cap-price').text
        df = df.append({'Link':link, 'Vendor':vendor,'Title':title, 'Price':price}, ignore_index = True)
    except:
        pass

#fixes the link of the first 4 products on the page    
df['Link'][4:] = 'https://store.unionlosangeles.com'+df['Link'][4:]

####################################
#             Exercice             #
#         Twitter postings         #
####################################

'''
!!!IMPORTANT READ!!!
This code may not work when you run it and it's because one of the classes we called may have changed,
I put a comment below where to expect the error iF there is one and how to fix it
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time

#Starts the driver and goes to our starting webpage
driver = webdriver.Chrome(
        'C:/Web Scraping course/chromedriver.exe')

driver.get('https://twitter.com/login')
time.sleep(2)

#Variable that contains the celebirty or profile our program will scrape
#This program will scrape Ryan Reynolds tweets as indicated in the line below
celebrity = 'Ryan Reynolds'

#inputs an email and password for the login details
login = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[1]/label/div/div[2]/div/input')
login.send_keys('webscrapingbot@gmail.com')
password = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[2]/label/div/div[2]/div/input')
password.send_keys('thisisabot')

#Presses the login button, and creates a wait time to let the home page fully load in
#if your getting an error here just make your browser full screen, it should work then
button = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[3]/div/div').click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div[2]/input')))

#inputs the name from the celebrity variable into the search box and presses enter
search = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div[2]/input')
search.send_keys(celebrity)
search.send_keys(Keys.ENTER)
time.sleep(2)

#Clicks on the people tab which has all the accounts associated with who we searched up
people = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div').click()
time.sleep(2)

#clicks on our celebrities profile
profile = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[1]/div/div/div/div[2]/div[1]/div[1]/a/div/div[1]/div[1]/span').click()
time.sleep(2)

#Imports the HTML of the celebrities profile into python
soup = BeautifulSoup(driver.page_source, 'lxml')

#grabs the HTML of each tweet
#ERROR WARNING! If there is an error try recopying the class attribute here, twitter may have changed it by like one or two letters whcih affects our code
postings = soup.find_all('div', class_ = 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0') 


#This loop will keep scrolling down the webpage loading in and collecting new tweets until we have scraped 100 unique tweets
tweets = []
while True:
    for post in postings:
        tweets.append(post.text)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    #need to change the class here to match it with the other posting variable if there is an error
    postings = soup.find_all('div', class_ = 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
    tweets2 = list(set(tweets))
    if len(tweets2) > 200:
        break

#Subsets our list of tweets to only contain the tweets with a specific word located in it
new_tweets = []    
for i in tweets2:
    #To change that specific word just input into the string below
    if '' in i:
        new_tweets.append(i)


####################################
#             Exercice             #
#         Indeed Job Scrapping     #
####################################

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

#Starts the driver and goes to our starting webpage
driver = webdriver.Chrome(
    'C:/Web Scraping course/chromedriver.exe'
)

driver.get('https://ca.indeed.com/')

#Inputs a job title into the input box
input_box = driver.find_element_by_xpath('//*[@id="text-input-what"]')
input_box.send_keys('data analyst')

#Clicks on the search button
button = driver.find_element_by_xpath('//*[@id="whatWhereFormId"]/div[3]/button').click()

#Creates a dataframe
df = pd.DataFrame({'Link':[''], 'Job Title':[''], 'Company':[''], 'Location':[''],'Salary':[''], 'Date':['']})

#This loop goes through every page and grabs all the details of each posting
#Loop will only end when there are no more pages to go through
while True:  
    #Imports the HTML of the current page into python
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    #Grabs the HTML of each posting
    postings = soup.find_all('div', class_ = 'jobsearch-SerpJobCard unifiedRow row result clickcard')
    
    #grabs all the details for each posting and adds it as a row to the dataframe
    for post in postings:
        link = post.find('a', class_ = 'jobtitle turnstileLink').get('href')
        link_full = 'https://ca.indeed.com'+link
        name = post.find('h2', class_ = 'title').text.strip()
        company = post.find('span', class_ = 'company').text.strip()
        try:
            location = post.find('div', class_ = 'location accessible-contrast-color-location').text.strip()
        except:
            location = 'N/A'
        date = post.find('span', class_ = 'date').text.strip()
        try:
            salary = post.find('span', class_ = 'salaryText').text.strip()
        except:
            salary = 'N/A'
        df = df.append({'Link':link_full, 'Job Title':name, 'Company':company, 'Location':location,'Salary':salary, 'Date':date},
                       ignore_index = True)
    
    #checks if there is a button to go to the next page, and if not will stop the loop
    try:
        button = soup.find('a', attrs = {'aria-label': 'Next'}).get('href')
        driver.get('https://ca.indeed.com'+button)
    except:
        break
   
#The code below just sorts the dataframe by posting date
df['Date_num'] = df['Date'].apply(lambda x: x[:2].strip())

def integer(x):
    try:
        return int(x)
    except:
        return x
    
df['Date_num2'] = df['Date_num'].apply(integer)
df.sort_values(by = ['Date_num2','Salary'], inplace = True)  

df = df[['Link', 'Job Title','Company','Location', 'Salary','Date']]

#exports the dataframe as a csv
df.to_csv('A/File/Path/indeed_jobs.csv')

####################################
#    Sending Email with python     #
####################################


#Code below sends an email to whomever through python
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

#Input the email account that will send the email and who will receiving it
sender = 'account@gmail.com'
receiver = 'account@gmail.com'

#Creates the Message, Subject line, From and To
msg = MIMEMultipart()
msg['Subject'] = 'New Jobs on Indeed'
msg['From'] = sender
msg['To'] = ','.join(receiver)

#Adds a csv file as an attachment to the email (indeed_jobs.csv is our attahced csv in this case)
part = MIMEBase('application', 'octet-stream')
part.set_payload(open('A/File/Path/indeed_jobs.csv', 'rb').read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename ="indeed_jobs.csv"')
msg.attach(part)

#Will login to your email and actually send the message above to the receiver
s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
s.login(user = 'account@gmail.com', password = 'input your password')
s.sendmail(sender, receiver, msg.as_string())
s.quit()
