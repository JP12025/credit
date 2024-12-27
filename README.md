# Numéro de carte bancaire

![credit cards](https://live.staticflickr.com/3372/3518120757_6f6d723b0e_n.jpg)

# Le problème à résoudre

Les cartes bancaires (type Visa, American Express, MasterCard...) vous permettent d'effectuer des paiements au quotidien.
Le numéro de votre carte permet de vous identifier chez le commerçant et de prélever l'argent sur votre compte.
Ces numéros sont partagés au niveau mondial et sont donc très longs.

Par exemple, les numéros des carte American Express contiennent 15 chiffres, MasterCard 16 chiffres et Visa 13 ou 16 chiffres.
Cela signifie qu'il peut exister jusqu'à 10^16 cartes MasterCard différentes en même-temps.

En réalité, ce n'est pas tout à fait vrai car les numéros de cartes sont organisés pour s'y retrouver.
Les numéros des cartes Visa commencent par `4`, les American Express par `34`ou `37` et la plupart des MasterCard par 
`51`, `52`, `53`, `54`, or `55` (il y en a d'autre mais on ne considérera que ceux là dans cet exercice).

Mais il y a une autre structure cachée dans les numéros de carte bancaire : leur `checksum`, ou signature en français,
basée sur l'algorithme de Luhn. Cette signature permet de savoir si un numéros est "correct" sans avoir à interroger 
un établissement bancaire. De simples opérations mathématiques sont suffisantes.

Vous devez écrire un programme qui vérifie la validité des numéros de cartes bancaires.

# L'algorithme de Luhn

Quelle est la formule magique inventée par Hans Peter Luhn chez IBM ? La recette est plutôt simple pour déterminer 
si un numéro est (syntaxiquement) valide:
1. en partant de l'avant-dernier chiffre à droite, prenez un chiffre sur deux
2. multiplier chaque chiffre par 2
3. faite la somme des chiffres des nombres obtenus
4. faite également la somme des chiffres qui n'ont pas été multipliés par 2
5. additionner les deux nombres, si le résultat fini par 0, le numéro est valide.

Ce n'est pas clair ?... 

Prenons l'exemple d'une carte Visa 4003600000000014.
1. en partant de l'avant-dernier chiffre à droite, prenez un chiffre sur deux
```
4003600000000014
4 0 6 0 0 0 0 1
```
2. multiplier chaque chiffre par 2
```
4 0 6  0 0 0 0 1
8 0 12 0 0 0 0 2
```
3. faite la somme des chiffres des nombres obtenus
```
8 0 12  0 0 0 0 2
8+0+1+2+0+0+0+0+2 = 13
```
4. faite également la somme des chiffres qui n'ont pas été multipliés par 2
```
4003600000000014
 0+3+0+0+0+0+0+4 = 7
```
5. additionner les deux nombres, si le résultat fini par 0, le numéro est valide.
```
7 + 13 = 20
```
Le numéro `4003600000000014` est valide !

# Implémentation

Dans un fichier `credit.py`, vous devez érire un programme qui commence par demander un numéro à l'utilisateur. Puis votre programme doit afficher `VISA`, `MASTERCARD`, `AMEX` ou `INVALID` (rien de plus, rien de moins) selon le résultat de l'algorithme de Luhn et les conditions énoncées plus haut.

Exemple avec un numéro de carte Visa valide.
```bash
$ python credit.py
Number: 4003600000000014
VISA
```

Tant que le numéro n'est pas un `int` bien formaté, c-à-d sans autre caractère que les chiffres de 0 à 9, 
votre programme doit redemander un nombre sans afficher de message d'erreur.
```bash
$ python credit.py
Number: 4003-6000-0000-0014
Number: foo
Number: 4003600000000014
VISA
```

Exemple de numéro invalide
```bash
$ python credit.py
Number: 6176292929
INVALID
````

# Les tests

N'oubliez pas qu'il est important de tester son programme.
En effet, lorsque vous décidez de tester un programme cela vous amène à vous poser des questions
sur ce que fait votre programme et les cas particuliers.

Voici quelques exemples de nombres valides :
- 4301050403060 VISA
- 7060208010802040 VISA
- 5150400020204060 MASTERCARD
- 5530603080700080 MASTERCARD
- 340901000708030 AMEX
- 340702050700020 AMEX

> [!NOTE]
> Si vous savez vérifier un numéro, vous savez aussi le générer.
> Ne faites un générateur que si vous estimez avoir le temps pour ça...

# Le rendu via git
A tout moment, vous pouvez soumettre votre travail sur github visa un `push`.

```bash
git add credit.py
git commit -m "My answer"
git push
```

Des tests automatiques seront lancés dont vous pourrez voir les résultats sur github.
