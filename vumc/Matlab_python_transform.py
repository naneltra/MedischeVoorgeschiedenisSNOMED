"""
THis script load a amnesis dump file and clusters by keyword 
"""
import pandas as pd
from tqdm import tqdm
import re
import vumc_mapping
import typer
import os
from dotenv import load_dotenv


load_dotenv()


MEDISCHE_VOORGESCHIEDENIS_FILE = '../' + os.getenv('DATA_FILE')
VUMC_SOM_TERMS_PER_AANDOENING = os.getenv('VUMC_SOM_TERMS_PER_AANDOENING')

tqdm.pandas(desc="processing vumc dataextract")


data = pd.read_csv(MEDISCHE_VOORGESCHIEDENIS_FILE)
print(data.shape)
data.tail()

df = data.copy()
df = df.rename(columns={"diagnose":"text"})
# df = df.set_index('id')
df = df.loc[~df['text'].isna()]


def count_term(txt, terms: list, ignore_case = False):
    count:int = 0
    
    for term in terms:
        term = re.escape(term)
        if ignore_case:
            count += len(re.findall(rf"\b{term}(?:[.><+]|\s|$)",txt, re.IGNORECASE))
            continue
        count += len(re.findall(rf"\b{term}(?:[.><+]|\s|$)",txt))
    return count

for k, v in tqdm(vumc_mapping.ArrayTotaal.items()):
    df[k] = df['text'].progress_apply(lambda x: count_term(x, v,True) > 0)

df.head()
df.to_csv(VUMC_SOM_TERMS_PER_AANDOENING, index=None)

df.loc[:,'PulmonaalLijden':'Huntington'].sum()

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




