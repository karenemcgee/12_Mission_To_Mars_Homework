# import modules
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def scrape_all():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    news_title, news_p = scrape_news(browser)
    img_url = scrape_image(browser)
    mars_weather = scrape_weather(browser)
    facts = scrape_facts()
    hemispheres_list = scrape_hemispheres(browser)

    data = {"news_title": news_title,
            "news_p": news_p,
            "featured_image": img_url,
            "weather": mars_weather,
            "facts": facts,
            "hemispheres": hemispheres_list}
    browser.quit()
    return data 

##### NASA MARS NEWS #####

def scrape_news(browser):
    # visit NASA site
    url_nasa = "https://mars.nasa.gov/news/"
    browser.visit(url_nasa)

    time.sleep(1)

    # parse into soup
    html = browser.html
    news_soup = bs(html, "html.parser")

    # scrape news title
    news_title = news_soup.body.find("div", class_='content_title').text
    news_title

    # scrape paragraph text
    news_p = news_soup.body.find("div", class_="article_teaser_body").text
    news_p

    return news_title, news_p


##### JPL MARS SPACE IMAGES - FEATURED IMAGE #####

def scrape_image(browser):
    # visit JPL site
    url_jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_jpl)

    time.sleep(1)

    # click to see full image
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    time.sleep(1)

    # parse full image page into soup
    html_image = browser.html
    image_soup = bs(html_image, "html.parser")

    # find image jpg and add to url
    image_url = image_soup.find("img", class_="fancybox-image")["src"]
    featured_image_url = url_jpl + image_url
    featured_image_url

    return featured_image_url


##### MARS WEATHER #####

def scrape_weather(browser):
    # visit mars weather twitter
    url_twitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_twitter)

    time.sleep(1)

    # parse full image page into soup
    html_twitter = browser.html
    twitter_soup = bs(html_twitter, "html.parser")

    # find first tweet text
    mars_weather = twitter_soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    #mars_weather

    return mars_weather


##### MARS FACTS #####

def scrape_facts(browser):
    # scrape Mars facts
    facts_df = pd.read_html("https://space-facts.com/mars/")[1]
    facts_df.columns = ["Fact", "Measurement"]
    facts_df.set_index("Fact", inplace=True)
    #facts_df

    return facts_df.to_html(classes="table table-striped")


##### MARS HEMISPHERES #####

def scrape_hemispheres(browser):
    # visit usgs astrogeology website
    url_usgs = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_usgs)

    time.sleep(1)

    # parse hemispheres page into soup
    html_usgs = browser.html
    usgs_soup = bs(html_usgs, "html.parser")

    # create list of dictionaries of hemisphere names and image urls
    hemispheres_list = []

    hemi_list = usgs_soup.find("div", class_ = "result-list" )
    hemispheres = hemi_list.find_all("div", class_="item")

    for hemi in hemispheres:
        title = hemi.find("h3").text.strip("Enhanced")
        link_to_click = hemi.find("a")["href"]
        link = "https://astrogeology.usgs.gov/" + link_to_click    
        browser.visit(link)
        html_hemi = browser.html
        hemi_soup = bs(html_hemi, "html.parser")
        downloads = hemi_soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemispheres_list.append({"title": title, "img_url": image_url})
        
    return hemispheres_list



if __name__ == "__main__":
    print(scrape_all())