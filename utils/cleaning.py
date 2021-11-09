import re
import nltk
import string 
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

def case_normalization(text):
    return text.lower()

def remove_whitespace(text):
    return text.strip()

def remove_punctuation(text):
    return re.sub(r'[^\w\s]', ' ', text)

def remove_stopwords(text):
    stop_words = set(stopwords.words("english"))
    res = " ".join([word for word in text.split() if word not in stop_words])
    return res

def remove_unicode(text_unicode):
    text_encode = text_unicode.encode(encoding="ascii", errors="ignore")
    text_decode = text_encode.decode()
    clean_text = " ".join([word for word in text_decode.split()])
    return clean_text

def remove_social_data(text):
    text = re.sub("@\S+", "", text)
    text = re.sub("\$", "", text)
    text = re.sub("https?:\/\/.*[\r\n]*", "", text)
    return text

def stemming(text):
    wordList = text.split(" ")
    stemmer = PorterStemmer()
    stemmedWords = []
    for word in wordList:
        stemmedWords.append(stemmer.stem(word))
    
    return " ".join(stemmedWords)

def lemmatizer(text):
    wordList = text.split(" ")
    lemmatizer = WordNetLemmatizer()
    lemmatizedWords = []
    for word in wordList:
        lemmatizedWords.append(lemmatizer.lemmatize(word))
    
    return " ".join(lemmatizedWords)

def removeStringsWithNumbers(text):
    wordList = text.split(" ")
    my_list = [item for item in wordList if item.isalpha()]
    return " ".join(my_list)

def cleanString(text):
    # text = "    WHAT's GOOD, my dude!!!! Did you buy bananas, apples, oranges \u200c from the store?????"
    text = case_normalization(text)
    text = remove_whitespace(text)
    text = remove_punctuation(text)
    text = remove_unicode(text)
    # text = remove_social_data(text)
    text = remove_stopwords(text)
    text = removeStringsWithNumbers(text)
    # text = lemmatizer(text)
    return text

if __name__ == "__main__":
    cleanString("test")



