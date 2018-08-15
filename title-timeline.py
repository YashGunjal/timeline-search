from flask import Flask ,render_template ,request
app = Flask(__name__)
import wikipedia
from gensim.summarization.summarizer import summarize
import wikipedia
import urllib.request
import operator ,re
from utils import utils 

app.jinja_env.cache = {}
def relevant_wiki(text):
  text = text.replace(" ","+")
  results = wikipedia.search(text)
  if results != []:
    page = wikipedia.page(results[0])
    return page.url
  else:
    return "NULL"
   
  
def text2sent(stri):
	stri = stri.replace(" . ",". ")
	stri = stri.replace("\\'s","'s")
	stri = stri.replace("\\xe2\\x80\\x94a","-")
	stri = re.sub( '\s+', ' ', stri).strip()
	noofsent = 0
	sentences = []
	#making patterns to split
	dot = re.compile(r"(\w|\))\.\s")
	colon = re.compile(r'(\w|\))\."\s')
	while True:
		#working with first pattern
		m = dot.search(stri)
		#print(type(m))
		if (m):  
			#print (m)
			index = m.start()+2
			present_cut =stri[:index]
			#looking for second pattern
			colon_index = colon.search(present_cut)
			if colon_index:
				sentences.append(stri[:colon_index.start()+3].strip())
				sentences.append(stri[colon_index.start()+3:index].strip())
				#print(stri[:colon_index.start()+3],colon_index.start())
				noofsent += 1
				#stri = stri[colon_index.start()+3:]
			else:  
				sentences.append(stri[:index].strip())
			noofsent += 1
			stri = stri[index:]
			#print("current strtring",stri)
		else:
			break
	return sentences

def all_text(link):
  
	#Fetching
	page = urllib.request.urlopen(link).read()
	page = str(page)
	#cutting the upper and lower part of wikipedia page just to focus of main content
	try:
		para1 = page.find("</head>")
		#print(para1)
		hinge = page.find('<div id="toc"')
		#print(hinge)
		toc_point = page[:hinge].find('</table',para1)
		#print (toc_point)
		if toc_point != -1:
			para1 = toc_point
		end1 = page.find('<span class="mw-headline" id="References">References',para1 )
		#print(end1)
		page = page[para1+1:end1]
	except Exception:
		pass
	else:
		#extraction
		words = " "
		end = 0
		while(end != -1):
			para = page.find(">",end)
			end = page.find("<",(para + 1))
			word = page[para+1:end]
			if (word != ""):
				if (word[0] != "&"):
					if (word[0] != "\\"):
						words = words +" "+ word
	return(words)

def sent_with_year_dic(list):
  '''Takes list of sentences and outputs list of sentence in chronological order'''
  noofsent = 0
  sentences_with_year = []
  dicty = {}
  get = re.compile(r"[0-9][0-9][0-9][0-9]")
  for sent in list:
    m = get.search(sent)
    if (m):
      n = get.search(sent[m.start()+3:])
      if (n):
        continue
      dicty[sent] = m.group()
      noofsent += 1
      sentences_with_year.append(sent)
  #soting the sentences containing year in chronological order
  import operator
  sorted_year_sent = []
  for key,value in sorted(dicty.items(), key=operator.itemgetter(1)):
    sorted_year_sent.append(key)
    #print(value,key)#uncomment this to have output with year
  return sorted_year_sent
@app.route("/")
def hello_world():
	#return "hello"
	return render_template('temp2.html')
	
@app.route('/results/', methods = ['POST'])
def hellos():
	text1 = request.form['text1']
	#return(render_template("result_show.html", sentences = sent_with_year_dic(text2sent(all_text(relevant_wiki(text1)))),text1 = text1.capitalize()))
	sentences_with_year = sent_with_year_dic(text2sent(all_text(relevant_wiki(text1))))
	all_sent = (" ").join(sentences_with_year)
	return(render_template("result_show.html", sentences = sentences_with_year,text1 = text1.capitalize()))

	
	
	
	
@app.route('/result/', methods = ['POST'])
def hello():
	text1 = request.form['text1']
	text = text1.replace(" ","+")
	#res = wikipedia.page(text)
	page = urllib.request.urlopen("https://en.wikipedia.org/w/index.php?search="+text).read()
	page = str(page)
	#cutting the upper and lower part of wikipedia page just to focus of main content
	try:
		para1 = page.find("</head>")
		#print(para1)
		hinge = page.find('<div id="toc"')
		#print(hinge)
		toc_point = page[:hinge].find('</table',para1)
		#print (toc_point)
		if toc_point != -1:
			para1 = toc_point
		end1 = page.find('<span class="mw-headline" id="References">References',para1 )
		#print(end1)
		page = page[para1+1:end1]
	except Exception:
		pass
	else:
	#extraction
		words = " "
		end = 0
		while(end != -1):
			para = page.find(">",end)
			end = page.find("<",(para + 1))
			word = page[para+1:end]
			#print(end)
			if (word != ""):
				if (word[0] != "&"):
					if (word[0] != "\\"):
						words = words +" "+ word
	words = words.replace(" . ",". ")
	words = words.replace("\\'s","'s")
	words = words.replace("\\xe2\\x80\\x94a","-")
	words = re.sub( '\s+', ' ', words).strip()
	noofsent = 0
	sentences = []
	#making patterns to split
	dot = re.compile(r"(\w|\))\.\s")
	colon = re.compile(r'(\w|\))\."\s')
	while True:
	#working with first pattern
		m = dot.search(words)
		#print(type(m))
		if (m):  
			#print (m)
			index = m.start()+2
			present_cut =words[:index]
			#looking for second pattern
			colon_index = colon.search(present_cut)
			if colon_index:
				sentences.append(words[:colon_index.start()+3].strip())
				sentences.append(words[colon_index.start()+3:index].strip())
				#print(words[:colon_index.start()+3],colon_index.start())
				noofsent += 1
				#words = words[colon_index.start()+3:]
			else:  
				sentences.append(words[:index].strip())
			noofsent += 1
			words = words[index:]
		  #print("current strtring",words)
		else:
			break
	list = sentences
	sentences_with_year = []
	dicty = {}
	get = re.compile(r"[0-9][0-9][0-9][0-9]")
	for sent in list:
		m = get.search(sent)
		if (m):
			n = get.search(sent[m.start()+3:])
			if (n):
				continue
			dicty[sent] = m.group()
			sentences_with_year.append(sent)
    #soting the sentences containing year in chronological order
	import operator
	sorted_year_sent = []
	for key,value in sorted(dicty.items(), key=operator.itemgetter(1)):
		sorted_year_sent.append(key)
		#print(value,key)#uncomment this to have output with year
	all_sent = (" ").join(sorted_year_sent)
    
	#sent_with_year_dic(text2sent(all_text(relevant_wiki(text))))
	return(render_template("result_show.html", sentences = text2sent(summarize(all_sent)) ,text1 = text1.capitalize(),dicty = dicty, result = relevant_wiki(text1)))
	
	
	
	
if __name__ == '__main__':
	app.run(debug = True)
	
