from textblob import TextBlob
import csv

list = []


def headline_sentiment():
    with open('apple_sentiment (1).csv', 'r') as csvfile:
        headreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in headreader:
            print(row)
            text = row[0]
            tb = TextBlob(text)
            print(tb.sentiment.polarity)
            score = float(tb.sentiment.polarity) * (1 - float(tb.sentiment.subjectivity))
            list.append(row[1] + "," + text + "," + str(score))
            with open('apple_final(1).csv','a') as file:
                file.write(row[1] + "," + text + "," + str(score))
                file.write('\n')

headline_sentiment()
print(list)