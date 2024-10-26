"""
This script checks if all keywords defined in the matlab script from aumc are mapped correctly to SNOMED concepts.
Keywords that were not yet present as concept in SNOMED will be added by search fitting concepts manually.
"""

from medcat.cat import CAT
from vumc import vumc_mapping
import os
from datetime import date
import pandas as pd

from dotenv import load_dotenv

load_dotenv()


def load_model():
    model_location = os.getenv('MODEL_PATH')
    return CAT.load_model_pack(model_location)
    
def get_all_vumec_terms():
    all_vumc_terms = []
    [all_vumc_terms.extend(_) for _ in vumc_mapping1.values()]
    return all_vumc_terms

def get_missing_terms(model):
    missing_terms = []
    mymodel = load_model()
    for t in get_all_vumec_terms():
        if not bool(model.get_entities(t)['entities']):
            missing_terms.append(t)
    return missing_terms

def load_terms():
    abbreviations_df = pd.read_csv('./data/terms.csv',index_col=None)
    abbreviations_df = abbreviations_df.loc[abbreviations_df['status']=='enable']
    return [_['term'] for _ in abbreviations_df.to_dict(orient='records')]

def annotate_terms(terms):
    model = load_model()
    terms_annotated = []
    for t in terms:
        terms_annotated.append((t,model.get_entities(t)['entities']))
    return terms_annotated


annotate_terms(load_terms())



vumc_mapping1 = vumc_mapping.ArrayTotaal
mymodel = load_model()

# keywords without SNOMED concept
missing_terms = get_missing_terms(mymodel)

all_vumc_terms_annotated = []
for t in get_all_vumec_terms():
    if bool(mymodel.get_entities(t)['entities']):
        all_vumc_terms_annotated.append((t,mymodel.get_entities(t)['entities']))
        
all_vumc_terms_annotated

new_descriptions = {
 'CARA': 427896006,
 'dec cordis': 195111005,
 'mitralisinsufficiëntie': 194736003,
 'mitralisklepinsufficiëntie': 48724000,
 'aortastenose': 29201000146108,
 'coronairlijden': 414024009,
 'coronair lijden': 414024009,
 'totaalblok': 233916004,
 'hartritmestoornissen': 698247007,
 'onderwandinfarct': 73795002,
 'voorwandinfarct':233839009,
 'intracerebrale hersenbloeding': 274100004,
 'hersenbloeding': 274100004,
 'stroke' : 230690007,
 'hemibeeld':50582007,
 'staminfarct': 95454007,
 'mediainfarct': 705128004,
 'media infarct': 705128004,
 'thalamusinfarct' : 427296003,
 'infarct thalamus': 427296003,
 'ICH': 274100004,
 'DM': 73211009,
 'DMII': 73211009,
 'Alzheimer': 26929004,
 'cognitieve achteruitgang':386805003,
 'MCI':386805003,
 'nierinsufficiëntie': 42399005,
 'Korsakov': 69482004,
 'Korsakoff': 69482004,
 'Korsakow': 69482004,
 'Wernicke encephalopathie': 21007002,
 'Wernicke': 69482004,
 'Huntington': 58756001,
 'occipitaal infarct': 276219001,
 'pons infarct'
 'infarct rechterhemisfeer': 307767006,
 'infarct rechter hemisfeer': 307767006,
 'infarct RHS': 307767006,
 'rechter hemisfeer': 5228007,
 'rechterhemisfeer': 5228007,
 'RHS': 5228007,
 'infarct linkerhemisfeer': 307766002,
 'infarct linker hemisfeer': 307766002,
 'infarct LHS': 307766002,
 'linkerhemisfeer': 72792008,
 'linker hemisfeer': 72792008,
 'LHS': 72792008,
 'vertrebrobasillair infarct':230717002,
 'vertebrobasilair infarct':230717002,
 'cerebrovasculair lijden': 62914000,
 'occipitaal': 31065004,
 'occipitaal infarct': 276219001,
 'stenose arteria carotis': 64586002,
 'stenose linker arteria carotis': 64586002,
 'stenose rechter arteria carotis': 64586002,
 'septaal infarct': 79009004,
 'inferior infarct': 233840006,
 'posterior infarct': 164869004,
 'anterior infarct': 233839009,
 'AS-infarct': 394659003,
 'anteroseptaal infarct': 62695002,
 'VW infarct': 233839009,
 'myocard infarct': 394659003,
 'MDL':183523005,
 'ACM':17232002,
 'ACP':70382005
 }

def add_and_train_annotations():
    for k,v in new_descriptions.items():
        cui = str(v)
        mymodel.add_and_train_concept(cui=cui,name=k)
    
    
#test
mymodel.get_entities('mr LHS')
mymodel.get_entities('mr MCI')
mymodel.create_model_pack(f'snomed_2023_trained_neg_{str(date.today())}')


