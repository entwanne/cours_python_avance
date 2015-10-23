## Liste ou générateur ?

Une question qui revient souvent est celle de savoir quand choisir une liste et quand choisir un générateur, voici donc un petit comparatif :

* Les listes prennent généralement plus de place en mémoire : tous les éléments existent en même temps. Dans le cas d'un générateur, l'élément n'existe que quand l'itérateur l'atteint, et n'existe plus après (sauf s'il est référencé autre part) ;
* Les générateurs peuvent être infinis (contrairement aux listes qui occupent un espace qui se doit d'être fini).

```python
>>> def infinite():
...     n = 0
...     while True:
...         yield n
...         n += 1
```

* Les générateurs ne sont pas indexables : on ne peut associer à un élément particulier (il faut itérer jusque cet élément) ;
* Les générateurs ont une durée de vie plus courte (ils ne contiennent plus rien une fois qu'ils ont été itérés en entier) ;
* Du fait que les générateurs n'occupent que peu de place en mémoire, on peut les enchaîner sans crainte.

```python
numbers = (x**2 for x in range(100))
numbers = zip(infinite(), numbers)
numbers = (a + b for (a, b) in numbers)
```

Ainsi, les éléments du premier générateur ne seront calculés qu'au parcours de `numbers`.
Il est aussi possible de profiter des avantages de l'un et de l'autre en récupérant une liste en fin de chaîne, par exemple en remplaçant la dernière ligne par :

```python
numbers = [a + b for (a, b) in numbers]
```

Ou en ajoutant à la fin :

```python
numbers = list(numbers)
```
