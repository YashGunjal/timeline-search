class utils():
	@staticmethod
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

	@staticmethod
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

