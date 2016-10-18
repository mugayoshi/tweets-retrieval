import json
import re
import sys

# from RegularExpressions import 

class Tweet:
    def __init__(self, content):
        self.content = content
        self.tokens_re = self.compile_re()
        self.tokens = self.tokenize()
        self.hashtags = []
        self.parse()

    def __str__(self):
        return self.content
    
    def compile_re(self):
        regex_str = [
            r'<[^>]+>', # HTML tags
            r'(?:@[\w_]+)', # @-mentions
            r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
            r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
            
            r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
            r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
            r'(?:[\w_]+)', # other words
            r'(?:\S)+' # anything else
        ]
    
        return re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)


    def tokenize(self):
        return self.tokens_re.findall(self.content)

    def parse(self):
        hashtag_regex = re.compile("(?:\#+[\w_]+[\w\'_\-]*[\w_]+)")
        for token in self.tokens:
            if hashtag_regex.match(token):
                self.hashtags.append(token.lower()[1:])
            
    def isTagged(self):
        """
        Checks whether the tweet contains hashtags
        """
        return bool(self.hashtags)
        
    def preprocess(self, lowercase=True):
        """
        Returns preprocessed tweet
        """
        tokens = [token.lower() for token in self.tokens]

        html_regex = re.compile('<[^>]+>')
        tokens = [token for token in tokens if not html_regex.match(token)]
        
        mention_regex = re.compile('(?:@[\w_]+)')
        tokens = ['@user' if mention_regex.match(token) else token for token in tokens]
        
        url_regex = re.compile('http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+')
        tokens = ['!url' if url_regex.match(token) else token for token in tokens]
        
        hashtag_regex = re.compile("(?:\#+[\w_]+[\w\'_\-]*[\w_]+)")
        tokens = ['' if hashtag_regex.match(token) else token for token in tokens]
        
        flag = False
        for item in tokens:
            if item=='rt':
                flag = True
                continue
            if flag and item=='@user':
                return ''
            else:
                flag = False
                
        return ' '.join([t for t in tokens if t]).replace('rt @user : ','')


