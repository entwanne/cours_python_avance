### La fonction `open`

L'un des gestionnaires de contexte les plus connus est probablement le fichier, tel que retourné par la fonction `open`.
Jusque là, vous avez pu l'utiliser de la manière suivante :

```python
f = open('filename', 'r')
# traitement sur le fichier
# ...
f.close()
```

Mais sachez que ça n'est pas la meilleure façon de procéder. En effet, si une exception survient pendant le traitement, la méthode `close` ne sera par exemple jamais appelée, et les dernières données écrites pourraient être perdues.

Il est donc conseillé de plutôt procéder de la sorte, avec `with` :

```python
with open('filename', 'r') as f:
    # traitement sur le fichier
    # ...
```

Ici, la fermeture du fichier est implicite, nous verrons plus loin comment cela fonctionne en interne.

Nous pourrions reproduire un comportement similaire sans gestionnaire de contexte, mais le code serait un peu plus complexe.

```python
try:
    f = open('filename', 'r')
    # traitement sur le fichier
    # ...
finally:
    f.close()
```
