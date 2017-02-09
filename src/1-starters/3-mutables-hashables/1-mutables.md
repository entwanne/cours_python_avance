### Mutables

Un objet mutable est ainsi un objet qui peut être modifié, dont on peut changer les propriétés une fois qu'il a été défini.
Une erreur courante est de confondre modification et réassignation.

La différence est facile à comprendre avec les listes.
Les listes sont des objets mutables : une fois la liste instanciée, il est par exempe possible d'y insérer de nouveaux éléments.

```python
>>> values = [0, 1, 2]
>>> values.append(3)
>>> values
[0, 1, 2, 3]
```

Le fonctionnement des variables en Python fait qu'il est possible d'avoir plusieurs noms (étiquettes) sur une même valeur.
Le principe de mutabilité s'observe alors très bien.

```python
>>> values = othervalues = [0, 1, 2]
>>> values.append(3)
>>> values
[0, 1, 2, 3]
>>> othervalues
[0, 1, 2, 3]
```

Sans que nous n'ayons explicitement touché à `othervalues`, sa valeur a changé. En effet, `values` et `othervalues` référencent un même objet.
Un même objet mutable.

En revanche, la réassignation fait correspondre le nom de la variable à un nouvel objet, il n s'agit pas d'une modification de la valeur initiale.

```python
>>> values = othervalues = [0, 1, 2]
>>> values = [0, 1, 2, 3] # réassignation de values
>>> values
[0, 1, 2, 3]
>>> othervalues
[0, 1, 2]
```

En Python, les objets de type `bool`, `int`, `str`, `tuple` et `frozenset` sont immutables.
Tous les autres types, les listes, les dictionnaires, ou les instances de vos propres classes sont des objets mutables.

Comme nous l'avons vu, les objets mutables sont à prendre avec des pincettes, car leur valeur peut changer sans que nous ne l'ayons explicitement demandé.
Cela peut arriver lorsqu'une valeur mutable est passée en argument à une fonction.

```python
>>> def append_42(values):
...     values.append(42)
...     return values
...
>>> v = [1, 2, 3, 4]
>>> append_42(v)
[1, 2, 3, 4, 42]
>>> v
[1, 2, 3, 4, 42]
```

Cela ne pourra jamais arriver avec un *tuple* par exemple, qui est immutable et ne possède aucune méthode pour être altéré.

```python
>>> def append_42(values):
...     return values + (42,)
...
>>> v = (1, 2, 3, 4)
>>> append_42(v)
(1, 2, 3, 4, 42)
>>> v
(1, 2, 3, 4)
```

Il n'est pas vraiment possible en Python de créer un nouveau type de mutables.
- rendre méthodes inefficaces (mais pas sûr)
- hériter d'un type immutable (namedtuple < tuple)
