#Importing dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import pymongo
import requests




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
    html = browser.html
    soup = bs(html, 'lxml')

    # getting the title and summary paragraph
    title = soup.find_all("div", class_="content_title")[1].text
    p = soup.find_all("div", class_="article_teaser_body")[0].text


    # visiting site to scrape image
    url = "https://www.jpl.nasa.gov/spaceimages/details.php?id=PIA22109"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "lxml")


    #getting img link 
    image = soup.find_all("div", class_="img")[0].img["src"]
    image_url = f'https://www.jpl.nasa.gov{image}'

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
    h_imgs = []

    #getting titles 
    ht = soup.find_all("h3")

    for t in ht:
    
        #creating dict to hold titles and urls 
        h_dict = {}
        title = t.text.strip()
        browser.click_link_by_partial_text(title)
    
        #adding to dict and making a list of dicts
        h_dict["title"] = title
        h_dict["img_url"] = browser.find_by_text("Sample")["href"]
        h_imgs.append(h_dict)
    
        # return to web page
        browser.visit(url)
    
    h_imgs

    # store to mars_dict
    mars_data["title"] = title
    mars_data["Summary"] = p
    mars_data["featured_image"] = image_url
    mars_data["mars_fact_table_html"] = mars_info
    mars_data["hemisphere_image_urls"] = h_imgs

    browser.quit()
    
    return mars_data
    
