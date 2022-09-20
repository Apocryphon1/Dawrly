import pandas as pd
from googletrans import Translator 


df = pd.read_excel("data/B09G9LHDV9.xlsx").to_dict
print (df)


translator = Translator()       
print(df.head())

translations = {}
for column in df.columns:
    unique_elements = df[column].unique()
    for element in unique_elements:

        translations[element] = translator.translate(element).text

df.replace(translations, inplace = True)
# output new excel file
df.to_excel('arabic.xlsx')
