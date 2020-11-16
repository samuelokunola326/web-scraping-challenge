#Importing dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import pymongo
import requests
import time
import shutil



# activate chrome using webdriver
def act_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)



def web_scrape():

    mars_data = {}
    browser = act_browser()


    # visiting site to scrape new title and paragraph
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, 'lxml')

    

    slide_elem = soup.select_one("ul.item_list li.slide")


    # getting the title and summary paragraph
    title = slide_elem.find("div", class_="content_title").get_text()
    p = slide_elem.find("div", class_="article_teaser_body").get_text()

    
    # visiting site to scrape image
    url = "https://www.jpl.nasa.gov/spaceimages/details.php?id=PIA22109"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "lxml")


    #getting img link 
    image = soup.find_all("div", class_="img")[0].img["src"]
    featured_image_url = f'https://www.jpl.nasa.gov{image}'


    #saving img as img file 
    response = requests.get(featured_image_url, stream=True)
    with open('feature_image_url.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    featured_image_url = 'feature_image_url.png'

    # visiting site to scrape planet facts
    url = "https://space-facts.com/mars/"
    table = pd.read_html(url)

    #putting into data frame and transposing 
    table = table[0].set_index(0).T

    # turning the df into df
    mars_info = table.to_html()



    #using web driver to visit website to get hemisphere images and titles
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "lxml")


    # loop through the links and add the urls
    hemisphere_image_urls = []

    #getting titles 
    ht = soup.find_all("h3")

    for t in ht:
        #creating dict to hold titles and urls 
        img_dict = {}
        htitle = t.text.strip()
        browser.click_link_by_partial_text(htitle)
    
        #adding to dict and making a list of dicts
        img_dict["htitle"] = htitle

        h_img = browser.find_by_text("Sample")["href"]
        response = requests.get(h_img, stream=True)
        with open(f'{htitle}.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

        h_img = f'{htitle}.png'

        img_dict["imgs_url"] = h_img
        hemisphere_image_urls.append(img_dict)
    
        # return to web page
        browser.visit(url)
    
        # h_imgs

    # store to mars_dict
    mars_data["title"] = title
    mars_data["p"] = p
    mars_data["featured_image_url"] = featured_image_url
    mars_data["mars_info"] = mars_info
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()
    
    return mars_data

   
         
    
