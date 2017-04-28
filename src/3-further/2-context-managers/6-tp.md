### TP : Redirection de sortie (`redirect_stdout`)

Nous allons ici mettre en place un gestionnaire de contexte équivalent à `redirect_stdout` pour rediriger la sortie standard vers un autre fichier.
Il sera aussi utilisable en tant que décorateur pour rediriger la sortie standard de fonctions.

La redirection de sortie est une opération assez simple en Python.
La sortie standard est identifiée par l'attribut/fichier `stdout` du module `sys`.
Pour rediriger la sortie standard, il suffit alors de faire pointer `sys.stdout` vers un autre fichier.

Notre gestionnaire de contexte sera construit avec un fichier dans lequel rediriger la sortie.
Nous enregistrerons donc ce fichier dans un attribut de l'objet.

À l'entrée du contexte, on gardera une trace de la sortie courante (`sys.stdout`) avant de la remplacer par notre cible.
Et en sortie, il suffira de faire à nouveau pointer `sys.stdout` vers la précédente sortie standard, préalablement enregistrée.

Nous pouvons faire hériter notre classe de `ContextDecorator` afin de pouvoir l'utiliser comme décorateur.

```python
import sys
from contextlib import ContextDecorator

class redirect_stdout(ContextDecorator):
    def __init__(self, file):
        self.file = file

    def __enter__(self):
        self.old_output = sys.stdout
        sys.stdout = self.file

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self.old_output
```

Pour tester notre gestionnaire de contexte, nous allons nous appuyer sur les `StringIO` du module `io`.
Il s'agit d'objets se comportant comme des fichiers, mais dont tout le contenu est stocké en mémoire, et accessible à l'aide d'une méthode `getvalue`.

```python
>>> from io import StringIO
>>> output = StringIO()
>>> with redirect_stdout(output):
...     print('ceci est écrit dans output')
...
>>> print('ceci est écrit sur la console')
ceci est écrit sur la console
>>> output.getvalue()
'ceci est écrit dans output\n'
```

```python
>>> output = StringIO()
>>> @redirect_stdout(output)
... def addition(a, b):
...     print('result =', a + b)
...
>>> addition(3, 5)
>>> output.getvalue()
'result = 8\n'
```

Notre gestionnaire de contexte se comporte comme nous le souhaitions, mais possède cependant une lacune : il n'est pas réentrant.

```python
>>> output = StringIO()
>>> redir = redirect_stdout(output)
>>> with redir:
...     with redir:
...         print('ceci est écrit dans output')
...
>>> print('ceci est écrit sur la console')
```

Comme on le voit, ou plutôt comme on ne le voit pas, le dernier affichage n'est pas imprimé sur la console, mais toujours dans `output`.
En effet, lors de la deuxième entrée dans `redir`, `sys.stdout` ne pointait plus vers la console mais déjà vers notre `StringIO`, et la trace sauvegardée (`self.old_output`) est alors perdue puisqu'assignée à `sys.stdout`.

Pour avoir un gestionnaire de contexte réentrant, il nous faudrait gérer une pile de fichiers de sortie.
Ainsi, en entrée, la sortie actuelle serait ajoutée à la pile avant d'être remplacée par le fichier cible.
Et en sortie, il suffirait de retirer le dernier élément de la pile et de l'assigner à `sys.stdout`.

```python
import sys

class redirect_stdout(ContextDecorator):
    def __init__(self, file):
        self.file = file
        self.stack = []

    def __enter__(self):
        self.stack.append(sys.stdout)
        sys.stdout = self.file

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self.stack.pop()
```

Vous pouvez constater en reprenant les tests précédent que cette version est parfaitement fonctionnelle (pensez juste à réinitialiser votre interpréteur suite aux tests qui ont définitivement redirigé `sys.stdout` vers une `StringIO`).
