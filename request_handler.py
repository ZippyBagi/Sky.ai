import sys
from answer import answer
from answer_web import search_web

COMMUNICATION_FILE_LOCATION = "/home/zippy/Scripts/Sky/file.txt"

if(sys.argv[1] == "!w"):
    query = ""
    for i in range(2,len(sys.argv)):
        query+=sys.argv[i] + " "
    search_web(query)
else:
    query = ""

    for i in range(1,len(sys.argv)):
        query+=sys.argv[i] + " "

    answer(query,COMMUNICATION_FILE_LOCATION)