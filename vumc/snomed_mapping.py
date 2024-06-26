import json
from pydantic import BaseModel
import requests

class SnomedDescription(BaseModel):
    id: int
    conceptId: int
    term: str
    preferredTerm: str


##################################
##          ECL Requests / Create SNOMED MAPPINGS
##################################


snomed_ecls = {'PulmonaalLijden': [
        '<< 50043002|respiratoire aandoening|'
    ],
    'CardiovasculairLijden': [
        '<< 16434071000119108|verhoogd risico op cardiovasculaire aandoening|'
        ,'<< 84114007|stoornis van cardiale functie|'
        ,'<< 301095005|cardiale bevinding|'
        ,'<< 418285008|angioplastiek|'
    ],
    'CerebrovasculairLijden': [
        '<< 432504007|cerebraal infarct|'
        ,'<< 299718000|bevinding van de hersenen|'
        ,'<< 246556002|bevinding van centraal zenuwstelsel| MINUS << 74732009|psychische stoornis|'
        ,'<< 62914000|cerebrovasculaire ziekte|'
        ,'<< 439127006|trombose|'
        ,'<< 119235005|gedeelte van hersenen|'
        ,'<< 1386000|intracraniele bloeding|'
        ,'* : 363698007|locatie van bevinding| = 25087005|structuur van systema nervosum|'
    ],
    'DiabetesMellitus': [
        '<< 75934005|stoornis van metabolisme|'
    ],
    'Dementie': [
        '* : 363714003|interpreteert| = 311465003|cognitieve functie|'
        ,'<< 386806002|cognitieve functiestoornis|'
        ,'<< 111479008|organische psychische stoornis|'
    ],
    'Nierfalen': [
        '<< 106098005|bevinding betreffende urinewegstelsel|'
        ,'<< 90708001|nefropathie|'
        ,'<< 118677009|verrichting op urogenitaal stelsel|'
    ],
    'Obesitas': [
        '<< 840358001|lichaamsgewicht verhoogd|',
        '<< 8943002|gewichtstoename|'
    ],
    'Parkinson': [
        '<< 32798002|parkinsonisme|'
    ],
    'Korsakov': [
        '<< 192811002|alcoholische encefaliopatie|',
        '<< 719848005|aandoening door alcohol|'
    ],
    'Huntington': [
        '<<702376003|ziekte van Huntington-achtig syndroom|'
    ]
}


def query_ecl(ecl):
    print(ecl)
    URL_SNOMED_TERMINOLOGY_SERVER_ECL = f'http://localhost:8081/v1/snomed/expand?ecl={ecl}&includeHistoric=false'
    return [SnomedDescription(**_) for _ in requests.get(URL_SNOMED_TERMINOLOGY_SERVER_ECL).json()]
    
def load_from_ecl(ecl_queries):
    snomed_mappings = {}
    for k,v in ecl_queries.items():
        concepts = []
        [concepts.extend(query_ecl(_)) for _ in v]
        snomed_mappings[k] = concepts
    return snomed_mappings
        
snomed_mappings = load_from_ecl(snomed_ecls)
# snomed_mappings['Huntington']

def write_snomed_mappings(snomed_mappings):
    for k,v in snomed_mappings.items():

         # Convert list of models to a list of dictionaries
        concept_dict = [concept.dict() for concept in v]
        
        # Write the list of dictionaries to a JSON file
        with open(f'./data/snomed_mappings/{k}.json', 'w') as json_file:
            json.dump(concept_dict, json_file, indent=4)

write_snomed_mappings(snomed_mappings)


##################################
##          Load SNOMED MAPPINGS from FILE
##################################

def load_snomed_mapping(file_location):
    f = open(file_location)
    data = json.load(f)
    f.close()
    return [SnomedDescription(**_) for _ in data]


def load_snomed_mappings():
    snomed_mappings = {}
    for k in snomed_ecls.keys():
        snomed_mappings[k] = load_snomed_mapping(f'./data/snomed_mappings/{k}.json')
    return snomed_mappings
        
snomed_mappings = load_snomed_mappings()
# snomed_mappings['Dementie']

for k,v in snomed_mappings.items():
    print(k, len(v), len(set([_.conceptId for _ in v])))
    

"""
SNOMED mapping, beschrijvingen en concepten. (ook engelse beschrijvingen in SNOMED NL)

PulmonaalLijden 17567 4137
CardiovasculairLijden 17471 3990
CerebrovasculairLijden 99834 11826
DiabetesMellitus 15631 3134
Dementie 6254 1106
Nierfalen 24833 4574
Obesitas 400 96
Parkinson 278 67
Korsakov 506 112
Huntington 35 9
"""