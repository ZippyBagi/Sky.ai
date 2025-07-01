import ollama
import sys
from answer_web import search_web


MODEL = 'deepseek-r1:14b'

def extract_between_markers(s, start_marker, end_marker):
    start_index = s.find(start_marker)
    if start_index == -1:
        return ''
    
    search_start = start_index + len(start_marker)
    
    end_index = s.find(end_marker, search_start)
    if end_index == -1:
        return ''
    
    content = s[start_index+len(start_marker) : len(start_marker)] + s[end_index+len(end_marker) : len(s)]
    return content


def answer(query, COMMUNICATION_FILE_LOCATION):
    print("working")
    response = ollama.generate(model=MODEL, prompt=f"Answer the question. Be factual and concise. Dont use any fancy formatting. If unsure, say 'I don't know'.Question:\n\n{query}")

    with open(COMMUNICATION_FILE_LOCATION,"w") as file:
       file.write(extract_between_markers(response['response'].replace('\n\n',''), "<think>", "</think>"))
       file.close()
