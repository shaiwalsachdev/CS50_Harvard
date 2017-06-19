import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        #Take Two Dictionaries
        posi = {}
        neg = {}
        #Add words to them
        with open(positives) as lines:
            for line in lines:
                if not (line.startswith(";") or line.startswith(" ")):
                    posi[line.strip()] = 1
        
        with open(negatives) as lines:
            for line in lines:
                if not (line.startswith(";") or line.startswith(" ")):
                    neg[line.strip()] = 1
                    
        self.positives = posi
        self.negatives = neg
        

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        #Check each word in text
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        total_score = 0
        #Sum the total score
        for token in tokens:
            token = token.lower()
            if token in self.positives:
                total_score = total_score + 1
            elif token in self.negatives:
                total_score = total_score - 1
            else:
                total_score = total_score + 0
        
        return total_score
