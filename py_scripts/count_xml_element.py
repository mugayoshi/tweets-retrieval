import xml.etree.ElementTree as ET
import sys

def main():
	"""
	argvs = sys.argv
	if len(argvs) != 3:
			print 'input must include both file path and name of the element you pick up'
			quit()
	"""
	filepath = '/home/nak/muga/annotated_corpus/twitter/spanish/TASS/general-tweets-train-tagged.xml'
	element_name = argvs[2]
	tree = ET.parse(filepath)
	root = tree.getroot()
	i = 0
	for lemma in root.iter(element_name):
		i = i + 1

	print "there are " + str(i) + " elements in " + filepath

if __name__ == "__main__":
		main()
