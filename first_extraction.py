import re
import argparse
import pandas as pd
import lxml.etree as etree


parser = argparse.ArgumentParser() #gets the file name from the command line
parser.add_argument('file', type = str)
args = parser.parse_args()

print(args.file+" is being controlled") #print which file is being controlled

tree = etree.parse(args.file)

data = []

for element in tree.iter("*"):
	if "{http://www.w3.org/XML/1998/namespace}lang" in element.attrib: #if there is a xml:lang attribute take the element, if not pass
		metadata_value = re.sub(r' at 0.+$', '', str(element)) #takes the value of the metadata and it cleans it a little
		lang = str(element.attrib).replace("{http://www.w3.org/XML/1998/namespace}", "") #takes the language and clean the data
		metadata_text = element.text #takes the text of the element
		dictionary = {"metadata_value":metadata_value, "lang":lang, "metadata_text" : metadata_text} #populate the dictionary for the dataframe
		data.append(dictionary)

df = pd.DataFrame(data) #create the dataframe

print(df)

df.to_pickle("data_first_extraction.pkl")
