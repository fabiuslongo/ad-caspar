# Knowledge Representation Summary

In this file are summarized all expressive capabilities of the cognitive architecture CASPAR.


### Mono-action nested definite clauses

---------------

This is the simplest case of one intransitive action/subject clause.

* Robert drinks
```sh
> Drink_VBZ(Robert_NNP(x1), __)
```
By making the action transitive adding an object, the second slot will be populated as follow:
* Robert drinks wine
```sh
> Drink_VBZ(Robert_NNP(x1), Wine_NN(x2))
```
Even imperative verbal phrases:
* drink the wine
```sh
> Drink_VB(__, Wine_NN(x1))
```
An action can also preserve its passive form (the thief is not the main actor of the action, but he receives it). The difference between the previous case is given by the POS:
* The thief has been caught
```sh
> Catch_VBN(__, Thief_NN(x2))
```
In the presence of an agent (the police), as action's actor, the subject will be populated as well.
* The thief has been caught by the police
```sh
> Catch_VBN(Police_NN(x1), Thief_NN(x2))
```
Let's make expressions more descriptive, by adding adjvectives (Good_JJ(...)) and adverbs (Slowly_RB(...)):
* Robert slowly drinks good wine
```sh
> Slowly_RB(Drink_VBZ(Robert_NNP(x1), Good_JJ(Wine_NN(x2))))
```
Let’s apply a further modification, in order to include a verbal preposition. In such case a proper action modificator (In_IN(_, object_preposition)) will be integrated in the clauses:
* Robert slowly drinks good wine in the living room
```sh
> In_IN(Slowly_RB(Drink_VBZ(Robert_NNP(x1), Good_JJ(Wine_NN(x2)))), Living_NN_Room_NN(x3))
```

### Negations

---------------

In the case the main verb of the action is negated, the corrispondent clause without the negation will be retracted.

* Colonel West doesn't sell missiles to Nono
```sh
> RETRACTED ---> To_IN(Sell_VB(Colonel_NNP_West_NNP(x1), Missile_NNS(x2)), Nono_NNP(x3))
```
Other negations are considered not primary modificators, thus preserved. Clauses KB is still consistent.
* Colonel West doesn't sell not good missiles to Nono
```sh
> RETRACTED ---> To_IN(Sell_VB(Colonel_NNP_West_NNP(x1), Not_RB_Good_JJ(Missile_NNS(x2))), Nono_NNP(x3))
```
* Colonel West sell not good missiles to Nono
```sh
> To_IN(Sell_VB(Colonel_NNP_West_NNP(x1), Not_RB_Good_JJ(Missile_NNS(x2))), Nono_NNP(x3))
```
* Robert knows that Barbara is not a not good housewife
```sh
> Know_VBZ(Robert_NNP(x1), Not_RB(Be_VBZ(Barbara_NNP(x3), Not_RB_Good_JJ(Housewife_NN(x4)))))
```


### Multi-action nested definite clauses

---------------

Here is some example with utterances containing disjoint actions: in this case, two distinct literals will be asserted.
* Robert knows the truth and Barbara drinks wine
```sh
> Know_VBZ(Robert_NNP(x1), Truth_NN(x2))
> Drink_VBZ(Barbara_NNP(x3), Wine_NN(x4))
```

Utterances containing interactive actions can also be expressed: in this case the two actions will be merged in a single literal.
* Robert knows that Barbara drinks wine
```sh
> Know_VBZ(Robert_NNP(x1), Drink_VBZ(Barbara_NNP(x3), Wine_NN(x4)))
```
* The man called Robert is a good man
```sh
> Be_VBZ(Call_VBN(Man_NN(x1), Robert_NNP(x3)), Good_JJ(Man_NN(x2)))
```
### Implicative nested definite clauses

---------------

Here is some example of utterance subordinated by specific conditions. 
#### Mono-condition
* When the sun shines strongly, Robert is happy
```sh
> Strongly_RB(Shine_VBZ(Sun_NN(x1), __)) ==> Be_VBZ(Robert_NNP(x3), Happy_NNP(x4))
```
when fulfilling object role, adjectives (Happy_JJ) are turned into nouns (Happy_NNP). Conditions may be also more than one.

#### Multi-condition
* As the air is cool and the sun shines, Robert is happy
```sh
> Be_VBZ(Air_NN(x1), Cool_NNP(x2)) & Shine_VBZ(Sun_NN(x3), __) ==> Be_VBZ(Robert_NNP(x5), Happy_NNP(x6))
```
Commas usage is recommended to have more chances of success, especially with long sentences.

#### Multi-proposition
Since implicative definite clauses must have not more of a single positive literal as consequent, in presence of a non-definite multi-proposition clause, it will be splitted into n=2 (n=#propositions) definite clauses like follow:
* When the air is cool, Barbara drinks wine and Robert is happy
```sh
> Be_VBZ(Air_NN(x1), Cool_NNP(x2)) ==> Drink_VBZ(Barbara_NNP(x3), Wine_NN(x4))
> Be_VBZ(Air_NN(x1), Cool_NNP(x2)) ==> Be_VBZ(Robert_NNP(x5), Happy_NNP(x6))
```
#### Mixed
* As the air is cool and the sun shines, Barbara drinks wine and Robert is happy
```sh
> Be_VBZ(Air_NN(x1), Cool_NNP(x2)) & Shine_VBZ(Sun_NN(x3), __) ==> Drink_VBZ(Barbara_NNP(x5), Wine_NN(x6))
> Be_VBZ(Air_NN(x1), Cool_NNP(x2)) & Shine_VBZ(Sun_NN(x3), __) ==> Be_VBZ(Robert_NNP(x7), Happy_NNP(x8))
```