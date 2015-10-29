## TP : Un petit creux ?

Dans ce TP, nous allons réaliser un frigo. Oui, mais pas n'importe quel frigo, j'en ai déjà un et ça ne me servirait pas à grand chose.
Nous allons créer un frigo magique. Magique ? Oui, notre frigo sera capable de cuisiner tout seul.
En fait, à chaque ouverture, il nous proposera un met au hasard parmi les recettes qu'il connaît, en fonction des ingrédients disponibles.

Voici comment j'aimerais utiliser ce frigo :

```python
>>> recettes = {
...     'choux': {
...         'oeufs': 6,
...         'farine': 180,
...         'eau': 25,
...         'beurre': 125
...     },
...     'chantilly': {
...         'creme fleurette': 25,
...         'sucre': 75
...     },
...     'omelette': {
...         'oeufs': 3
...     }
... }
>>> f = frigo(recettes, ('oeufs', 12), ('farine', 300), ('eau', 100), ('beurre', 250))
>>> # Oui, nous rangeons la farine au frigo !
>>> next(f)
'choux'
>>> next(f)
'omelette'
>>> f.send(('oeufs', 3))
>>> f.send(('farine', 500))
>>> next(f)
'choux'
>>> next(f)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

En résumé, donc :

* On construit un frigo à l'aide d'un dictionnaire de recettes et de quantités d'ingrédients ;
* Il est possible d'injecter un nouvel ingrédient à l'aide de `send`, en précisant le nom et la quantité ;
* Chaque appel à `next` réalise une recette en consommant les ingrédients ;
* Quand plus aucune recette n'est réalisable, le générateur s'arrête.

Voici ma solution :

```python
from collections import Counter
from random import choice

def eligible(recette, stock):
    """Indique si une recette est éligible en fonction du stock
    i.e. si chaque ingrédient est présent en quantité suffisante"""
    return all(stock[ingredient] >= n for ingredient, n in recette.items())

def simple_frigo(recettes):
    "Crée un frigo vide avec seulement des recettes"
    stock = Counter()
    ret = yield # Premier yield pour permettre de remplir le frigo
    while True:
        while ret is not None: # Chaque ingrédient envoyé est ajouté au stock
            ingredient, n = ret
            stock[ingredient] += n
            ret = yield
        try:
            # Choisit une recette aléatoire parmi les éligibles
            name, recette = choice([(name, r) for name, r in recettes.items() if eligible(r, stock)])
        except IndexError:
            # IndexError est levé quand choice reçoit une liste vide
            # Aucune recette n'était éligible, on sort du générateur
            break
        for ingredient, n in recette.items(): # Consommation des ingrédients de la recette
            stock[ingredient] -= n
        ret = yield name

def frigo(recettes, *ingredients):
    "Crée un frigo à l'aide de recettes et d'ingrédients de base"
    frigo = simple_frigo(recettes) # Instancie un frigo simple
    next(frigo) # Premier next afin de pouvoir commencer à envoyer des ingrédients
    for i in ingredients:
        frigo.send(i) # Envoi des ingrédients de base
    yield from frigo # Puis passage au comportement normal de notre frigo
```

J'ai ici choisi de séparer le générateur en deux fonctions, afin de ne pas avoir à répéter l'étape de remplissage des stocks (à la première recette, puis à chaque send).
