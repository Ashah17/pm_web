# from langchain_google_genai import ChatGoogleGenerativeAI
# import os
# from scrape_functions import *
# from initial_itinerary import *
# import time


# def individual_places():
#     options_dict, optionChosen = developOptions()

#     chosenDetails = options_dict[int(optionChosen)]

#     itinerary = "***************\n"

#     for place_dur in chosenDetails:
#         dur = place_dur[1]
#         loc = place_dur[0]

#         print("Creating itinerary for: \n")
#         print(dur + " in " + loc + "\n")

#         itinerary += "Details for " + str(dur) + " days in " + str(loc) + "\n"

#         itinerary += summarize_content(loc, dur)
#         itinerary += "\n***************"
    
#     file = open("Itinerary.txt", "w")

#     file.write(itinerary)

#     file.close()

#     listedItinerary = extract_details(itinerary)

#     return listedItinerary #listed out places, restaurants, tips, transportation for each place chosen

#     #next step is to take this list and plan out the days according to th enumber of days that were chosen



# def summarize_content(loc, dur):
#     #gathering general trip info from top 5 reddits/blogs: CHANGE NUMBER!!!

#     redditContent, blogContent = scrapeRedditAndBlogs(loc, dur)

#     #TOOK OUT THE DURATION FROM THE LLM BELOW SO ONLY LOC - INVOLVE DUR LATER IN GOOGLE MAPS

#     redditSummaries = ""

#     for r in redditContent:
#         redditSummaries += summarizeText(r, " \n summarize this") #tell llm to summarize the content, add to a huge string
#         redditSummaries += "\n \n \n \n ******** \n \n \n \n"

#     blogSummaries = ""

#     for b in blogContent:
#         blogSummaries += summarizeText(b, " \n summarize this") #tell llm to summarize the content, add to a huge string
#         blogSummaries += "\n \n \n \n ******** \n \n \n \n"

#     finalRSummary = summarizeText(redditSummaries, " \n consolidate all information and keep it detailed")
#     finalBSummary = summarizeText(blogSummaries, " \n consolidate all information and keep it detailed")


#     finalSummary = summarizeText(finalRSummary+finalBSummary, 
    
#     """ \n combine these in the following format for a trip to """ +  loc + """:
#         bulleted list of all places to visit, bulleted list of all restaurant options, bulleted list of all tips to keep in mind,
#         best mode of transporation for this place
#     """)
    
#     print('reddit: \n')
#     print(finalRSummary)
#     print('blog: \n')
#     print(finalBSummary)

#     return finalSummary

#     # file = open("Itinerary.txt", "w")

#     # file.write(finalSummary)

#     # file.close()
    

# def summarizeText(text, addition):
#     prompt = text + addition

#     os.environ['GOOGLE_API_KEY'] = "AIzaSyDAihy560sOWWZAtWvO2lVzNSegMvBHf2w" #environ var

#     llm = ChatGoogleGenerativeAI(model='gemini-pro', temperature=0.9)

#     response = llm.invoke(prompt)

#     return response.content


# def breakdown_section(section):
#     places = []
#     restaurants = []
#     tips = []
#     transportation = []

#     lines = section.split("\n")
#     current_list = None

#     for line in lines:
#         line = line.strip()
#         if "Places" in line:
#             current_list = places
#         elif "Restaurant" in line:
#             current_list = restaurants
#         elif "Tips" in line:
#             current_list = tips
#         elif "Transporation" in line:
#             current_list = transportation
#         elif line.startswith("* ") or line.startswith("- "):
#             if current_list is not None:
#                 current_list.append(line[2:])
#         elif line and current_list is transportation:
#             transportation.append(line)

#     return places, restaurants, tips, transportation


# def extract_details(info_text):
#     sections = info_text.split("***************")[1:]

#     itinerary = {}

#     for section in sections:
#         lines = section.strip().split("\n")
#         if lines:
#             # Extract the city name from the first line
#             city_line = lines[0].strip()
#             city_name = city_line.split(" in ")[-1]
#             # Extract information for the current city
#             section_info = breakdown_section(section)
#             # Add to the itinerary dictionary
#             itinerary[city_name] = section_info

#     return itinerary



# individual_places()

from langchain_google_genai import ChatGoogleGenerativeAI
import os
from scrape_functions import *
from initial_itinerary import *
import time


def individual_places():
    options_dict, optionChosen = developOptions()

    chosenDetails = options_dict[int(optionChosen)]

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

    docs, loc, dur = scrapeRedditAndBlogs(loc, dur)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 2000, chunk_overlap = 1000, add_start_index = True
    )

    split_docs = text_splitter.split_documents(docs) #split all docs

    llm = ChatGoogleGenerativeAI(model = "gemini-pro", temperature=0.2)

    embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"

    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

    vectordb = Chroma.from_documents(split_docs, embeddings)

    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 50})

    prompt_template = PromptTemplate(
        input_variables=['context', 'question'],
        template = 'Context: {context}\n\nQuestion: {question} \n\nAnswer:'
    )

    query = """ \n combine these in the following format for a trip to """ +  loc + """ for """ + dur + """ days :
        bulleted list of all places to visit, bulleted list of all restaurant options, bulleted list of all tips to keep in mind,
        best mode of transporation for this place
    """

    retrieved_docs = retriever.invoke(query)

    context = '\n'.join([doc.page_content for doc in retrieved_docs])

    prompt = prompt_template.format(context=context, question=query)

    # retries = 0

    # while retries < 2:
    #     try:
    #         details = (llm.invoke(prompt)).content
    #     except Exception as e:
    #         retries += 1
    #         if retries >= 2:
    #             raise e
    #         time.sleep(2)

    details = (llm.invoke(prompt)).content

    return details

    # file = open("Itinerary.txt", "w")

    # file.write(details)

    # file.close()


    

def summarizeText(text, addition):
    prompt = text + addition

    os.environ['GOOGLE_API_KEY'] = "AIzaSyDAihy560sOWWZAtWvO2lVzNSegMvBHf2w" #environ var

    llm = ChatGoogleGenerativeAI(model='gemini-pro', temperature=0.2)

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
            itinerary[city_name] = section_info

    return itinerary




# individual_places()

    
    





    
    





    




