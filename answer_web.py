import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

import urllib3 
from bs4 import BeautifulSoup

from duckduckgo_search import DDGS

MODEL_NAME = "deepseek-r1:14b"
EMBEDDING_MODEL = "nomic-embed-text" 
KEYWORD_MODEL = "qwen3:0.6b" #Advice: use as light of a model as possible for this
CHUNK_SIZE = 1000  
CHUNK_OVERLAP = 200

def search_web(question,COMMUNICATION_FILE_LOCATION):

    http = urllib3.PoolManager()

    keywords = ollama.generate(
        model=KEYWORD_MODEL,
        prompt=f"Based on the provided context, generate one to three words for a web search about the topic. Make sure to answer ONLY WITH THE KEYWORD sentance and nothing else. Do not use any special formatting, DO NOT Put the answer in quatation marks "
               f"Context:\n{question}",
    )

    keywords = extract_between_markers(keywords["response"],"<think>", "</think>")

    urls = DDGS().text(keywords, max_results=3)

    content = ""


    for i in urls:
        url = i['href']
        request = http.request('GET', url)
        
        soup = BeautifulSoup(request.data, 'html.parser')
        content = ""
        f=0
        for string in soup.body:      
            if(string.get_text().find("Access Denied") != -1):
                print("THIS LINK IS BROKEN")
                f=1
                break    
            content = content + string.getText()
        
        if(f== 1):
            continue
        
        content = content.replace('\n\n', '')

        answer = answer_query(content, question)

        answer = extract_between_markers(answer,"<think>", "</think>")

        if(answer.find("I don't know") != -1 or answer.find("I dont know") != -1 ):
            print("Searching next query")
            continue

        with open(COMMUNICATION_FILE_LOCATION,"w") as file:
            file.write(f"{answer}" + f"\n Results gotten from: {url}")
            file.close()
        break

    
def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", "! ", "? ", "; ", ", "]
    )


    return splitter.split_text(text)

def get_embeddings(texts):
    embeddings = []

    for text in texts:
        response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=text)
        embeddings.append(response["embedding"])
    
    return np.array(embeddings)

def retrieve_relevant_chunks(query, chunks, embeddings, top_k=3):
    query_embedding = np.array(ollama.embeddings(
        model=EMBEDDING_MODEL, 
        prompt=query
    )["embedding"])
    
    # Big scary algorithm that calculates similairty
    similarities = cosine_similarity([query_embedding], embeddings)[0]
    
    # Get top-k indices - fuck pythons element grabbing system
    top_indices = similarities.argsort()[-top_k:][::-1]
    return [chunks[i] for i in top_indices]


def answer_query(text, question):
    
    chunks = chunk_text(text)

    embeddings = get_embeddings(chunks)
    relevant_chunks = retrieve_relevant_chunks(question, chunks, embeddings)
    
    context = "\n\n".join(relevant_chunks)
    response = ollama.generate(
        model=MODEL_NAME,
        prompt=f"Answer the question using ONLY the provided context. "
               f"Be factual and concise. If unsure, say 'I don't know'.\n\n"
               f"Context:\n{context}\n\nQuestion: {question}",
    )


    return response["response"]


def extract_between_markers(s, start_marker, end_marker):
    start_index = s.find(start_marker)
    if start_index == -1:
        return ''
    
    search_start = start_index + len(start_marker)
    
    end_index = s.find(end_marker, search_start)
    if end_index == -1:
        return ''
    
    content = s[start_index+len(start_marker) : len(start_marker)] + s[end_index+ len(end_marker): len(s)]
    return content
