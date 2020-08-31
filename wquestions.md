# Questions capabilities overview

In this file is shown how AD-CASPAR deals with Polar and Wh-questions, by the means of the module qa_shifter.py. The latter
works is a parser based on production rules, which works considering lexical rule to shit a question into a possible assertion.
Every question, by leveraging its dependencies, is divided into chunks as it follows:

[PRE_AUX], [AUX], [POST_AUX], [ROOT], [POST_ROOT], [COMP_ROOT]




### Polar questions

This is the simplest case of questions which not requires any structured answer but _True_ or _False_.

---------------

* _Barack Obama became president of United States in 2009?_
* _Have you found a name for your dog?_

The corresponding queries as single composite literals will be:

* In_IN(Become_VBD(Barack_NNP_Obama_NNP(x1), Of_IN(President_NN(x2), United_NNP_States_NNP(x3))), N2009_CD(x4))
* Find_VBD(You_PRP(x1), For_IN(Name_NN(x2), Your_PRP__Dog_NN(x3)))


### Who-questions

---------------

* Who is Donald Trump?
* Who wants to be king?
* Who could be the president of United States?
* Who could it be?
* Who did you see?

### What-questions

---------------

* What is a king?
* What is located in Nevada?
* What does Mary want?
* What movies have you seen recently?
* What qualities do you think are important in a friend?

### Where-questions

---------------

* Where is the newspaper?
* Where could your brother live?
* where does your brother live?
* Where are you looking at?

### When-questions

---------------

* When is the Thanksgiving?
* When could your city become a metropolis?
* when do you want to leave the country?