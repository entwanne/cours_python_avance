## `with` or without you

Un contexte est ainsi un scope particulier, avec des opérations exécutées en entrée et en sortie.

Un bloc d'instruction `with` se présente comme suit.

```python
with expr as x: # avec expr étant un gestionnaire de contexte
    # operations sur x
```

La syntaxe est assez simple à appréhender, `x` permettra ici de contenir des données propres au contexte (`x` vaudra `expr` dans la plupart des cas).
Si par exemple `expr` correspondait à une ressource, la libération de cette ressource (fermeture du fichier, déblocage du verrou, etc.) serait gérée pour nous en sortie du scope, dans tous les cas.

Il est aussi possible de gérer plusieurs contextes dans un même bloc :

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
