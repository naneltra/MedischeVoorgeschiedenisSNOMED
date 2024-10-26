import pandas as pd
from pathlib import Path
import re
from tqdm import tqdm
from vumc import plot_compare, snomed_mapping
import os
from dotenv import load_dotenv
import typer

tqdm.pandas(desc="processing vumc dataextract")
load_dotenv()

#annotated and processed
VOORGESCHIEDENIS_PATH_ANNOTATED = os.getenv('DATA_ANNOTATED_PATH')
VOORGESCHIEDENIS_OUTPUT_PATH = os.getenv('DATA_OUTPUT_PATH')

app = typer.Typer()


##############################################
##      MAP TO HIGH LEVEL SNOMED CONCEPTS
##############################################

def map_to_type(df):
    df['aandoening']=df['concepts'].apply(lambda x: any(map(lambda v: v[3]=='AANDOENING',x)))
    df['bevinding']=df['concepts'].apply(lambda x: any(map(lambda v: v[3]=='BEVINDING',x)))
    df['substantie']=df['concepts'].apply(lambda x: any(map(lambda v: v[3]=='SUBSTANTIE',x)))
    df['verrichting']=df['concepts'].apply(lambda x: any(map(lambda v: v[3]=='VERRICHTING',x)))
    df['persoon']=df['concepts'].apply(lambda x: any(map(lambda v: v[3]=='PERSOON',x)))
    df['beroep']=df['concepts'].apply(lambda x: any(map(lambda v: v[3]=='BEROEP',x)))
    df['lichaamsstructuur']=df['concepts'].apply(lambda x: any(map(lambda v: v[3]=='LICHAAMSSTRUCTUUR',x)))
    df['fysiekobject']=df['concepts'].apply(lambda x: any(map(lambda v: v[3]=='FYSIEK OBJECT',x)))
    df['afwijkendemorfologie']=df['concepts'].apply(lambda x: any(map(lambda v: v[3]=='AFWIJKENDE MORFOLOGIE',x)))

    df.loc[:,'aandoening':'lichaamsstructuur'].sum()

def get_concepts_by_tui(concept_tuples, tui: str):
    f = filter(lambda x: x[3]==tui, concept_tuples)
    return list(map(lambda x: x[0],f))

def get_concepts_for_tui(df):
    df['aandoeningen']=df['concepts'].apply(lambda x: get_concepts_by_tui(x,'AANDOENING'))
    df['substanties']=df['concepts'].apply(lambda x: get_concepts_by_tui(x,'SUBSTANTIE'))
    df['verrichtingen']=df['concepts'].apply(lambda x: get_concepts_by_tui(x,'VERRICHTING'))
    df['lichaamsstructuren']=df['concepts'].apply(lambda x: get_concepts_by_tui(x,'LICHAAMSSTRUCTUUR'))
    df['bevindingen']=df['concepts'].apply(lambda x: get_concepts_by_tui(x,'BEVINDING'))
    df['personen']=df['concepts'].apply(lambda x: get_concepts_by_tui(x,'PERSOON'))
    df['fysiekeobjecten']=df['concepts'].apply(lambda x: get_concepts_by_tui(x,'FYSIEK OBJECT'))
    df['afwijkendemorfologien']=df['concepts'].apply(lambda x: get_concepts_by_tui(x,'AFWIJKENDE MORFOLOGIE'))

def top_20(df):
    df.explode('aandoeningen')['aandoeningen'].value_counts().head(20)
    df.explode('bevindingen')['bevindingen'].value_counts().head(20)
    df.explode('substanties')['substanties'].value_counts().head(20)
    df.explode('verrichtingen')['verrichtingen'].value_counts().head(20)
    df.explode('personen')['personen'].value_counts().head(20)
    df.explode('lichaamsstructuren')['lichaamsstructuren'].value_counts().head(20)
    df.explode('fysiekeobjecten')['fysiekeobjecten'].value_counts().head(20)
    df.explode('afwijkendemorfologien')['afwijkendemorfologien'].value_counts().head(20)


##############################################
##      APPLY SNOMED MAPPING
##############################################

def check_number_exists(set1, set2):
    for snomedId in set1:
        if snomedId in set2:
            return True
    return False

def create_categories_by_snomed_mappings(df: pd.DataFrame):
    dict_mapping = {}
    for k,v in snomed_mapping.snomed_mappings.items():
        dict_mapping[k]= {str(_.conceptId) for _ in v}
        
    for k,v in tqdm(dict_mapping.items()):
        df[k] = df['conceptIds'].progress_apply(lambda x: check_number_exists(x,v))


"""

Results found per categorie using SNOMED mapping


PulmonaalLijden           127744
CardiovasculairLijden     282620
CerebrovasculairLijden    363281
DiabetesMellitus          171135
Dementie                  153634
Nierfalen                 163100
Obesitas                   12833
Parkinson                  23307
Korsakov                   15519
Huntington                  1009


"""


"""
Resultaten zoektermen matlabscript (vertaald naar Python)

PulmonaalLijden           128562
CardiovasculairLijden     273723
CerebrovasculairLijden    358055
DiabetesMellitus          161240
Dementie                  151080
Nierfalen                 159410
Obesitas                   12543
Parkinson                  22946
Korsakov                   15243
Huntington                     1
"""

plot_compare.plot_tiles()


def main():
    # df_text = load_data()

    df = pd.read_parquet(VOORGESCHIEDENIS_PATH_ANNOTATED)
    
    # df = pd.read_csv('./data/output.csv', index_col=None)
    df['concepts'] = df['concepts'].apply(lambda x: list(eval(x)))
    # df.to_parquet('./data/output.parquet.gzip',compression='gzip')
    df['conceptIds'] = df['concepts'].progress_apply(lambda x: {_[1] for _ in x})

    create_categories_by_snomed_mappings(df)

    df.loc[:,'PulmonaalLijden':'Huntington'].sum()

    # dfDiabetesMellitus = df.loc[df['DiabetesMellitus']]
    df.to_csv(VOORGESCHIEDENIS_OUTPUT_PATH,index=None)



if __name__ == "__main__":
    app()
