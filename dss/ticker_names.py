from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import pandas as pd

def ticker_from_name(name):
    df = pd.read_csv('static/companylist.csv')
    return (df.Symbol[process.extractOne(name, choices=df.Name)[2]])
