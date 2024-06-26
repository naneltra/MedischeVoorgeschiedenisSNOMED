from medcat.cat import CAT
from pathlib import Path
from vumc import vumc_mapping

import importlib
importlib.reload(vumc_mapping)

batch_size_chars = 68800 

model_location = '/Users/lennaartraams/git/r-d-projects/gm-r-d/apps/medcat_service/models/snomed_2023_trained_neg_b3c1e19c8ffccf75.zip'
MODEL_PATH = Path(model_location)

mymodel = CAT.load_model_pack(MODEL_PATH.absolute().as_posix())


vumc_mapping1 = vumc_mapping.ArrayTotaal

[print(_) for _ in vumc_mapping1.keys()]

all_vumc_terms = []
[all_vumc_terms.extend(_) for _ in vumc_mapping1.values()]
all_vumc_terms



missing_terms = []
for t in all_vumc_terms:
    if not bool(mymodel.get_entities(t)['entities']):
        missing_terms.append(t)
        
missing_terms

all_vumc_terms_annotated = []
for t in all_vumc_terms:
    if bool(mymodel.get_entities(t)['entities']):
        all_vumc_terms_annotated.append((t,mymodel.get_entities(t)['entities']))
        
all_vumc_terms_annotated







new_descriptions = {'CARA': 427896006,
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
#  ' AF ',
#  ' MI ',
#  ' AP ',
#  ' BF ',
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
 'occipitaal infarct',
 'pons infarct'
 'infarct RHS'
 'infarct LHS'
 'infarct rechterhemisfeer'
 'infarct rechter hemisfeer'
 'infarct linkerhemisfeer',
 'infarct linker hemisfeer'
 'vertrebrobasillair infarct'
 'cerebrovasculair lijden'
 'occipitaal infarct'
 'stenose arteria carotis'
 'septaal infarct'
 'inferior infarct'
 'posterior infarct'
 'anterior infarct'
 'AS-infarct'
 'anteroseptaal infarct'
 'VW infarct'
 'myocard infarct'
 }

for k,v in new_descriptions.items():
    cui = str(v)
    mymodel.add_and_train_concept(cui=cui,name=k)
    
    
mymodel.get_entities('mr heeft stroke')