from langchain_google_genai import ChatGoogleGenerativeAI
import os
from .scrape_functions import *
from .initial_itinerary import *
import time
from google.api_core.exceptions import ResourceExhausted


def individual_places(selected_itinerary):
    # options_dict, optionChosen = developOptions(loc, dur)

    chosenDetails = selected_itinerary

    itinerary = "***************\n"

    for place_dur in chosenDetails:
        dur = place_dur[1]
        loc = place_dur[0]

        print("Creating itinerary for: \n")
        print(dur + " in " + loc + "\n")

        itinerary += "Details for " + str(dur) + " days in " + str(loc) + "\n"

        itinerary += summarize_content(loc, dur)
        itinerary += "\n***************"

    file = open("Itinerary.txt", "w")

    file.write(itinerary)

    file.close()

    listedItinerary = extract_details(itinerary)

    return listedItinerary #listed out places, restaurants, tips, transportation for each place chosen

    #next step is to take this list and plan out the days according to th enumber of days that were chosen



def summarize_content(loc, dur):
    #gathering general trip info from top 5 reddits/blogs: CHANGE NUMBER!!!

    print("gathering")

    docs, loc, dur = scrapeRedditAndBlogs(loc, dur)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 2000, chunk_overlap = 1000, add_start_index = True
    )

    split_docs = text_splitter.split_documents(docs) #split all docs

    llm = ChatGoogleGenerativeAI(model = "gemini-1.5-flash", temperature=0.2)

    embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"

    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

    vectordb = Chroma.from_documents(split_docs, embeddings)

    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 50})

    prompt_template = PromptTemplate(
        input_variables=['context', 'question'],
        template = 'Context: {context}\n\nQuestion: {question} \n\nAnswer:'
    )

    query = """ \n Considering the various information provided, create a holistic itinerary for a trip to """ +  loc + """ for """ + dur + """ days.  
        Be sure to include every single possible place and attraction to visit within the location.
        Return in the following format:
        bulleted list of all places to visit, bulleted list of all restaurant options, bulleted list of all tips to keep in mind,
        best mode of transporation for this place.
    """

    retrieved_docs = retriever.invoke(query)

    context = '\n'.join([doc.page_content for doc in retrieved_docs])

    prompt = prompt_template.format(context=context, question=query)

    # try:
    #     details = (llm.invoke(prompt)).content
    #     return details
    # except ResourceExhausted:
    #     print("DIDNT WORK!!")
    #     details = ""
    #     return details

    details = llm.invoke(prompt).content
    return details

    # print(details)

    # return details

    # file = open("Itinerary.txt", "w")

    # file.write(details)

    # file.close()


    

def summarizeText(text, addition):
    prompt = text + addition

    os.environ['GOOGLE_API_KEY'] = "AIzaSyDAihy560sOWWZAtWvO2lVzNSegMvBHf2w" #environ var

    llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash', temperature=0.2)

    response = llm.invoke(prompt)

    return response.content


def breakdown_section(section):
    places = []
    restaurants = []
    tips = []
    transportation = []

    lines = section.split("\n")
    current_list = None

    for line in lines:
        line = line.strip()
        if "Places" in line:
            current_list = places
        elif "Restaurant" in line:
            current_list = restaurants
        elif "Tips" in line:
            current_list = tips
        elif "Transporation" in line:
            current_list = transportation
        elif line.startswith("* ") or line.startswith("- "):
            if current_list is not None:
                current_list.append(line[2:])
        elif line and current_list is transportation:
            transportation.append(line)

    return places, restaurants, tips, transportation


def extract_details(info_text):
    sections = info_text.split("***************")[1:]

    itinerary = {}

    for section in sections:
        lines = section.strip().split("\n")
        if lines:
            # Extract the city name from the first line
            city_line = lines[0].strip()
            city_name = city_line.split(" in ")[-1]
            # Extract information for the current city
            section_info = breakdown_section(section)
            # Add to the itinerary dictionary
            if any(section_info):
                #so if all is empty, it won't add entry
                itinerary[city_name] = section_info

    return itinerary




# individual_places()

    
    




