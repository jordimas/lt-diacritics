# Introducció

Al LanguageTool tenim més de 3500 de regles que han anat creixent amb els anys per a identificar aquests errors. Ara volia contribuir-hi, fet una anàlisi quantitativa per tal d'identificar aquests casos que encara no identifiquem correctament.

Objectiu del projecte: analitzar de forma quantitativa l'ús de paraules que es diferencien només per l'accent diacrític i que potencialment poden ser errors comuns per tal de:
* Entendre quin espectre cobreixen les regles actuals
* Identificar regles noves que podem crear de forma sistemàtica per solucionar aquests casos

# Metodologia


# Dades

Tenim 1.179.865 formes al diccionari, d'aquestes 888.650 són úniques ja que al diccionari tenim una entrada per forma i funció gramatical (per exemple «que» té tres entrades, una per cada funció que té).

De les 888.650 formes, 60689 (6.83%) són formes que existeixen amb versió amb i sense diacrític. D'aquestes, 26277 (43.30%) les troben als nostres corpus, és a dir, tenim exemples del seu ús. Les que no trobem als corpus, són formes extremadament poc freqüents, un 95.89% de són formes verbals que s'usen molt poc.

El següent pas és entendre la freqüència d'aparició d'aquests parells (per exemple  bàsquet/basquet) als corpus, això ens dóna un senyal clar de si els s'usen o no freqüentment. Les regles per detectar aquest tipus d'errors són costoses de fer, llavors volem focalitzar-nos en aquelles on el problema és freqüent (per exemple, tabac/tàbac no ho és).


