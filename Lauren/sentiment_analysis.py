# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 14:44:42 2017

@author: ljglass
"""

import csv
import collections
import random
from review import Review
import pandas
import numpy as np


def open_csv(file_location):
	"""

	:param file_location: string
	:return: list of Review objects
	"""

	review_objs = []

	with open(file_location) as csvfile:
		reader = csv.reader(csvfile)
		reader.next()  # skip the header

		for row in reader:
			review = Review(row[1], stars=int(row[2]))  # create Review object and store it in a list
			review_objs.append(review)

	return review_objs


def sort_reviews(review_objs):
	"""

	:param review_objs: list of Review objects
	:return: a list of positive reviews, a list of negative reviews
	"""

	positive_reviews = []
	negative_reviews = []

	# iterate through review objects and separate them into positive/negative lists
	for review_obj in review_objs:
		if review_obj.review_sentiment == 1:
			positive_reviews.append(review_obj)
		else:
			negative_reviews.append(review_obj)

	return positive_reviews, negative_reviews


# find top words from reviews
def find_top_words(review_objs):
	"""

	:param review_objs: list of Review objects
	:return: list of the top 3000 words used
	"""

	all_words = []
	for review_obj in review_objs:
		all_words.extend(review_obj.lemmatized_review)  # extend combines 2 lists

	word_counts = collections.Counter(all_words)  # counter object counts occurances of the words

	return [w[0] for w in word_counts.most_common(3000)]


def find_features(review_objs, top_words):
	"""

	:param review_objs: list of Review objects
	:param top_words: list of top words
	:return:
	"""

	all_features = []

	# iterates through review objects and uses the sentiment_feature_extraction method
	for review_obj in review_objs:
		features = review_obj.sentiment_feature_extraction(top_words)
		all_features.append(features)  # all_features becomes a list of lists

	df = pandas.DataFrame(data=np.array(all_features), columns=top_words)
	return df


def find_labels(review_objs):

	all_labels = []

	# iterate through review objects and pull out the label (review sentiment)
	for review_obj in review_objs:
		label = review_obj.review_sentiment
		all_labels.append(label)

	sr = pandas.Series(data=np.array(all_labels))  # put labels into pandas data series
	return sr


if __name__ == "__main__":

	# get review data from csv file
	review_objs = open_csv("cafe_reviews.csv")

	# separate into positive and negative, allocate correctly for training/testing
	positive_reviews, negative_reviews = sort_reviews(review_objs)
	training_reviews = positive_reviews[:300] + negative_reviews[:300]  # training always must have equal positive/negative
	testing_reviews = positive_reviews[300:] + negative_reviews[300:]

	# get the top words used in the TRAINING REVIEWS, always use this list!!!!
	top_words = find_top_words(training_reviews)

	random.shuffle(training_reviews)  # shuffle :)

	# make the dataframes
	training_features = find_features(training_reviews, top_words)
	training_labels = find_labels(training_reviews)

	# make the dataframes
	testing_features = find_features(testing_reviews, top_words)
	testing_labels = find_labels(testing_reviews)
