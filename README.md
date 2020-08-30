# AD-CASPAR

This is the repository of the Python (3.7+) implementation of AD-CASPAR (Abductive-Deductive Cognitive Architecture System Planned and Reactive)
referred to the paper _AD-CASPAR: Abductive-Deductive Cognitive Architecture based on Natural Language and First Order Logic Reasoning_. 
This architecture inherits all the features of his predecessor [CASPAR](https://github.com/fabiuslongo/pycaspar), extending them with a 
 two-level Clauses Knowledge Base, an abductive inference as pre-phase of deduction, and a Telegram
chatbot prototype implementing Question Answering tecniques for Polar and Wh-Questions.

![Image 1](https://github.com/fabiuslongo/ad-caspar/blob/master/images/AD-Caspar.jpg)

# Installation


This repository has been tested on Pycharm 2019.1.2 x64 with the following packages versions:

* [Phidias](https://github.com/corradosantoro/phidias) (release 1.3.4.alpha) 
* SpaCy (ver. 2.2.4)
* Natural Language Toolkit (ver. 3.5)
* python-telegram-bot
* [Mongodb](www.mongodb.com)

### Phidias

---------------
##### on all platforms
```sh
> git clone https://github.com/corradosantoro/phidias
> python setup.py install
```
##### additional package needed (Linux)
```sh
> python -pip install readline
> python -pip install parse
```
##### additional package needed (Windows)
```sh
> python -m pip install pyreadline
> python -m pip install parse
```

### SpaCy

---------------

```sh
> python -m pip install spacy
> python -m spacy download en_core_web_md
```


### Natural Language Toolkit

---------------

from prompt:
```sh
> python -m pip install nltk
```
from python console:
```sh
> import nltk
> nltk.download('wordnet')
```

### python-telegram-bot
```sh
> python -m pip python-telegram-bot
```

# Testing
Before going any further it is first necessary to create a new telegram bot by following the instruction
 in this [page](https://core.telegram.org/bots#6-botfather). The returned token must be inserted instead of 
 XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX at line 82 of sensors.py. 


### Starting Phidias Shell

---------------

```sh
> python ad-caspar.py

          PHIDIAS Release 1.3.4.alpha (deepcopy-->clone,micropython,py3)
          Autonomous and Robotic Systems Laboratory
          Department of Mathematics and Informatics
          University of Catania, Italy (santoro@dmi.unict.it)
          
eShell: main >
```
### Starting agent

---------------

```sh
eShell: main > go()
eShell: main > AD-Caspar started! Bot is running...
```

