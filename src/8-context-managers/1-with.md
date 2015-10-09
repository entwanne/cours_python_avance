## `with` or without you

- with, fonctionnement, gestion des ressources

Un contexte est ainsi un scope particulier, avant lequel aura lieu l'allocation des ressources, et leur désallocation en sortie.

Un bloc d'instruction `with` se présente comme suit.

```python
with expr as x:
    # operations sur x
```

La syntaxe est assez simple à appréhender, on remplace simplement `x = expr` par `with expr as x`, et la désallocation de la ressource est gérée pour nous, dans tous les cas.

Il est aussi possible d'allouer plusieurs ressources dans un même bloc :

```python
with expr1 as x, expr2 as y:
    # traitements sur x et y
```

équivalent à

```python
with expr1 as x:
    with expr2 as y:
        # traitements sur x et y
```
