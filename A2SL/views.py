from django.shortcuts import render
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from django.contrib.staticfiles import finders
import os
import random
import json

def home_view(request):
	return render(request,'home.html')

def animation_view(request):
	if request.method == 'POST':
		text = request.POST.get('sen', '')
		if not text:
			return render(request,'animation.html',{'words':[],'text':''})
		#tokenizing the sentence
		text = text.lower()
		#tokenizing the sentence
		words = word_tokenize(text)

		tagged = nltk.pos_tag(words)
		tense = {}
		tense["future"] = len([word for word in tagged if word[1] == "MD"])
		tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
		tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
		tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])



		#stopwords that will be removed
		stop_words = set(["mightn't", 're', 'wasn', 'wouldn', 'be', 'has', 'that', 'does', 'shouldn', 'do', "you've",'off', 'for', "didn't", 'm', 'ain', 'haven', "weren't", 'are', "she's", "wasn't", 'its', "haven't", "wouldn't", 'don', 'weren', 's', "you'd", "don't", 'doesn', "hadn't", 'is', 'was', "that'll", "should've", 'a', 'then', 'the', 'mustn', 'i', 'nor', 'as', "it's", "needn't", 'd', 'am', 'have',  'hasn', 'o', "aren't", "you'll", "couldn't", "you're", "mustn't", 'didn', "doesn't", 'll', 'an', 'hadn', 'whom', 'y', "hasn't", 'itself', 'couldn', 'needn', "shan't", 'isn', 'been', 'such', 'shan', "shouldn't", 'aren', 'being', 'were', 'did', 'ma', 't', 'having', 'mightn', 've', "isn't", "won't"])



		#removing stopwords and applying lemmatizing nlp process to words
		lr = WordNetLemmatizer()
		filtered_text = []
		for w,p in zip(words,tagged):
			if w not in stop_words:
				if p[1]=='VBG' or p[1]=='VBD' or p[1]=='VBZ' or p[1]=='VBN' or p[1]=='NN':
					filtered_text.append(lr.lemmatize(w,pos='v'))
				elif p[1]=='JJ' or p[1]=='JJR' or p[1]=='JJS'or p[1]=='RBR' or p[1]=='RBS':
					filtered_text.append(lr.lemmatize(w,pos='a'))

				else:
					filtered_text.append(lr.lemmatize(w))


		#adding the specific word to specify tense
		words = filtered_text
		temp=[]
		for w in words:
			if w=='I':
				temp.append('Me')
			else:
				temp.append(w)
		words = temp
		probable_tense = max(tense,key=tense.get)

		if probable_tense == "past" and tense["past"]>=1:
			temp = ["Before"]
			temp = temp + words
			words = temp
		elif probable_tense == "future" and tense["future"]>=1:
			if "Will" not in words:
					temp = ["Will"]
					temp = temp + words
					words = temp
			else:
				pass
		elif probable_tense == "present":
			if tense["present_continuous"]>=1:
				temp = ["Now"]
				temp = temp + words
				words = temp


		filtered_text = []
		for w in words:
			path = w + ".mp4"
			f = finders.find(path)
			#splitting the word if its animation is not present in database
			if not f:
				for c in w:
					filtered_text.append(c)
			#otherwise animation of word
			else:
				filtered_text.append(w)
		words = filtered_text;


		return render(request,'animation.html',{'words':words,'text':text})
	else:
		return render(request,'animation.html')

def reflex_view(request):
	# Get list of available ASL words from static files
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	asset_dir = os.path.join(BASE_DIR, 'Asset')
	videos_dir = os.path.join(BASE_DIR, 'Videos')
	
	available_words = []
	
	# Check Asset directory (primary source for static files)
	if os.path.exists(asset_dir):
		for file in os.listdir(asset_dir):
			if file.endswith('.mp4'):
				word = file.replace('.mp4', '')
				# Verify file is accessible via static files
				path = word + ".mp4"
				if finders.find(path):
					available_words.append(word)
	
	# Also check Videos directory and copy to Asset if needed (for development)
	# In production, all videos should be in Asset directory
	if os.path.exists(videos_dir):
		for file in os.listdir(videos_dir):
			if file.endswith('.mp4'):
				word = file.replace('.mp4', '')
				# Check if already in available_words
				if word not in available_words:
					# Try to find via static files
					path = word + ".mp4"
					if finders.find(path):
						available_words.append(word)
	
	# Filter out single letters and keep only meaningful words
	meaningful_words = [w for w in available_words if len(w) > 1 and not w.isdigit()]
	
	# If no words found, provide some defaults
	if not meaningful_words:
		meaningful_words = ['Hello', 'Thank', 'You', 'Good', 'Happy']
	
	# Pass as JSON for JavaScript
	words_json = json.dumps(meaningful_words)
	
	return render(request, 'reflex.html', {'words': meaningful_words, 'words_json': words_json})
