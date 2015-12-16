## Utiliser une fonction comme métaclasse

Par extension, on appelle parfois métaclasse tout *callable* qui renverrait une classe lorsqu'il serait appelé.

Ainsi, une fonction faisant appel à `type` serait considérée comme métaclasse.

```python
>>> def meta(*args):
...     print('enter metaclass')
...     return type(*args)
...
>>> class A(metaclass=meta):
...     pass
...
enter metaclass
```

Cependant, on ne peut pas à proprement parler de métaclasse, celle de notre classe `A` étant toujours `type`.

```python
>>> type(A)
<class 'type'>
```

Ce qui fait qu'à l'héritage, l'appel à la métaclasse serait perdu (cet appel n'étant réalisé qu'une fois).

```python
>>> class B(A):
...     pass
...
```

Pour rappel, le comportement avec une « vraie » métaclasse serait le suivant :

```python
>>> class meta(type):
...     def __new__(cls, *args):
...         print('enter metaclass')
...         return super().__new__(cls, *args)
...
>>> class A(metaclass=meta):
...     pass
...
enter metaclass
>>> type(A)
<class '__main__.meta'>
>>> class B(A):
...     pass
...
enter metaclass
```
