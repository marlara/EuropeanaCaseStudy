import pandas as pd

df = pd.read_pickle("data_first_extraction.pkl")

test_passed = 0

#First check: multiple languages

multiple_language = df.loc[df['lang'] != "{'lang': 'en'}"] #check if in the column lang there are other languages than the english

if multiple_language is not None:
	print("First check passed: there is more then one language other then english:\n")
	print(multiple_language)
	test_passed +=1
else:
	print("First check passed: there is only the english language")

#Second check: word lenght

totalwords = df['metadata_text'].str.count(' ') + 1 #check che number of words
good_count = all(t < 301 for t in totalwords.astype(int)) #check if all the words are less then 300
if good_count:
	print("Second check: word count less then 300")
	print(totalwords)
	test_passed +=1
else:
	print("Second check: word count more then 300")
	print(totalwords)


#Third check: sentence match

frames = {}

#create different frames grouped by the metadata_value and put them inside a dictionary of dataframes
for k, v in df.groupby((df['metadata_value'].shift() != df['metadata_value']).cumsum()): #see https://towardsdatascience.com/pandas-dataframe-group-by-consecutive-same-values-128913875dba
    #print(f'[group {k}]')
    #print(v)
    frames.update({f'[group {k}]': v}) 

print(frames)

#iterates through the dictionaries and check the sentence count
dict_passed = 0
for k,v in frames.items(): 	
	sentence_list = [] #create a list for the sentences
	for el in v["metadata_text"]:
		sentence_count = el.count('. ') + 1 #count each sentence
		sentence_list.append(sentence_count)
	result = all(sentence == sentence_list[0] for sentence in sentence_list) #check if all the element in the group are the same
	if result:
		print("The sentences match")
		print(sentence_list)
		print(k + el + str(sentence_count))
		dict_passed +=1
	else:
		print("The sentences don't match")
		print(sentence_list)
		print(k + el + str(sentence_count))
if dict_passed == len(frames):
	test_passed +=1


print("Number of test passed "+str(test_passed))

if test_passed == 3: #if all tests are passed
	df.to_pickle("data_second_selection.pkl")