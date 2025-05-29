
import re


def extract_yt_term(command):
    # define a regular expression pattern to extract song name
    pattern=r'play\s+(.*?)\s+on\s+youtube'
    #use re.search to find a match in the command
    match=re.search(pattern,command,re.IGNORECASE)
    #if a match is found return the extracted song name ;otherwise none
    return match.group(1) if match else None

import re

def remove_words(input_string, words_to_remove):
    # Remove punctuation from the input string
    input_string = re.sub(r'[^\w\s]', '', input_string)
    
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join and return the filtered string
    result_string = ' '.join(filtered_words)
    return result_string
