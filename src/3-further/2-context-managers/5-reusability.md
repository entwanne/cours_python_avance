### Réutilisabilité et réentrance

#### Réutilisabilité

Nous avons vu que la syntaxe du bloc `with` était `with expr as var`.
Dans les exemples précédents, nous avions toujours une expression `expr` à usage unique, qui était évaluée pour le `with`.

Mais un même gestionnaire de contexte pourrait être utilisé à plusieurs reprises si l'expression est chaque fois une même variable.
En reprenant la classe `MyContext` définie plus tôt :

```python
>>> ctx = MyContext()
>>> with ctx:
...     pass
...
enter
exit
>>> with ctx:
...     pass
...
enter
exit
```

`MyContext` est un gestionnaire de contexte réutilisable : on peut utiliser ses instances à plusieurs reprises dans des blocs `with` successifs.

Mais les fichiers tels que retournés par `open` ne sont par exemple pas réutilisables : une fois sortis du bloc `with`, le fichier est fermé, il est donc impossible d'ouvrir un nouveau contexte.

```python
>>> f = open('filename', 'r')
>>> with f:
...     pass
...
>>> with f:
...     pass
...
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  ValueError: I/O operation on closed file.
```

Notre gestionnaire `context` créé grâce au décorateur `contextmanager` n'est pas non plus réutilisable : il dépend d'un générateur qui ne peut être itéré qu'une fois.

#### Réentrance

Un cas particulier de la réutilisabilité est celui de la réentrance.
Un gestionnaire de contexte est réentrant quand il peut être utilisé dans des `with` imbriqués.

```python
>>> ctx = MyContext()
>>> with ctx:
...     with ctx:
...         pass
...
enter
enter
exit
exit
```

On peut alors prendre l'exemple des classes `Lock` et `RLock` du module `threading`, qui servent à poser des verrous sur des ressources.
Le premier est un gestionnaire réutilisable (seulement) et le second est réentrant.

Pour bien distinguer la différences entre les deux, je vous propose les codes suivant.

```python
>>> from threading import Lock
>>> lock = Lock()
>>> with lock:
...     with lock:
...         pass
...

```

Python bloque à l'exécution de ces instructions.
En effet, le bloc intérieur demande l'accès à une ressource (`lock`) déjà occupée par le bloc extérieur.
Python met en pause l'exécution en attendant que la ressource se libère.
Mais celle-ci ne se libérera qu'en sortie du bloc exétieur, qui attend la fin de l'exécution du bloc intérieur.

Les deux blocs s'attendent mutuellement, l'exécution ne se terminera donc jamais.
On est ici dans un cas de blocage, appelé *dead lock*.
Dans notre cas, nous pouvons sortir à l'aide d'un ||Ctrl+C|| ou en fermant l'interpréteur.

Passons à `RLock` maintenant.

```python
>>> from threading import RLock
>>> lock = RLock()
>>> with lock:
...     with lock:
...         pass
...
```

Celui-ci supporte les `with` imbriqués, il est réentrant.
