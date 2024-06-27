
# In het kort

In deze repo staan diverse Python scripts om mbv MedCAT medische voorgeschiedenis te annoteren met SNOMED concepten in de volgende categorieen:
- PulmonaalLijden
- CardiovasculairLijden
- CerebrovasculairLijden
- DiabetesMellitus
- Dementie
- Nierfalen
- Obesitas
- Parkinson
- Korsakov
- Huntington

Op basis van de mapping met ECL queries worden er veel meer documenten per categorie gevonden.


![Plot](/static/plot_comparison.png)


# Doel en Scope

Deze repo is een analyse op clustering van vrije tekst (medische voorgeschiedenis) met behulp van SNOMED ontologie.  
Dit is een alternatief op het clusteren op basis van zoektermen, zoals het MATLAB script. Beide benaderingen worden vergeleken. De verkenning van boomstructuren in SNOMED kan nieuwe inzichten geven en is een toets of de informatie vraag beantwoord kan worden.  

Deze analyse beperkt zicht tot het herkennen van concepten en houdt geen rekening met de context binnen de text waarbinnen het concept is gevonden (vervolgstap). 

# Aanpak

1. Zoektermen uit matlabscript vertalen naar SNOMED concepten en toevoegen aan annotatie model indien beschrijving ontbreekt.
2. Clusters van concepten maken met behulp van ECL queries
3. Resultaten van ECL queries samenvoegen per thema. Elk thema bevat een grote lijst met SNOMED concepten.
4. Text preprocessing, veel gebruikte afkortingen vertalen naar omschrijving. Afkorten niet vertalen als deze al in SNOMED geregeistreerd staan en opgepakt worden door de annotatie tool.
5. Draai  annotatie tool over alle preprocessed tekst.
6. Map de concepten op de lijsten gegenereerd bij stap 3.


# Datastroom

![Dataflow](/static/image.png)

# Annoteren met MedCAT

- Is een NLP pipeline op basis van een populaire library Spacy
- Heeft tolerantie voor spelfouten
- Ondersteunt werkwoord vervoeging (lemmatizer)
- Kan getraind worden om context te herkennen, om daarmee ambigue concepten te onderscheiden
- Training handmatige annotatie vergroot precisie
- Model bevat alle nederlandse SNOMED beschrijvingen. Dit genereren we zelf op basis van de NL SNOMED editie van Nictiz.
- Negatie voorspelling

# SNOMED mapping en hierarchie

Concepten kunnen gemapped worden op bepaalde thema’s door gebruik te maken van de SNOMED hiërarchie. De annotatie tool heeft geen kennis van concepten onderling, hiervoor gebruiken we een terminologie server waarin SNOMED NL is ingeladen, inclusief relaties tussen concepten.

Als alternatief kan een [online browser](https://browser.ihtsdotools.org/?perspective=full&conceptId1=404684003&edition=MAIN/SNOMEDCT-NL/2024-03-31&release=&languages=nl,en) worden ingezet


![SNOMED browser](static/browser_sr.gif)

# Expression Constraint Language (ECL)

SNOMED dataset is een graph structuur, de meest eenvoudige manier is het gebruik van ECL om bomen te doorzoeken. -> [Documentatie](https://confluence.ihtsdotools.org/display/DOCECL/Appendix+D+-+ECL+Quick+reference)

Enkele voorbeelden:
Alle concepten op het zelfde en onderliggende niveaus
```
<< 119235005|gedeelte van hersenen|
```

Concepten met een relatie met een ander concept, attribuut locatie
```
* : 363698007|locatie van bevinding| = 25087005|systema nervosum|
```

Concepten met een relatie met een ander concept, attribuut interpreteert
```
* : 363714003|interpreteert| = 311465003|cognitieve functie|
```

ECL zoekopdrachten voor elk thema vind je [hier](/vumc/snomed_mapping.py)