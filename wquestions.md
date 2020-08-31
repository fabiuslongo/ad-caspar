# Questions capabilities overview

In this file is shown how AD-CASPAR deals with Polar and Wh-questions, by the means of the module qa_shifter.py. The latter
works as a parser based on production rules, which works considering linguistic rules in order to shift a question into a likely assertion.
Every question, by leveraging its dependencies, is divided into chunks as it follows:

[PRE_AUX]-[AUX]-[POST_AUX]-[ROOT]-[POST_ROOT]-[COMP_ROOT]

Every chunk except ROOT might be void.


### Polar questions

This is the simplest case of questions which not requires any structured answer but _True_ or _False_.

---------------

* _Barack Obama became president of United States in 2009?_
* _Have you found a name for your dog?_

The corresponding queries as single composite literals will be:

```sh
> In_IN(Become_VBD(Barack_NNP_Obama_NNP(x1), Of_IN(President_NN(x2), United_NNP_States_NNP(x3))), N2009_CD(x4))
> Find_VBD(You_PRP(x1), For_IN(Name_NN(x2), Your_PRP__Dog_NN(x3)))
```

### Who-questions

---------------

* _Who is Donald Trump?_

```sh
> Be_VBZ(x1, Donald_NNP_Trump_NNP(x2))
> Be_VBZ(Donald_NNP_Trump_NNP(x1), x2)
```
* _Who wants to be king?_
```sh
> Want_VBZ_Be_VB(x1, King_NN(x2))
```
* _Who could be the president of United States?_
```sh
> Be_VB(x1, Of_IN(President_NN(x2), United_NNP_States_NNP(x3)))
```
* _Who could it be?_
```sh
> Be_VB(It_PRP(x1), x2)
```
* _Who did you see?_
```sh
> See_VBD(You_PRP(x1), x2)
```

### What-questions

---------------

Copular tenses like "is", "was", "were", although intransitive, identify a subject with an object, thus a likely answer might have subject/object inverted as well.
Each copular verb we want to give such a behaviour, can be defined by changing inside COP_VERB (QA Section) in config.ini.

* _What is a king?_
```sh
> Be_VBZ(x1, King_NN(x2))
> Be_VBZ(King_NN(x1), x2)
```
* _What is located in Nevada?_
```sh
> In_IN(Locate_VBN(__, x2), Nevada_NNP(x3))
```
* _What does Mary want?_
```sh
> Want_VBZ(Mary_NNP(x1), x2)
```


### Where-questions

---------------

Each adverb used for answers attemps can be defined by changing LOC_PREPS (QA Section) in config.ini.

* _Where is the newspaper?_
```sh
> In_IN(Be_VBZ(Newspaper_NN(x1), __), x3)
> At_IN(Be_VBZ(Newspaper_NN(x1), __), x3)
```
* _Where could your brother live?_
```sh
> In_IN(Live_VB(Your_PRP__Brother_NN(x1), __), x3)
> At_IN(Live_VB(Your_PRP__Brother_NN(x1), __), x3)
```
* _Where does your brother live?_
```sh
> In_IN(Live_VBZ(Your_PRP__Brother_NN(x1), __), x3)
> At_IN(Live_VBZ(Your_PRP__Brother_NN(x1), __), x3)
```
* _Where are you looking at?_
```sh
> At_IN(Look_VBG(You_PRP(x1), __), x3)
```

### When-questions

---------------

Each adverb used for answers attemps can be defined by changing TIME_PREPS (QA Section) in config.ini.


* _When is the Thanksgiving?_
```sh
> In_IN(Be_VBZ(Thanksgiving_NNP(x1), __), x3)
```
* _When could your city become a metropolis?_
```sh
> In_IN(Become_VB(Your_PRP__City_NN(x1), Metropolis_NN(x2)), x3)
```
* _When do you want to leave the country?_
```sh
> In_IN(Want_VBP_Leave_VB(You_PRP(x1), Country_NN(x2)), x3)
```