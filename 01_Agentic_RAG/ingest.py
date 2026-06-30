# Script to load the data
# Script to build the index using minsearch


import requests
from minsearch import Index


def load_faq_data():
    """
    Function to load all faq data

    """
    all_courses_url = "https://datatalks.club/faq/json/courses.json"
    all_courses_response = requests.get(all_courses_url)
    all_courses_response.raise_for_status()
    all_courses_data = all_courses_response.json()



    documents = []
    url_prefix = "https://datatalks.club/faq"

    for course in all_courses_data:
        course_url = url_prefix + course['path']

        # print(course_url)
        course_response = requests.get(course_url)
        course_response.raise_for_status()
        course_data = course_response.json()

        documents.extend(course_data)
    
    return documents


def build_index(documents):
    """
    Function to build the index for the document using minsearch
    
    """
    index  = Index(
    text_fields = ['question', 'section', 'answer'],
    keyword_fields = ['course']
    )

    index.fit(documents)

    return index