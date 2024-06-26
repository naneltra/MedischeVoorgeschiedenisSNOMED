import pandas as pd
from pathlib import Path
import re
from tqdm import tqdm
from vumc import plot_compare, vumc_mapping, snomed_mapping
from dotenv import load_dotenv
import os

# import importlib
# importlib.reload(snomed_mapping)
# importlib.reload(vumc_mapping)
# importlib.reload(plot_compare)

tqdm.pandas(desc="processing vumc dataextract")
load_dotenv()

##############################################
##      LOAD MEDISCHE VOORGESCHIEDENIS
##############################################

VOORGESCHIEDENIS_PATH = Path('./data/medische_voorgeschiedenis.csv')

def load_voorgeschiedenis(path: Path) -> pd.Dataframe:
    path = VOORGESCHIEDENIS_PATH
    df = pd.read_csv('./data/medische_voorgeschiedenis.csv', delimiter='|')
    return df

df = load_voorgeschiedenis(VOORGESCHIEDENIS_PATH)

# calculate mean document length for batch optimization = 43
df.loc[~df['text'].isna(),'text'].apply(lambda x: len(x)).mean()

df = df.rename(columns={"db_id":"id","diagnose":"text"})
df = df.set_index('id')
df = df.loc[~df['text'].isna()]



##############################################
##      ANNOTATE
##############################################
from medcat.cat import CAT

def data_iterator(data: pd.DataFrame):
    for id, row in data[['text']].iterrows():
        yield (id, str(row['text']))

generator = data_iterator(df)


df['word_count'] = df.loc[~df['diagnose'].isna(),'diagnose'].apply(lambda x: len(x.split(' ')))

# 43 * 8 * 200
batch_size_chars = 68800 

model_location = os.getenv('MODEL_PATH')
mymodel = CAT.load_model_pack(model_location)

results = mymodel.multiprocessing_batch_char_size(generator,  # Formatted data
                                              batch_size_chars = batch_size_chars,
                                              nproc=8)

def get_snomed_results(id: str):
    if id not in results:
        return []
    if 'entities' in results[id]:
        entities_dict = results[id]['entities']
        return [(v['pretty_name'],v['cui'],v['meta_anns']['Negation']['value'],v['type_ids'][0]) for k,v in entities_dict.items()]
    return []

df = pd.read_csv('./data/output.csv',index_col=0)

df['concepts'] = df['concepts'].apply(lambda x: list(eval(x)))

df_backup = df.copy()
df_backup.head()
df = df_backup






##############################################
##      MAP TO HIGH LEVEL SNOMED CONCEPTS
##############################################


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


df['aandoeningen']=df['concepts'].apply(lambda x: get_concepts_by_tui(x,'AANDOENING'))
df['substanties']=df['concepts'].apply(lambda x: get_concepts_by_tui(x,'SUBSTANTIE'))
df['verrichtingen']=df['concepts'].apply(lambda x: get_concepts_by_tui(x,'VERRICHTING'))
df['lichaamsstructuren']=df['concepts'].apply(lambda x: get_concepts_by_tui(x,'LICHAAMSSTRUCTUUR'))
df['bevindingen']=df['concepts'].apply(lambda x: get_concepts_by_tui(x,'BEVINDING'))
df['personen']=df['concepts'].apply(lambda x: get_concepts_by_tui(x,'PERSOON'))
df['fysiekeobjecten']=df['concepts'].apply(lambda x: get_concepts_by_tui(x,'FYSIEK OBJECT'))
df['afwijkendemorfologien']=df['concepts'].apply(lambda x: get_concepts_by_tui(x,'AFWIJKENDE MORFOLOGIE'))


df.explode('aandoeningen')['aandoeningen'].value_counts().head(20)
df.explode('bevindingen')['bevindingen'].value_counts().head(20)
df.explode('substanties')['substanties'].value_counts().head(20)
df.explode('verrichtingen')['verrichtingen'].value_counts().head(20)
df.explode('personen')['personen'].value_counts().head(20)
df.explode('lichaamsstructuren')['lichaamsstructuren'].value_counts().head(20)
df.explode('fysiekeobjecten')['fysiekeobjecten'].value_counts().head(20)
df.explode('afwijkendemorfologien')['afwijkendemorfologien'].value_counts().head(20)








##############################################
##      NORMALISING ABBREVATIONS
##############################################

df['text'] = df['text'].str.replace('##','fracturen')
df['text'] = df['text'].str.replace('#','fractuur')
df['text'] = df['text'].str.replace('=a','is aangevraagd')
df['text'] = df['text'].str.lower()
df['text'] = df['text'].str.strip()
df['text'] = df['text'].str.replace('[^\w\s]',' ',regex=True)

def count_term(txt, abbr: str, ignore_case = False):
    abbr = re.escape(abbr)
    if ignore_case:
        return len(re.findall(rf"\b{abbr}(?:[.><+]|\s|$)",txt, re.IGNORECASE))
    return len(re.findall(rf"\b{abbr}(?:[.><+]|\s|$)",txt))
  

def analyse_term_on_dataset():
    abbreviations_df = pd.read_csv('./terms.csv',index_col=None)
    abbreviations_df = abbreviations_df.loc[abbreviations_df['status']=='enable']
    
    abbr_count = []
    
    for index, row in tqdm(abbreviations_df.iterrows()):
        abbreviation = row['term']
        replacement = row['meaning']
        is_ignore_case = row.get('ignore_case', False)

        abbr_count.append((abbreviation, replacement, df['text'].apply(lambda x: count_term(x, abbreviation,is_ignore_case)).sum()))


    with open('abbr_analyses.txt', 'w') as file:
        for tup in abbr_count:
            file.write(','.join(map(str, tup)) + '\n')
    
    df_abbr_count = pd.DataFrame(abbr_count, columns=['term','meaning','count'])
    df.to_csv('df_abbr_analysis.csv')


def replace_abbreviations_in_column(df, abbreviations_df):

    for index, row in abbreviations_df.iterrows():
        abbreviation = row['term']
        replacement = row['meaning']
        ignore_case = row.get('ignore_case', False)

        # Create regex pattern based on case sensitivity
        flags = re.IGNORECASE if ignore_case else 0
        pattern = r'\b{}\b'.format(re.escape(abbreviation))

        # Replace abbreviations in the column using lambda function
        df['text'] = df['text'].apply(lambda text: re.sub(pattern, replacement, text, flags=flags))

    return df


df_abbr = pd.read_csv('./terms.csv',index_col=None)
df_abbr.to_dict()

df_clean = replace_abbreviations_in_column(df,df_abbr)





##############################################
##      APPLY SNOMED MAPPING
##############################################

df['conceptIds'] = df['concepts'].progress_apply(lambda x: {_[1] for _ in x})

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


create_categories_by_snomed_mappings(df)

df.loc[:,'PulmonaalLijden':'Huntington'].sum()

dfDiabetesMellitus = df.loc[df['DiabetesMellitus']]


"""

Results found per categorie using SNOMED mapping


PulmonaalLijden           111485
CardiovasculairLijden     210754
CerebrovasculairLijden    252201
DiabetesMellitus          140808
Dementie                   98930
Nierfalen                  93306
Obesitas                   12599
Parkinson                  23032
Korsakov                   13449
Huntington                     0


"""


"""
Resultaten zoektermen matlabscript (vertaald naar Python)

PulmonaalLijden            79057
CardiovasculairLijden     205388
CerebrovasculairLijden    122840  
DiabetesMellitus           82602
Dementie                   96929
Nierfalen                  48859
Obesitas                    7026
Parkinson                  14867
Korsakov                    8578
Huntington                   740
"""

plot_compare.plot_tiles()