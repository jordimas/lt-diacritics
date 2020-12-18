# Introducció

En el context del corrector gramatical LanguageTool, l'objectiu d'aquest projecte és analitzar de forma quantitativa l'ús de paraules que es diferencien només per l'accent diacrític (p. ex. llàstima/llastima) i que potencialment poden ser errors comuns per tal de:
* Entendre quin espectre d'aquest tipus de paraules cobreixen les regles actuals
* Identificar regles noves que podem crear de forma sistemàtica per solucionar aquests casos

Al LanguageTool tenim més de 3500 de regles que han anat creixent de forma orgànica amb els anys per a identificar aquests errors.

# Dades

Tenim 1.179.865 formes al diccionari, d'aquestes 888.650 són úniques ja que al diccionari tenim una entrada per forma i funció gramatical (per exemple «que» té tres entrades, una per cada funció que té).

De les 888.650 formes, 60.689 (6.83%) són formes que existeixen amb versió amb diacrític i sense. D'aquestes 45.416 (74.83%) les troben als nostres corpus, és a dir, tenim exemples del seu ús. Les que no trobem als corpus, són formes extremadament poc freqüents, un 95.89% de són formes verbals que s'usen molt poc.

Ara entenem la freqüència d'aparició d'aquests parells (per exemple bàsquet/basquet) als corpus, això ens dóna un senyal clar de si s'usen o no freqüentment.

![Freqüencia d'aparició de diacrítics](frequencia-diacritics.png)

# Metodologia 

## Primera fase

Objectiu: detectar paraules poc freqüents que es poden confondre podem assenyalar com a error

Metodologia:
* Extraiem del corpus exemples del seu ús amb accent
* Demanem a LanguageTool que indiqui quants errors té l'exemple
* Llevem l'accent de la paraula
* Demanem a LanguageTool que indiqui quants errors té l'exemple sense accent

Això ens permet identificar de forma sistemàtica les formes que es poden confondre, que no detectem, i que per freqüència d'aparició podem fer una recomanació a l'usuari.

## Segona fase

Objectiu: detectar paraules freqüents que es poden confondre podem assenyalar com a error

Per paraules on la freqüència d'aparició amb diacrític i sense està més igualada provarem de fer regles genèriques i veure de forma sistemàtica quines funcionen millor avaluant-les de forma les diferents versions contra corpus e introduint errors.


# Resultats del projecte (18 desembre)

Millores a LanguageTool 5.2:

* Ens ha permés identificar formes molt poc freqüents i ja no usades en el diccionari que existeixen en versió amb accent i llevar-les dels diccionaris
* S'ha millorat la regla que detectava formes balears [CA_SIMPLE_REPLACE_BALEARIC](https://community.languagetool.org/rule/show/CA_SIMPLE_REPLACE_BALEARIC?lang=ca)
* S'ha creat una regla nova [RARE_WORDS](https://community.languagetool.org/rule/show/RARE_WORDS?lang=ca) que basant-se amb la freqüència d'aparició de la paraula amb accent o sense (per exemple, 95% que aquesta paraula va sempre va amb accent) ho suggereixi

