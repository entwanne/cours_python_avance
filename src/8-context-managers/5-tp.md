## TP: changement de répertoire

Dans ce TP, je vous propose d'implémenter un gestionnaire de contexte pour gérer le répertoire courant.
En effet, on voudrait pouvoir changer temporairement de dossier courant, sans effet de bord sur la suite du programme.

Ainsi, à la construction de l'objet, on enregistrerait le dossier cible.
Puis, à l'entrée du contexte, on garderait une trace du dossier courant avant de se déplacer vers la cible (`os.chdir`).
En sortie, il nous suffirait de nous déplacer à nouveau vers le précédent dossier courant.

On peut aussi hériter de `ContextDecorator` afin de l'utiliser en tant que décorateur.

```python
import os
from contextlib import ContextDecorator

class changedir(ContextDecorator):
    def __init__(self, target):
        self.target = target
    def __enter__(self):
        self.current = os.getcwd()
        os.chdir(self.target)
    def __exit__(self, *_):
        os.chdir(self.current)
```

```python
>>> os.getcwd()
'/home/antoine'
>>> with changedir('/tmp'):
...     os.getcwd()
...
'/tmp'
>>> os.getcwd()
'/home/antoine'
>>> @changedir('/')
... def func():
...     return os.getcwd()
...
>>> func()
'/'
>>> os.getcwd()
'/home/antoine'
```
