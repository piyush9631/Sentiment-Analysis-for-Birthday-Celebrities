from selenium import webdriver
from bs4 import BeautifulSoup as bs
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import codecs
from string import punctuation
driver = webdriver.Chrome()
driver.get("http://m.imdb.com/feature/bornondate")
html = driver.page_source
driver.close()
soup = bs(html, 'lxml')
name = []
image = []
profession = []
bestwork = []
for i in soup.findAll("span",{"class","lister-item-index unbold text-primary"})[:10]:
    name.append(i.find_next_sibling().get_text()[:-1])
    image.append(i.find_parent().find_parent().find_previous_sibling().img["src"])
    a,b=i.find_parent().find_next_sibling().get_text().split("|")
    profession.append(a[26:-1])
    bestwork.append(b[2:-2])
    


# In[2]:


class tweetSearchAndAnalysis():
    ckey = 'RhXU0VWFCU3jIT4YUClIKuuyc'
    csecret = 'yhIaitf5URHEetbbStTQVNGkDNgQqRbyZv5suKelfHVqo0DGxm'
    atoken = '880759723519352832-EpLdxd2LXtDbaNnKnkAEIiL5c4gW82l'
    asecret = 'oK0TCsgPNeHkRuYb1MOm4fPtMbticHth7p1OaYMS1Afcx'
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    api = tweepy.API(auth)
    pos_sent = open("positive_words.txt").read()
    positive_words = pos_sent.split('\n')
    neg_sent = open('negative_words.txt').read()
    negative_words = neg_sent.split('\n')

    def tweetSearch(self, celebrityName):

        outFile = codecs.open("testTweets.txt", 'w', "utf-8")
        results = self.api.search(q=celebrityName, lang="en", locale="en", count=100)
        for result in results:
            outFile.write(result.text + '\n')

        outFile.close()

    def posNegCount(self, tweet):

        pos = 0
        neg = 0

        for p in list(punctuation):
            tweet = tweet.replace(p, '')

        tweet = tweet.lower()
        words = tweet.split(' ')
        word_count = len(words)

        for word in words:
            if word in self.positive_words:
                pos = pos + 1
            elif word in self.negative_words:
                neg = neg + 1

        return pos, neg

    def tweetSentimentAnalysis(self):

        tweets = codecs.open("testTweets.txt", 'r', "utf-8").read()
        tweets_list = tweets.split('\n')
        positive_counter = 0
        negative_counter = 0
        for tweet in tweets_list:
            if (len(tweet)):
                p, n = self.posNegCount(tweet)
                positive_counter += p
                negative_counter += n

        if positive_counter > negative_counter:
            return "POSITIVE"

        elif positive_counter < negative_counter:
            return "NEGATIVE"

        else:
            return "NEUTRAL"

c = []

for i in name:
    a = tweetSearchAndAnalysis()
    a.tweetSearch(i)
    c.append(a.tweetSentimentAnalysis())

#print (soup.section.h1.string)

for j in range(len(c)):
    print ((j+1),'\tName = ',name[j],'\n\tImage = ',image[j],'\n\tProfession = ',profession[j],'\n\tBest Work = ',bestwork[j],'\n\tOverall Sentiment on Twitter = ',c[j])

