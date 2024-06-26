"""
This script loads a csv file with abbrevations and replaces it with written out equivalent.
This will improve annotation quality, the annotation model is setup to not annotate 2 character words.
"""


import pandas as pd
import re
from tqdm import tqdm
tqdm.pandas(desc="processing vumc dataextract")

# df.to_csv('terms.csv',index=None)
abbreviations_df = pd.read_csv('./data/terms.csv',index_col=None)
abbreviations_df = abbreviations_df.loc[abbreviations_df['status']=='enable']
abbreviations_df.info()

abbr_list = abbreviations_df.to_dict(orient='records')


def replace_abbreviations(text:str, abbreviations_df):
    for abbr in abbr_list:
        abbreviation = abbr['term']
        replacement = abbr['meaning']
        ignore_case = abbr.get('ignore_case', False)

        flags = re.IGNORECASE if ignore_case else 0

        pattern = r'(?=<^|\s|){}(?=[.><+]|\s|$)'.format(re.escape(abbreviation))

        # Replace abbreviations in the column using lambda function
        # df['text'] = df[label].progress_apply(lambda text: re.sub(pattern, replacement, text, flags=flags))
        
        text = re.sub(pattern,replacement, text, flags=flags)

    return text



df_text = pd.DataFrame(['this is a text', 'this is another text'], columns=['text'])
df_text = pd.read_csv('./data/medische_voorgeschiedenis.csv', index_col='db_id', sep='|')
df_text = df_text.loc[~df_text['diagnose'].isna()]

df_text['text'] = df_text['diagnose'].progress_apply(lambda text: replace_abbreviations(text,abbreviations_df))

pattern = r'(?=<^|\s|){}(?=[.><+]|\s|$)'.format(re.escape('re'))
re.sub(pattern, 'XXX', 're Syndroom van Tietze re # bla re', flags=False)

df_dummy = pd.DataFrame(['Syndroom van Tietze re #'],columns=['diagnose'])
df_dummy['text'] = df_dummy['diagnose'].progress_apply(lambda t: replace_abbreviations(t,ab))

replace_abbreviations('Syndroom van MDL Tietze re #',abbr_list)


replace_abbreviations_in_column(df_dummy,'diagnose',abbreviations_df)

df_dummy.head()

d = 'SADASD'
d= d.lower()