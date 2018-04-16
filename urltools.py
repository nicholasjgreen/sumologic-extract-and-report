import re

exprGuid = re.compile(r'(\{){0,1}[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}(\}){0,1}')
exprFile = re.compile(r'\/[0-9a-zA-Z%!@#$^&*\-_()<>.]*.(pdf|jpg|jpeg|png|tif|bmp|csv|msg|xlsx|xls|docx|doc)$')
exprNumber = re.compile(r'\/(\d+)(\.(\d+))?')

def tidyUrl(url):
    url = url.lower()
    url = exprGuid.sub('<GUID>', url)
    url = exprFile.sub('/<FILE>', url)
    url = exprNumber.sub('/<NUMBER>', url)
    url = url.strip('/')
    return url


def extractUrlParts(url):
    return url.split('/')


def ingestWord(word_counts, word):
    # Skip empty
    if word == '':
        return

    # Add or increase
    if not word in word_counts:
        word_counts[word] = 1
    else:
        word_counts[word] = word_counts[word] + 1



valid_method_set = set(['GET', 'PUT', 'POST', 'DELETE'])

def is_valid_http_method(word):
    return word.upper() in valid_method_set



def feature_name_from_method_and_url_parts(method, parts):
    return '[{}]_{}'.format(method, '/'.join(parts))
