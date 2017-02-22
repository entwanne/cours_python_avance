### Instance, classe et métaclasse

On sait que tout objet est instance d'une classe.
On dit aussi que la classe est le type de l'objet.
Et donc, tout objet a un type.
Le type d'un objet peut être récupéré grâce à la *fonction* `type`.

```python
>>> type(5)
<class 'int'>
>>> type('foo')
<class 'str'>
>>> type(lambda: None)
<class 'function'>
```

Mais si les classes sont des objets, quel est alors leur type ?

```python
>>> type(object)
<class 'type'>
```

Le type d'`object` est `type`.
En effet, `type` est un peu plus complexe que ce que l'on pourrait penser, nous y reviendrons dans le prochain chapitre.

On notera simplement qu'une classe est alors une instance de la classe `type`.
Et qu'une classe telle que `type`, qui permet d'instancier d'autres classes, est appelée une métaclasse.

Instancier une classe pour en créer une nouvelle n'est pas forcément évident.
Nous avons plutôt l'habitude d'hériter d'une classe existante.
Mais dans les cas où nous créons une classe par héritage, c'est aussi une instanciation de `type` qui est réalisée en interne.

#### Caractéristiques des classes

Les classes (ou *type objects*) sont un ensemble d'objets qui possèdent quelques caractéristiques communes :

- Elles héritent d'`object` (mise à part `object` elle-même) ;
- Elles sont des instances plus ou moins directes de `type` (de `type` ou de classes héritant de `type`) ;
- On peut en hériter ;
- Elles peuvent être instanciées (elles sont des *callables* qui retournent des objets de ce type).

```python
>>> int.__bases__ # int hérite d'object
(<class 'object'>,)
>>> type(int) # int est une instance de type
<class 'type'>
>>> class A(int): pass # on peut hériter de la classe int
>>> int() # on peut instancier int
0
>>> type(int()) # ce qui retourne un objet du type int
<class 'int'>
```

Et on observe que notre classe `A` est elle aussi instance de `type`.

```python
>>> type(A)
<class 'type'>
```
