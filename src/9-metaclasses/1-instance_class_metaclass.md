## Instance, classe et métaclasse

En Python, tout objet a un type. Le type d'un objet peut être récupéré grâce à `type`.
Quel est donc le type d'une classe ?

```python
>>> type(object)
<class 'type'>
```

Le type d'`object` est donc `type`.
En effet, `type` est un peu plus complexe que ce que l'on pourrait penser, nous y reviendrons plus tard.

Une classe est ainsi une instance de la classe `type`.
Une classe qui permet d'instancier d'autres classes est appelée une métaclasse.


### À quoi sert une métaclasse ?

Une métaclasse permet alors de créer de nouvelles classes, mais pour quoi faire ?

L'intérêt principal des métaclasses est de pouvoir modifier les classes lors de leur création, en ajoutant de nouvelles méthodes ou attributs par exemple.

Nous verrons plus loin dans ce chapitre l'exemple d'`Enum`, une implémentation du [type énuméré](https://fr.wikipedia.org/wiki/Type_%C3%A9num%C3%A9r%C3%A9) en Python.


### Héritage et instanciation

Nous avions l'habitude de créer des classes en héritant d'une classe existante, mais pas en en instanciant une.
J'aimerais ici revenir sur ces concepts d'héritage et d'instanciation.

Les classes (ou *type objects*) sont un ensemble d'objets qui possèdent quelques caractéristiques communes :

- Elles héritent d'`object` (mis à part `object` lui-même) ;
- Elles sont des instances plus ou moins directes de `type` (de `type` ou de classes héritant de `type`) ;
- Elles peuvent être instanciées (elles sont des *callables* qui retournent des objets de ce type) ;
- On peut en hériter.

```python
>>> int.__bases__ # int hérite d'object
(<class 'object'>,)
>>> type(int) # int est une instance de type
<class 'type'>
>>> int() # on peut instancier int
0
>>> type(int()) # ce qui retourne un objet du type int
<class 'int'>
>>> class A(int): pass # on peut en hériter
```

`type` étant une classe, elle possède les mêmes caractéristiques.

```python
>>> type.__bases__ # type hérite d'object
(<class 'object'>,)
>>> type(type) # type est une instance de type
<class 'type'>
>>> class A(type): pass # on peut en hériter
```

Nous verrons par la suite comment nous pouvons instancier `type`.

Toutes les classes étant des instances de `type`, on en déduit qu'il faut passer par `type` pour toute construction de classe.
Une métaclasse est donc une classe héritant de `type`.

Dans les cas où nous créons une classe par héritage, c'est aussi une instanciation de `type` qui est réalisée en interne.

J'en profite pour vous relayer un bon article expliquant ces concepts d'instanciation et d'héritage :
<http://www.cafepy.com/article/python_types_and_objects>
