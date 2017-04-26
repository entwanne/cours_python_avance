### Liens utiles

Et pour terminer ce chapitre, un nouveau rappel vers la documenation Python.
Je vous encourage vraiment à la lire le plus possible, elle est très complète et très instructive, bien que parfois un peu bordélique.

* Définition du terme métaclasse : <https://docs.python.org/3/glossary.html#term-metaclass>
* Personnalisation de la création de classes : <https://docs.python.org/3/reference/datamodel.html#customizing-class-creation>
* Classe `type` : <https://docs.python.org/3/library/functions.html#type>
* PEP relative aux métaclasses : <https://www.python.org/dev/peps/pep-3115/>

Je tenais aussi à présenter ici [un tutoriel/guide en 8 parties de Sam&Max dédié au modèle objet, à `type` et aux métaclasses](http://sametmax.com/le-guide-ultime-et-definitif-sur-la-programmation-orientee-objet-en-python-a-lusage-des-debutants-qui-sont-rassures-par-les-textes-detailles-qui-prennent-le-temps-de-tout-expliquer-partie-1/).

Enfin, je ne peux que vous conseiller de vous pencher sur [les sources de CPython](https://github.com/python/cpython) pour comprendre les mécanismes internes.
Notamment [le fichier `Objects/typeobject.c`](https://github.com/python/cpython/blob/master/Objects/typeobject.c) qui définit les classes `type` et `object`.
