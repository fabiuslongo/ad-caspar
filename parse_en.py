import spacy
import platform
import os
from collections import Counter
from nltk.corpus import wordnet
import configparser
import itertools
import time


config = configparser.ConfigParser()
config.read('config.ini')

DIS_ACTIVE = config.getboolean('DISAMBIGUATION', 'DIS_ACTIVE')
DIS_VERB = config.get('DISAMBIGUATION', 'DIS_VERB').split(", ")
DIS_NOUN = config.get('DISAMBIGUATION', 'DIS_NOUN').split(", ")
DIS_ADJ = config.get('DISAMBIGUATION', 'DIS_ADJ').split(", ")
DIS_ADV = config.get('DISAMBIGUATION', 'DIS_ADV').split(", ")
DIS_EXCEPTIONS = config.get('DISAMBIGUATION', 'DIS_EXCEPTIONS').split(", ")
DIS_METRIC_COMPARISON = config.get('DISAMBIGUATION', 'DIS_METRIC_COMPARISON')
GMC_ACTIVE = config.getboolean('GROUNDED_MEANING_CONTEXT', 'GMC_ACTIVE')
GMC_POS = config.get('GROUNDED_MEANING_CONTEXT', 'GMC_POS').split(", ")

OBJ_JJ_TO_NOUN = config.getboolean('POS', 'OBJ_JJ_TO_NOUN')







class Parse(object):
    def __init__(self, VERBOSE):

        self.FILTER = ['det', 'punct', 'aux', 'auxpass', 'cc', 'case', 'intj', 'dep', 'predet', 'advcl']

        self.adv_adj_POS = ['RB', 'UH', 'RP', 'PRP', 'RBS', 'JJ', 'NN', 'RBR', 'DT']

        self.POS_FILTER = []

        self.VERBOSE = VERBOSE

        self.BLACK_LIST_WORDS = ['that', 'which', 'then']

        # nlp engine instantiation
        print("\nNLP engine initializing. Please wait...")

        # python -m spacy download en_core_web_md
        #self.nlp = spacy.load('en_core_web_md')  # 91 MB

        # python -m spacy download en_core_web_lg
        self.nlp = spacy.load('en_core_web_lg')  # 789 MB

        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')

        # enable cache usage
        self.FLUSH = True

        # last dependencies
        self.last_deps = []

        # last detected entities
        self.ner = []

        # last processed sentence
        self.last_sentence = None

        # last processed sentence
        self.pending_root_tense_debt = None

        # novel deps usage
        self.last_enc_deps = []

        # offset dictionary
        self.offset_dict = {}

        # Macro Semantic Table
        self.MST = [[], [], [], [], [], []]

        # GMC support dictionary
        self.GMC_SUPP = {}

        # GMC support dictionary reversed
        self.GMC_SUPP_REV = {}

        # Lemmas correction dictionary
        self.LCD = {}

        self.cnt = itertools.count(1)
        self.dav = itertools.count(1)

        # Beginning Computational time
        self.start_time = 0



    def set_start_time(self):
        self.start_time = time.time()


    def get_comp_time(self):
        end_time = time.time()
        assert_time = end_time - self.start_time
        return assert_time


    def Iterator_init(self):
        self.cnt = itertools.count(1)
        self.dav = itertools.count(1)


    def Iterator_next_dav(self):
        return(next(self.dav))


    def Iterator_next_var(self):
        return(next(self.cnt))


    def feed_MST(self, component, index):
        self.MST[index].append(component)


    def get_last_MST(self):
        return self.MST


    def get_pending_root_tense_debt(self):
        return self.pending_root_tense_debt

    def set_pending_root_tense_debt(self, d):
        self.pending_root_tense_debt = d

    def get_last_sentence(self):
        return self.last_sentence


    def get_last_ner(self):
        return self.ner


    def set_last_deps(self, deps):
        self.last_deps = deps


    def get_last_deps(self):
        return self.last_deps


    def get_flush(self):
        return self.FLUSH


    def flush(self):
        self.FLUSH = True
        self.last_deps = []
        self.ner = []
        self.MST = [[], [], [], [], [], []]


    def no_flush(self):
        self.FLUSH = False


    def get_nlp_engine(self):
        return self.nlp



    def get_pos(self, s):
        s_list = s.split(':')
        if len(s_list) > 1:
            return s_list[1]
        else:
            return s_list[0]


    def get_lemma(self, s):
        s_list = s.split('_')
        if len(s_list) == 1:
            result = s_list[0].split(":")[0]
        else:
            result = ""
            for i in range(len(s_list)):
                if i == 0:
                    result = s_list[i].split(':')[0]
                else:
                    result = result +"_"+s_list[i].split(':')[0]
        return result


    def get_enc_deps(self, input_text):

        nlp = self.get_nlp_engine()
        doc = nlp(input_text)
        self.last_sentence = input_text

        enc_deps = []
        offset_dict = {}

        for token in doc:
            enc_dep = []
            enc_dep.append(token.dep_)
            #enc_dep.append(token.head.idx)
            enc_dep.append(token.head.text)

            offset_dict[token.idx] = token.head.text

            #enc_dep.append(token.idx)
            enc_dep.append(token.text)

            offset_dict[token.idx] = token.text

            enc_deps.append(enc_dep)

        self.offset_dict = offset_dict

        return enc_deps



    def get_deps(self, input_text, LEMMATIZED):

        nlp = self.get_nlp_engine()
        doc = nlp(input_text)
        self.last_sentence = input_text

        for X in doc.ents:
            ent = "("+X.label_ + ", " + X.text + ")"
            self.ner.append(ent)

        words_list = []
        for token in doc:
            words_list.append(token.text)

            enc_dep = []
            enc_dep.append(token.dep_)
            enc_dep.append(token.head.idx)
            enc_dep.append(token.idx)


        counter = Counter(words_list)

        offset_dict = {}
        offset_dict_lemmatized = {}


        for token in reversed(doc):
            index = counter[token.text]

            print("\nlemma in exam: ", token.lemma_)

            # check for presence in Grounded Meaning Context (GMC). In this case the choosen synset must be that in GMC, already found
            if GMC_ACTIVE is True and token.tag_ in GMC_POS and token.lemma_ in self.GMC_SUPP:

                offset_dict[token.idx] = token.text + "0" + str(index) + ":" + token.tag_
                shrinked_proper_syn = self.GMC_SUPP[token.lemma_]
                offset_dict_lemmatized[token.idx] = shrinked_proper_syn + "0" + str(index) + ":" + token.tag_

                print("\n<--------------- Getting from GMC: "+token.text+" ("+shrinked_proper_syn+")")

            # Otherwise a proper synset must be inferred....
            elif DIS_ACTIVE and (token.tag_ in DIS_VERB or token.tag_ in DIS_NOUN or token.tag_ in DIS_ADJ or token.tag_ in DIS_ADV) and token.lemma_ not in DIS_EXCEPTIONS:

                if token.tag_ in DIS_VERB:
                    pos = wordnet.VERB
                elif token.tag_ in DIS_NOUN:
                    pos = wordnet.NOUN
                elif token.tag_ in DIS_ADV:
                    pos = wordnet.ADV
                else:
                    pos = wordnet.ADJ

                # pos=VERB, NOUN, ADJ, ADV
                syns = wordnet.synsets(token.text, pos=pos, lang="eng")

                proper_syn = ""
                proper_syn_sim = 0
                proper_definition = ""
                source = ""

                for synset in syns:
                    #print("\nsynset: ", synset.name())
                    #print("#synset examples: ", len(synset.examples()))

                    # Checking vect distance from glosses
                    if DIS_METRIC_COMPARISON == "GLOSS" or len(synset.examples()) == 0:
                        doc2 = nlp(synset.definition())
                        sim = doc.similarity(doc2)

                        if sim > proper_syn_sim:
                            proper_syn_sim = sim
                            proper_syn = synset.name()
                            proper_definition = synset.definition()
                            source = "GLOSS"

                    elif DIS_METRIC_COMPARISON == "EXAMPLES":

                        # Checking vect distances from examples (wether existing)
                        for example in synset.examples():
                            doc2 = nlp(example)
                            sim = doc.similarity(doc2)

                            if sim > proper_syn_sim:
                                proper_syn_sim = sim
                                proper_syn = synset.name()
                                proper_definition = synset.definition()
                                source = "EXAMPLES"

                    elif DIS_METRIC_COMPARISON == "BEST":

                        # Checking best vect distances between gloss and examples
                        for example in synset.examples():
                            doc2 = nlp(example)
                            sim1 = doc.similarity(doc2)

                            if sim1 > proper_syn_sim:
                                proper_syn_sim = sim1
                                proper_syn = synset.name()
                                proper_definition = synset.definition()
                                source = "BEST-example"

                        doc2 = nlp(synset.definition())
                        sim2 = doc.similarity(doc2)

                        if sim2 > proper_syn_sim:
                            proper_syn_sim = sim2
                            proper_syn = synset.name()
                            proper_definition = synset.definition()
                            source = "BEST-gloss"

                    elif DIS_METRIC_COMPARISON == "AVERAGE":

                        # AVERAGE = average between doc2vect gloss and examples
                        actual_sim1 = 0
                        source = "AVERAGE"

                        for example in synset.examples():
                            doc2 = nlp(example)
                            sim1 = doc.similarity(doc2)

                            if sim1 > actual_sim1:
                                actual_sim1 = sim1

                        doc2 = nlp(synset.definition())
                        sim2 = doc.similarity(doc2)
                        average = (actual_sim1 + sim2) / 2

                        if average > proper_syn_sim:
                            proper_syn_sim = average
                            proper_syn = synset.name()
                            proper_definition = synset.definition()

                    else:
                        # COMBINED = similarity between doc2vect gloss+examples
                        source = "COMBINED"

                        for example in synset.examples():
                            combined = str(synset.definition())+" "+example
                            doc2 = nlp(combined)
                            sim1 = doc.similarity(doc2)

                            if sim1 > proper_syn_sim:
                                proper_syn_sim = sim1
                                proper_syn = synset.name()
                                proper_definition = synset.definition()


                print("\nProper syn: ", proper_syn)
                print("Max sim: ", proper_syn_sim)
                print("Gloss: ", proper_definition)
                print("Source: ", source)

                shrinked_proper_syn = self.shrink(proper_syn)

                self.GMC_SUPP[token.lemma_] = shrinked_proper_syn
                print("\n--------------> Storing in GCM: "+token.lemma_+" ("+shrinked_proper_syn+")")
                self.GMC_SUPP_REV[shrinked_proper_syn] = token.lemma_

                if OBJ_JJ_TO_NOUN is True:
                    # taking in account of possible past adj-obj corrections
                    lemma = str(token.lemma_).lower()
                    if lemma in self.LCD:
                        shrinked_proper_syn = self.LCD[lemma]
                        print("\n<------------- Getting from LCD: "+shrinked_proper_syn+" ("+lemma+")")

                offset_dict_lemmatized[token.idx] = shrinked_proper_syn + "0" + str(index) + ":" + token.tag_
                offset_dict[token.idx] = token.text + "0" + str(index) + ":" + token.tag_

            else:

                lemma = str(token.lemma_).lower()

                # taking in account of possible past adj-obj corrections
                if OBJ_JJ_TO_NOUN is True and lemma in self.LCD:
                    lemma = self.LCD[lemma]
                    print("\n<------------- Getting from LCD: ", lemma)

                offset_dict[token.idx] = token.text+"0"+str(index)+":"+token.tag_
                offset_dict_lemmatized[token.idx] = lemma+"0"+str(index)+":"+token.tag_

            counter[token.text] = index - 1


        deps = []
        for token in doc:
            new_triple = []
            new_triple.append(token.dep_)

            if token.head.lemma_ == '-PRON-':
                new_triple.append(offset_dict[token.head.idx])
            else:
                if LEMMATIZED:
                    new_triple.append(offset_dict_lemmatized[token.head.idx])
                else:
                    new_triple.append(offset_dict[token.head.idx])

            if token.lemma_ == '-PRON-':
                new_triple.append(offset_dict[token.idx])
            else:
                if LEMMATIZED:
                    new_triple.append(offset_dict_lemmatized[token.idx])
                else:
                    new_triple.append(offset_dict[token.idx])

            deps.append(new_triple)

        # query accomodation
        if LEMMATIZED:
            for d in deps:
                if d[2][0:5].lower() == "dummy":
                    d[2] = "Dummy:DM"

            for i in range(len(deps)):
                governor = self.get_lemma(deps[i][1]).capitalize() + ":" + self.get_pos(deps[i][1])
                dependent = self.get_lemma(deps[i][2]).capitalize() + ":" + self.get_pos(deps[i][2])
                deps[i] = [deps[i][0], governor, dependent]


        return deps


    def morph(self, sent):
        sent_changed = ""
        for c in sent:
            if c in [':', '$', '.']:
                sent_changed = sent_changed + "_"
            else:
                sent_changed = sent_changed + c
        final_sent_changed = ""
        sent_changed_splitted = sent_changed.split(" ")
        for i in range(len(sent_changed_splitted)):
            if sent_changed_splitted[i][0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                if i == 0:
                    final_sent_changed = "N" + sent_changed_splitted[i]
                else:
                    final_sent_changed = final_sent_changed + " N" + sent_changed_splitted[i]
            else:
                if i == 0:
                    final_sent_changed = sent_changed_splitted[i]
                else:
                    final_sent_changed = final_sent_changed + " " + sent_changed_splitted[i]

        return final_sent_changed


    def shrink(self, word):
        chunk_list = word.split("_")
        sw = ""
        for chunk in chunk_list:
            sw = sw + chunk
        return sw



def main():
    VERBOSE = True

    parser = Parse(VERBOSE)

    LEMMMATIZED = True
    sentence = "The world is yours"
    deps = parser.get_deps(sentence, LEMMMATIZED)
    parser.set_last_deps(deps)
    ner = parser.get_last_ner()
    print("\nner: ", ner)

    print("\n" + str(deps))

    """
    MST = parser.create_MST(deps, 'e', 'x')
    print("\nMST: \n" + str(MST))
    """




if __name__ == "__main__":
    main()








