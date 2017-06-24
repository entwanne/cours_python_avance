### Changement de répertoire

**Pré-requis : Gestionnaires de contexte**

Dans cet exercice, je vous propose d'implémenter un gestionnaire de contexte pour gérer le répertoire courant.
En effet, on voudrait pouvoir changer temporairement de dossier courant, sans effet de bord sur la suite du programme.

Nous voudrions aussi notre gestionnaire de contexte réutilisable et réentrant, à la manière du TP `redirect_stdout`, afin de ne pas perdre le répertoire de départ en cas de contextes imbriqués.

Ainsi, à la construction de l'objet, on enregistrerait le dossier cible, qui serait passé en paramètre.
Puis, à l'entrée du contexte, on garderait une trace du dossier courant (`os.getcwd()`) dans une pile de dossiers, avant de se déplacer vers la cible (`os.chdir`).
En sortie, il nous suffirait de nous déplacer à nouveau vers le précédent dossier courant (le dernier élément de la pile).

```python
import os

class changedir:
    def __init__(self, target):
        self.target = target
        self.stack = []

    def __enter__(self):
        current = os.getcwd()
        self.stack.append(current)
        os.chdir(self.target)

    def __exit__(self, exc_type, exc_value, traceback):
        old = self.stack.pop()
        os.chdir(old)
```

On constate que ce gestionnaire répond bien aux utilisations simples…

```python
>>> os.getcwd()
'/home/entwanne'
>>> with changedir('/tmp'):
...     os.getcwd()
...
'/tmp'
>>> os.getcwd()
'/home/entwanne'
```

… comme aux complexes.

```python
>>> cd = changedir('/tmp')
>>> os.getcwd()
'/home/entwanne'
>>> with cd:
...     with cd:
...         os.getcwd()
...
'/tmp'
>>> os.getcwd()
'/home/entwanne'
```
