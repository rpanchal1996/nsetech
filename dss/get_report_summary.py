import pandas as pd
import requests
import PyPDF2
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

def ticker_from_name(name):
    df = pd.read_csv('static/companylist.csv').dropna()
    return (df.Symbol[process.extractOne(name, choices=df.Name)[2]])

links = pd.read_csv('URLsWithDomains.csv').URL
url = links[0]
r = requests.get(url, allow_redirects=True)  # to get content after redirection
pdf_url = r.url # 'https://media.readthedocs.org/pdf/django/latest/django.pdf'
with open('file_name.pdf', 'wb') as f:
    f.write(r.content)
text = ''
for i in range(fileReader.numPages):
    try:
        text = text + fileReader.getPage(i).extractText()
        text = text + "\n"
    except:
        print("no!")
LANGUAGE = 'english'
parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
summarizer = Summarizer()
summary = summarizer(parser.document, 50)
with open('output.txt', 'w') as file:
    for sentence in summary:
        file.writelines(str(sentence))
        file.writelines("\n")
