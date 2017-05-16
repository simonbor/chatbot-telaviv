# coding=utf-8
# imports here
import csv
from random import randint
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet
from sklearn.feature_extraction import stop_words
from nltk.stem import WordNetLemmatizer


class Review(object):
	def __init__(self, review_text, stars=None):
		"""
		The Review class will include all the functionality we need for analyzing reviews.
		:param review_text:
		:param stars:
		"""

		# self.review is a class attribute & should store what the clean_text method returns
		self.review = self.clean_text(review_text)

		# self.review_sentiment is a class attribute & should store what the convert_stars method returns
		self.review_sentiment = self.convert_stars(stars)

		# self.stop_words is a class attribute & should store the stop words from both lists or whichever you want
		self.stop_words = set(stopwords.words('english')) | set(stop_words.ENGLISH_STOP_WORDS)

		# store results of lemmatizing process into a class variable, since it is in the init function it is automatic!
		self.lemmatized_review = self.lemmatize()  # list

	def clean_text(self, review_text):
		"""
		This method should replace the string â€œ...\nMoreâ€ if it appears in the review_text & replace it with a blank
		string. Then fix the encoding.

		Strings have two useful methods:
			1)   .replace(unwanted_str, wanted_str)
			2)   .decode('utf-8')

		:param review_text: str
		:return: str cleaned of junk
		"""

		return review_text.replace("...\nMore", "").decode('utf-8')

	def convert_stars(self, stars):
		"""
		This method should implement the following logic:
			if the stars variable isnâ€™t None  & if stars is greater than or equal to 3, return an integer 1
			if the stars variable isnâ€™t None  & if stars is less than 3, return an integer 0
			otherwise, return None

		:param stars: int
		:return: int or None
		"""

		if stars is not None:
			if stars >= 3:
				return 1
			else:
				return 0
		else:
			return None

	def wordnet_conversion(self, tag):
		"""
		This method will take a tag from the pos_tag function and convert it to a word net POS. NLTK is a lil
		disorganized like this but ma laasot.

		:param tag: str
		:return: wordnet.POS
		"""

		# if it has a noun tag
		if tag in ['NN', 'NNS', 'NNP', 'NNPS']:
			return wordnet.NOUN

		# if it has a verb tag
		elif tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
			return wordnet.VERB

		# if it has an adverb tag
		elif tag in ['RB', 'RBR', 'RBS']:
			return wordnet.ADV

		# if it has an adj tag
		elif tag in ['JJ', 'JJR', 'JJS']:
			return wordnet.ADJ

		# otherwise, whatever it's a noun
		else:
			return wordnet.NOUN

	def lemmatize(self):
		"""
		Put all the lemmas of self.review (not including stop words) into a list.
		:return: list
		"""

		# tokenize the review into words
		tokenized_review = word_tokenize(self.review)

		# find the POS tags
		tags = pos_tag(tokenized_review)

		# initiate the lemmatizer obj
		lemmatizer = WordNetLemmatizer()

		# create an empty list to store the lemmas of the word tokens
		lemmatized_review = []

		# iterate through the word tokens & tags tuples from the pos_tag function (how convenient!)
		for token_tag_tuple in tags:

			# store data in separate variables so it's easier to read
			token = token_tag_tuple[0]
			tag = token_tag_tuple[1]

			# convert the POS tag to a wordnet POS    0:)
			wordnet_pos = self.wordnet_conversion(tag)

			# lemmatize the token with the wordnet POS
			lemma = lemmatizer.lemmatize(token, pos=wordnet_pos)

			# check that the lemma isn't useless by checking in the stop words list we made in the init function!
			if lemma not in self.stop_words:
				lemmatized_review.append(lemma)  # add it to the lemmatized_review list

		return lemmatized_review

	def sentiment_feature_extraction(self, top_words):
		"""
		Takes a list of top words. Checks if each top word is in the lemmatized review. If it is,
		record in a list called features the integer 1, otherwise record 0.

		Example: Say we only look for the 5 most common words across all reviews, and they are
		['bad', 'good', 'horrible', 'amazing', 'cafe']

		we have a review that says ['cafe', 'horrible']
		the features of this review will be [0,0,1,0,1]

		we have a review that says ['cafe', 'amazing', 'location', 'coffee', 'good']
		the features of this review will be [0,1,0,1,1]

		This way as we can see, we can normalize reviews even more and compare reviews of different lengths as well!
		We will be looking for the 3000 most common words

		:param top_words: list or set of the top words in a corpus
		:return: list
		"""

		# empty list to store the features
		features = []

		# checks each word in top_words if it is in the lemmatized review
		for word in top_words:

			# if it is, store the corresponding feature as 1
			if word in self.lemmatized_review:
				features.append(1)

			# otherwise, store the corresponding feature as 0
			else:
				features.append(0)

		return features

	def predict_sentiment(self):
		"""
		If a review does not come with a
		In the future this section will use a ML model to predict
		negative:0 or positive:1 sentiment.
		:return: a randomly generate a number between 0 and 1
		"""
		sentiment = randint(0, 1)

		return sentiment

	def store_review(self):
		"""
		store self.review in a csv file called submitted_cafe_reviews.csv

		In the future, this section will provide extra data for a ML model!
		"""
		file_location = 'submitted_cafe_reviews.csv'

		with open(file_location, 'ab') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow([self.review])


# Once you are done coding the above class, test it out by running it in the console
# It should print out the first 5 reviews and their sentiment (0 or 1)
# When it passes this test, please delete these comments and this main section below :)
if __name__ == '__main__':

	rows = []
	with open("cafe_reviews.csv") as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			rows.append(row)

	for i in rows[1:5]:
		review = Review(i[1], int(i[2]))
		print review.review, review.review_sentiment