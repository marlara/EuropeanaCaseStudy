import pandas as pd

df = pd.read_pickle("data_second_selection.pkl")

df["lang"] = df["lang"].str.replace("{'lang': '","").str.replace("'}", "")  #clean the lang column

csv = pd.read_csv("language_check.csv") #read the csv with the list of correct language codes

compare = any(df['lang'].isin(csv["check"])) #check if any of the lang in the first dataset is in the csv

if compare:
	print("No problems with language codes")
	print(df["lang"].drop_duplicates())
else:
	print("There are some unknown language codes")
	print(df["lang"].drop_duplicates())


df_selection = df.sort_values(["lang", "metadata_value"]) #sort by language and metadata type

languages = {}

for k, v in df_selection.groupby('lang'): #create a dictionary based on the language code
	#print(f'{k}')
	#print(v["metadata_text"])
	languages.update({f'{k}':v["metadata_text"]})

for k,v in languages.items():
	v.to_csv("data_europeana."+k, index=False) #create files
	
