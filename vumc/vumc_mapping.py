
# https://browser.ihtsdotools.org/
# There terms are SNOMED concepts under
# << 50043002|respiratoire aandoening|
PulmonaalA = [
    "COPD",
    "astma",
    "longfibrose",
    "CARA",
    "OSAS",
    "slaapapneu",
    "obstructief slaapapneu",
]

[print(_) for _ in PulmonaalA]


# << 16434071000119108|verhoogd risico op cardiovasculaire aandoening|
# << 84114007|stoornis van cardiale functie|
# << 301095005|cardiale bevinding|
# << 418285008|angioplastiek|
CardiovasculairLijdenA = [
    "hartfalen",
    "decompensatio cordis",
    "dec cordis",
    "coronair lijden",
    "atriumfibrilleren",
    "boezemfibrilleren",
    "myocardinfarct",
    "mitralisinsufficiëntie",
    "hypertrofie linker ventrikel",
    "PTCA",
    "angina pectoris",
    "hartkatheterisatie",
    "pulmonale hypertensie",
    "mitralisklepinsufficiëntie",
    "kleplijden",
    "coronair lijden",
    "myocard infarct",
    "PCI",
    "dotteren",
    "aortastenose",#TODO: ADD TO MEDCAT
    "arterieel vaatlijden",
    "PTA",
    "Claudicatio intermittens",
    "PTCA",
    "hypertrofie linker ventrikel",
    "angina pectoris",
    "hartkatheterisatie",
    "CABG",
    "coronairlijden",
    "AV-blok",
    "totaalblok",
    "hartritmestoornissen",
    "pacemaker",
    "onderwandinfarct",
    "voorwandinfarct",
    "VW infarct",
    "anteroseptaal infarct",
    "AS-infarct",
    "anterior infarct",
    "posterior infarct",
    "inferior infarct",
    "septaal infarct",
]
CardiovasculairLijdenB = ["AF", "MI", "STEMI", "PCI", "AP", "BF", "PTA"]
CardiovasculairLijdenA.extend(CardiovasculairLijdenB)



# << 432504007|cerebraal infarct|
# << 299718000|bevinding van de hersenen|
# << 246556002|bevinding van centraal zenuwstelsel|
# << 62914000|cerebrovasculaire ziekte|
# << 439127006|trombose|
# << 119235005|gedeelte van hersenen|
# << 118940003|aandoening van zenuwstelsel|          TODO: NIET GEBRUIKEN
# * : 363698007|locatie van bevinding| = 25087005|structuur van systema nervosum|
# * : 116676008|gerelateerde morfologie| = 55641003|infarct|    TODO: NIET GEBRUIKEN
# << 439127006|cardiovasculaire aandoening|  (parent van trombose)   TODO: NIET GEBRUIKEN

CerebrovasculairLijdenA = [
    "CVA",
    "TIA",
    "iCVA",
    "beroerte",
    "hersen infarct",
    "stenose arteria carotis",#TODO: ADD TO MEDCAT
    "trombose",
    "DVT",
    "herseninfarct",
    "intracerebrale hersenbloeding",
    "intracerebrale bloeding",
    "hersenbloeding",
    "stroke",
    "cerebraal infarct",
    "hemiplegie",
    "tetraplegie",
    "hemiparese",
    "hemibeeld",
    "lacunair infarct",
    "lacunaire infarcten",
    "occipitaal infarct",
    "hersenstaminfarct",
    "staminfarct",
    "media infarct",
    "mediainfarct",
    "cerebellair infarct",
    "cerebrovasculair lijden",
    "vertrebrobasillair infarct",
    "infarct linker hemisfeer",#TODO: ADD TO MEDCAT
    "infarct linkerhemisfeer",#TODO: ADD TO MEDCAT
    "infarct rechter hemisfeer",#TODO: ADD TO MEDCAT
    "infarct rechterhemisfeer",#TODO: ADD TO MEDCAT
    "infarct LHS",#TODO: ADD TO MEDCAT
    "infarct RHS",#TODO: ADD TO MEDCAT
    "cerebrale infarcten",
    "pons infarct",
    "thalamusinfarct",
    "infarct thalamus",
]
CerebrovasculairLijdenB = ["CVA", "TIA", "iCVA", "DVT", "ICH"]
CerebrovasculairLijdenA.extend(CerebrovasculairLijdenB)


# << 75934005|stoornis van metabolisme|
DiabetesMellitusA = ["diabetes mellitus", "diabetes", "suikerziekte"]
DiabetesMellitusB = ["DM", "DMII"]
DiabetesMellitusA.extend(DiabetesMellitusB)


# * : 363714003|interpreteert| = 311465003|cognitieve functie|
# << 386806002|cognitieve functiestoornis|
DementieA = [
    "dementie",
    "Alzheimer",
    "cognitieve achteruitgang",
    "MCI",
    "mild cognitive impairment",
    "cognitieve stoornis",
    "anamnetische stoornis",
    "SDAT",
]
DementieB = ["MCI"]
DementieA.extend(DementieB)




# << 106098005||bevinding betreffende urinewegstelsel
# << 90708001|nefropathie|
# << 118677009|verrichting op urogenitaal stelsel|
NierfalenA = [
    "nierfalen",
    "nierinsufficiëntie",
    "dialyse",
    "nefropathie",
    "nierfunctiestoornis",
    "verminderde nierfunctie",
    "slechte nierfunctie",
    "nierinsufficientie",
    "nierinsufficiëntie",
]



# << 840358001||lichaamsgewicht verhoogd
# << 8943002|| gewichtstoename
ObesitasA = ["obesitas", "obees", "overgewicht", "gewichtstoename"]



# << 32798002|parkinsonisme|
ParkinsonA = ["Parkinson"]



# << 192811002|alcoholische encefaliopatie|
# << 719848005|aandoening door alcohol|
KorsakovA = [
    "alcohol",
    "Korsakov",
    "Korsakoff",
    "Korsakow",
    "Wernicke encephalopathie",
    "Wernicke",
    "amnestisch syndroom",
]

# <<702376003|ziekte van Huntington-achtig syndroom|
HuntingtonA = ["Huntington"]



ArrayTotaal = {
    'PulmonaalLijden': PulmonaalA,
    'CardiovasculairLijden': CardiovasculairLijdenA,
    'CerebrovasculairLijden': CerebrovasculairLijdenA,
    'DiabetesMellitus': DiabetesMellitusA,
    'Dementie': DementieA,
    'Nierfalen': NierfalenA,
    'Obesitas': ObesitasA,
    'Parkinson': ParkinsonA,
    'Korsakov': KorsakovA,
    'Huntington': HuntingtonA
}
