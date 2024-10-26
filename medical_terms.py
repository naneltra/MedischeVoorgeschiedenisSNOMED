"""
This script loads a csv file with abbrevations and replaces it with written out equivalent.
This will improve annotation quality, the annotation model is setup to not annotate 2 character words.
"""

import typer
import pandas as pd
import re
from tqdm import tqdm
import os
from dotenv import load_dotenv
tqdm.pandas(desc="processing vumc dataextract")

load_dotenv()

model_location = os.getenv('MODEL_PATH')
TERMS = os.getenv('TERMS')
DATA_FILE = os.getenv('DATA_FILE')
PROCESSED_DATA_FILE = os.getenv('PROCESSED_DATA_FILE')


def replace_abbreviations_dataframe(df:pd.DataFrame, abbr_list) -> pd.DataFrame:
    for abbr in tqdm(abbr_list):
        abbreviation = abbr['term']
        replacement = abbr['meaning']
        ignore_case = abbr.get('ignore_case', False)

        flags = re.IGNORECASE if ignore_case else 0

        pattern2 = r'(^|\s){}([.><+-:)]|\s|$)'.format(re.escape(abbreviation))
        # replacement = 'XXX'
        df['diagn_proc'] = df['diagn_proc'].progress_apply(lambda t: re.sub(pattern2,rf'\1{replacement}\2',t,flags=flags))
        
    return df

def load_terms():
    abbreviations_df = pd.read_csv(TERMS,index_col=None)
    abbreviations_df = abbreviations_df.loc[abbreviations_df['status']=='enable']
    return abbreviations_df.to_dict(orient='records')

def load_data():
    df_text = pd.read_csv(DATA_FILE)
    df_text = df_text.loc[~df_text['diagnose'].isna()]
    df_text['diagn_proc'] = df_text['diagnose']
    return df_text


def main():
    abbr_list = load_terms()
    df_text = load_data()

    df_text = replace_abbreviations_dataframe(df_text, abbr_list)
    df_text.to_csv(PROCESSED_DATA_FILE,index=None)


if __name__ == "__main__":
    typer.run(main)
