"""
This script loads a csv file with abbrevations and replaces it with written out equivalent.
This will improve annotation quality, the annotation model is setup to not annotate 2 character words.
"""

import typer
import pandas as pd
import re
from tqdm import tqdm
tqdm.pandas(desc="processing vumc dataextract")


def replace_abbreviations_dataframe(df:pd.DataFrame, abbr_list) -> pd.DataFrame:
    for abbr in tqdm(abbr_list):
        abbreviation = abbr['term']
        replacement = abbr['meaning']
        ignore_case = abbr.get('ignore_case', False)

        flags = re.IGNORECASE if ignore_case else 0

        pattern2 = r'(^|\s){}([.><+]|\s|$)'.format(re.escape(abbreviation))
        # replacement = 'XXX'
        df['diagn_proc'] = df['diagn_proc'].progress_apply(lambda t: re.sub(pattern2,rf'\1{replacement}\2',t,flags=flags))
        
    return df


def main():
    abbreviations_df = pd.read_csv('./data/terms.csv',index_col=None)
    abbreviations_df = abbreviations_df.loc[abbreviations_df['status']=='enable']

    abbr_list = abbreviations_df.to_dict(orient='records')

    df_text = pd.read_csv('./data/medische_voorgeschiedenis.csv', index_col='db_id', sep='|')
    df_text = df_text.loc[~df_text['diagnose'].isna()]
    df_text['diagn_proc'] = df_text['diagnose']

    df_text = replace_abbreviations_dataframe(df_text[:1000], abbr_list)
    df_text.to_csv('./data/medische_voorgeschiedenis_processed.csv',index=None)


if __name__ == "__main__":
    typer.run(main)
