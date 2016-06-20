import treetaggerwrapper

def main():
	tagger = treetaggerwrapper.TreeTagger(TAGLANG='en', TAGDIR='/home/nak/muga/Downloads/')
	tags = tagger.tag_text(u"I am going to play tennis.")
	#must use unicode string e.g. 'u***'
	for tag in tags:
		print tag


if __name__ == "__main__":
	main()
