# Conteneurs

En Python, on appelle conteneur (*container*) un objet ayant vocation à en contenir d'autres, comme les chaînes de caractères, les listes, les ensembles ou les dictionnaires.

Il existe plusieurs catégories de conteneurs, notamment celle des *subscriptables*. Ce nom barbare regroupe tous les objets sur lesquels l'opérateur `[]` peut être utilisé.
L'ensemble des types cités dans le premier paragraphe sont *subscriptables*, à l'exception de l'ensemble (*set*), qui n'implémente pas l'opération `[]`.

Les *subscriptables* se divisent en deux nouvelles catégories  : les *indexables* et les *sliceables*. Les premiers sont ceux pouvant être indexés avec des nombres entiers, les seconds pouvant l'être avec des `slice` (voir plus loin).

On parle plus généralement de séquence quand un conteneur est *indexable* et *sliceable*.

Une autre catégorie important de conteneurs est formée par les *mappings* : il s'agit des objets qui associent des valeurs à des clefs, comme le font les dictionnaires.

Une séquence et un *mapping* se caractérisent aussi par le fait qu'ils possèdent une taille, comme nous le verrons plus loin dans ce chapitre.
