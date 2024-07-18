import os
from .scrape_functions import *

#imports below for RAG
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings


def developOptions(loc, dur):
    docs, loc, dur = scrapeInitial(loc, dur)

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

    # query = "Provide structured options for a %d day trip to %s" % (dur, loc)

    # query = "provide multiple diverse itinerary options based on this info. split between the options with a *** and a new line"

    # query = """Considering the various 10-day Italy itinerary options suggested in the provided documents, propose several unique travel plans that cater to different interests.
    # Incorporate a mix of popular destinations and lesser-known gems while ensuring a balanced and enjoyable experience. 
    # Provide a brief overview for each itinerary highlighting key locations and activities."""

    query = """ \n \n Considering the various""" + dur + "-day " + loc + """ itinerary options suggested in the provided documents, propose several unique travel plans that cater to different interests.
    Provide a brief overview for each itinerary highlighting key locations and activities.
    Incorporate a mix of popular destinations and lesser-known gems while ensuring a balanced and enjoyable experience.
    Ensure that all day numbers add up to the duration provided

    Format each option as such, changing the hashtags to numbers as required and adding as many lines per option as required: \n
    *** \n
    #. Creative option name (based on places included): \n
    Place name, # days \n
    Place name, # days \n
    *** \n

    """
    #

    retrieved_docs = retriever.invoke(query)

    context = '\n'.join([doc.page_content for doc in retrieved_docs])

    prompt = prompt_template.format(context=context, question=query)

    options = (llm.invoke(prompt)).content

    # print(options)

    # print("\n\n\nwhat option would you like:     ")
    # option_chosen = input()

    # print(saveOptions(options))

    # return saveOptions(options), option_chosen

    return saveOptions(options)


def saveOptions(options):
    split_options = options.strip().split("***")  # Split based on the stars

    options_saved = {}

    for option in split_options:
        lines = option.strip().split('\n')

        if len(lines) > 1:
            # Extract the option number and name
            option_header = lines[0].strip()
            option_number = option_header.split()[0].strip('.')
            option_name = ' '.join(option_header.split()[1:])  # Get the option name after the number

            # Extract the city and duration tuples
            places_durations = []
            for line in lines[1:]:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) == 2:
                        place = parts[0].strip()
                        duration = parts[1].strip()
                        places_durations.append((place, duration))

            # Add the option to the dictionary
            options_saved[f"{option_number}. {option_name}"] = places_durations

    return options_saved


# developOptions()