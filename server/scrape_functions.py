from serpapi import GoogleSearch
import requests
from bs4 import BeautifulSoup
import csv
import praw
import os
#imports above for scraping

#import below for rag document
from langchain.docstore.document import Document

#function to scrape top 20 reddit results 
#and top 20 blogs for a trip to country x for y days

#CHANGED TO MAKE THIS DOCUMENTS FOR AN RAG

def scrapeInitial(loc, dur):
    os.environ['GOOGLE_API_KEY'] = "AIzaSyDAihy560sOWWZAtWvO2lVzNSegMvBHf2w"
    # print('i want to go to: ')
    # loc = input()
    # print('i want to go for these many days: ')
    # dur = input()

    dur = str(dur)

    initEarthLinks = scrapeSERPInitial(loc, dur, "earthtrekkers")
    initKimLinks = scrapeSERPInitial(loc, dur, "kimkim")

    etContent = []

    docs = []

    for link in initEarthLinks:
        etContent = scrapeBlog(link)
        # etContent.append(scrapeBlog(link))
        #make new document for each link
        metadata = {"source": link}
        document = Document(page_content=etContent)
        docs.append(document)

    kimContent = []

    for link in initKimLinks:
        # kimContent.append(scrapeBlog(link))
        kimContent = scrapeBlog(link)
        metadata = {"source": link}
        document = Document(page_content=kimContent)
        docs.append(document)

    #scraped the initial links

    # initItineraryContent = etContent + kimContent #consolidate info

    return docs, loc, dur

    



def scrapeRedditAndBlogs(loc, dur):
    blogLinks, redditLinks = scrapeSERP(loc, dur) #call link scraper, save into blog and reddit links

    redditContent = []

    docs = []

    for rLink in redditLinks:
        # redditContent.append(scrapeReddit(rLink)) #add reddit content to list
        redditContent = scrapeReddit(rLink)
        metadata = {"source": rLink}
        document = Document(page_content=redditContent, metadata=metadata)
        docs.append(document)

    blogContent = []

    for bLink in blogLinks:
        # blogContent.append(scrapeBlog(bLink)) #add blog content to list
        blogContent = scrapeBlog(bLink)
        metadata = {"source": bLink}
        document = Document(page_content=blogContent, metadata=metadata)
        docs.append(document)

    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size = 1000, chunk_overlap = 200, add_start_index = True
    # )
    # #chunk into 1000 character docs, overlap of 200 to not lose important surrounding context
    
    # split_docs = text_splitter.split_documents(docs) #split all docs

    # vectorstore_reddit_blogs = Chroma.from_documents(documents=split_docs, embedding=GoogleGenerativeAIEmbeddings())

    return docs, loc, dur



#function to get the initial links

def scrapeSERPInitial(loc, dur, site_name):

    query = dur + "days in " + loc + " " + site_name

    params = {
        "q": query,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": "4152da1bab98e3c9da74046d8380538574653c93af620c5a3d51b1566c112522",
        "num": 6
    }

    search = GoogleSearch(params)
    results = search.get_dict()['organic_results']

    initialLinks = []

    for r in results:
        initialLinks.append(r['link'])

    return initialLinks


def scrapeSERP(loc, dur):

    query = "what to do in " + loc + "for " + dur + "days blogs?"

    params = {
        "q": query,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": "4152da1bab98e3c9da74046d8380538574653c93af620c5a3d51b1566c112522",
        "num": 5
    }

    search = GoogleSearch(params)
    results = search.get_dict()['organic_results']

    blogLinks = []

    for r in results:
        blogLinks.append(r['link'])

    query = "what to do in " + loc + "for " + dur + "days reddit?"

    params = {
        "q": query,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": "4152da1bab98e3c9da74046d8380538574653c93af620c5a3d51b1566c112522",
        "num": 5
    }

    search = GoogleSearch(params)
    results = search.get_dict()['organic_results']

    redditLinks = []

    for r in results:
        redditLinks.append(r['link'])

    return blogLinks, redditLinks




#reddit scraping praw library to scrape the text from a reddit site


def scrapeReddit(link):

    reddit = praw.Reddit(
        client_id = "VxmaNeTmgzmp8dUA2ttN2A",
        client_secret = "LULEusDdIdJS09FBpSMviarzvuQo2A",
        user_agent = "Mobile-Ad6205"
    )

    sub = reddit.submission(url=link)
    sub.comments.replace_more(limit=None)
    comments = sub.comments.list()

    content = sub.selftext + "\n"

    for comment in comments:
        content += comment.body + "\n"

    with open('siteData', 'w', encoding='utf-8') as file:
        file.write(content)

    return content


#basic bs4 scraping to scrape text from blog 


def scrapeBlog(link):
    # try:
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    tags = soup.find_all('p')

    content = ""

    for tag in tags:
        content += tag.get_text()

    return content
    # except ConnectionError:
    #     print("err with {link}, skipping it")
    # except requests.HTTPError:
    #     print("err with {link}, skipping it")
    # except Exception:
    #     print("err with {link}, skipping it")
    # return ""