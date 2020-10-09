import spacy
import platform
import os
from collections import Counter


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

        # last uniquezed dependencies
        self.last_m_deps = []

        # last detected entities
        self.ner = []

        # last processed sentence
        self.last_sentence = None

        # last processed sentence
        self.pending_root_tense_debt = None


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
        self.last_m_deps = []
        self.ner = []


    def no_flush(self):
        self.FLUSH = False


    def get_nlp_engine(self):
        return self.nlp


    def create_MST(self, deps, dav, var):

        index_args_counter = 0
        davidsonian_index = 0

        pending_prep = []
        preps = []
        mods = []
        compounds = []

        pendings = []
        var_list = []

        cond = []
        adv_adj = []

        pending_agent = []
        pending_prt = []

        for triple in deps:
            if triple[0] not in self.FILTER and triple[0] != "ROOT":

                # noun subjects
                if triple[0] == "nsubj":

                    PENDING_FOUND = False

                    # looking for a pending
                    for p in pendings:
                        if triple[1] == p[0]:
                            PENDING_FOUND = True

                            index_args_counter = index_args_counter + 1
                            p[2] = var + str(index_args_counter)

                            assignment = []
                            assignment.append(var + str(index_args_counter))
                            assignment.append(triple[2])

                            var_list.append(assignment)

                    if PENDING_FOUND == False:

                        # creating a pending

                        p = []
                        p.append(triple[1])

                        davidsonian_index = davidsonian_index + 1
                        p.append(dav+str(davidsonian_index))

                        index_args_counter = index_args_counter + 1
                        p.append(var+str(index_args_counter))

                        assignment = []
                        assignment.append(var+str(index_args_counter))

                        assignment.append(triple[2])
                        var_list.append(assignment)

                        index_args_counter = index_args_counter + 1
                        p.append(var + str(index_args_counter))

                        assignment = []
                        assignment.append(var+str(index_args_counter))

                        assignment.append('?')
                        var_list.append(assignment)

                        pendings.append(p)

                    if self.VERBOSE is True:
                        print('--------- nsubj ----------')
                        print('pendings: ' + str(pendings))
                        print('pending_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                # noun subjects passive
                elif triple[0] == "nsubjpass":

                    PENDING_FOUND = False

                    # looking for a pending
                    for p in pendings:
                        if triple[1] == p[0]:
                            PENDING_FOUND = True

                            index_args_counter = index_args_counter + 1
                            p[2] = var + str(index_args_counter)

                            assignment = []
                            assignment.append(var + str(index_args_counter))
                            assignment.append(triple[2])

                            var_list.append(assignment)

                    if PENDING_FOUND == False:

                        # creating a pending

                        p = []
                        p.append(triple[1])

                        davidsonian_index = davidsonian_index + 1
                        p.append(dav+str(davidsonian_index))

                        index_args_counter = index_args_counter + 1
                        p.append(var+str(index_args_counter))

                        assignment = []
                        assignment.append(var+str(index_args_counter))

                        assignment.append('?')
                        var_list.append(assignment)

                        index_args_counter = index_args_counter + 1
                        p.append(var + str(index_args_counter))

                        assignment = []
                        assignment.append(var+str(index_args_counter))

                        assignment.append(triple[2])
                        var_list.append(assignment)

                        pendings.append(p)

                    if self.VERBOSE is True:
                        print('--------- nsubjpass ----------')
                        print('pendings: ' + str(pendings))
                        print('pending_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                # expletive existentials (there) in the subject position.
                elif triple[0] == "expl":

                    # creating a pending

                    p = []
                    p.append(triple[1])

                    davidsonian_index = davidsonian_index + 1
                    p.append(dav+str(davidsonian_index))

                    # void variable for intransitive verb mode
                    p.append('_')

                    # second variable void
                    index_args_counter = index_args_counter + 1
                    p.append(var+str(index_args_counter))
                    assignment = []
                    assignment.append(var+str(index_args_counter))
                    assignment.append('?')
                    var_list.append(assignment)

                    pendings.append(p)

                    if self.VERBOSE is True:
                        print('--------- expl ----------')
                        print('pendings: ' + str(pendings))
                        print('pending_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                # clausal subjects
                elif triple[0] == "csubj":

                    davidsonian_found = "UNASSIGNED"

                    # retriving dependent-related davidsonian

                    for p in pendings:
                        if p[0] == triple[2]:
                            davidsonian_found = p[1]

                    p = []
                    p.append(triple[1])

                    davidsonian_index = davidsonian_index + 1
                    p.append(dav+str(davidsonian_index))

                    # setting retrived davidsonian
                    p.append(davidsonian_found)

                    index_args_counter = index_args_counter + 1
                    p.append(var+str(index_args_counter))
                    pendings.append(p)

                    assignment = []
                    assignment.append(var+str(index_args_counter))
                    assignment.append('?')

                    var_list.append(assignment)

                    if self.VERBOSE is True:
                        print('--------- csubj ----------')
                        print('pendings: ' + str(pendings))
                        print('pending_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                # parenthetical modifiers
                elif triple[0] == "parataxis":

                    davidsonian_found = "UNASSIGNED"
                    PENDING_FOUND = False

                    # retriving dependent-related davidsonian
                    for p in pendings:
                        if self.get_first_token(p[0]) == triple[1]:
                            davidsonian_found = p[1]
                            PENDING_FOUND = True

                    if PENDING_FOUND:
                        # retriving governor pending for setting davidsonian as object
                        for p in pendings:
                            if self.get_first_token(p[0]) == triple[2]:
                                p[3] = davidsonian_found

                    if self.VERBOSE is True:
                        print('--------- csubj ----------')
                        print('pendings: ' + str(pendings))
                        print('pending_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                # clausal complements
                elif triple[0] == "ccomp":

                    davidsonian_found = "UNASSIGNED"
                    PENDING_FOUND = False
                    DOBJECT_FOUND = False

                    # retriving dependent-related davidsonian
                    for p in pendings:
                        if self.get_first_token(p[0]) == triple[2]:
                            davidsonian_found = p[1]
                            PENDING_FOUND = True

                        # accomodation for dealing with "What", "When" questions
                        if self.get_first_token(p[0]) == triple[1] and triple[2][:-5] in ["What", "When", "Who"]:
                            DOBJECT_FOUND = True
                            assignment = []
                            assignment.append(var + str(index_args_counter))
                            assignment.append(triple[2])
                            var_list.append(assignment)
                            p[3] = var + str(index_args_counter)
                            index_args_counter = index_args_counter + 1

                    if DOBJECT_FOUND:
                       pass

                    elif PENDING_FOUND:
                        # retriving governor pending for setting davidsonian as object
                        for p in pendings:
                            if self.get_first_token(p[0]) == triple[1]:
                                p[3] = davidsonian_found
                    else:
                        # creating a pending

                        p = []
                        p.append(triple[2])

                        davidsonian_index = davidsonian_index + 1
                        p.append(dav + str(davidsonian_index))

                        index_args_counter = index_args_counter + 1
                        p.append(var + str(index_args_counter))

                        assignment = []
                        assignment.append(var + str(index_args_counter))

                        assignment.append('?')
                        var_list.append(assignment)

                        index_args_counter = index_args_counter + 1
                        p.append(var + str(index_args_counter))

                        assignment = []
                        assignment.append(var + str(index_args_counter))

                        assignment.append('?')
                        var_list.append(assignment)

                        pendings.append(p)

                    if self.VERBOSE is True:
                        print('--------- ccomp ----------')
                        print('pendings: ' + str(pendings))
                        print('pending_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                # Clausal modifiers of noun
                elif triple[0] == "acl":

                    PENDING_FOUND = False
                    variation = "UNASSIGNED"
                    VAR_FOUND = False

                    # the new object of a pending become triple[1]

                    # searching and storing the variable linked to triple[1], if exists
                    for v in var_list:
                        if triple[1] == v[1]:
                            variation = v[0]
                            VAR_FOUND = True


                    # searching (and changing) the pending's subject related to triple[2]
                    for p in pendings:
                        if self.get_first_token(p[0]) == triple[2]:
                            PENDING_FOUND = True
                            if VAR_FOUND == True:
                                p[3] = variation
                            else:
                                var_to_change = p[3]
                                for v in var_list:
                                    if v[0] == var_to_change:
                                        v[1] = triple[1]

                    if PENDING_FOUND is False:

                        # creating new pending with triple[1] as object

                        p = []
                        p.append(triple[2])

                        davidsonian_index = davidsonian_index + 1
                        p.append(dav+str(davidsonian_index))

                        p.append(variation)

                        index_args_counter = index_args_counter + 1
                        p.append(var+str(index_args_counter))

                        assignment = []
                        assignment.append(var+str(index_args_counter))
                        assignment.append('?')
                        var_list.append(assignment)

                        pendings.append(p)

                    if self.VERBOSE is True:
                        print('--------- acl ----------')
                        print('pendings: ' + str(pendings))
                        print('pending_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                # Relative clause modifiers
                elif triple[0] == "relcl":

                    PENDING_FOUND = False
                    related_var = "UNASSIGNED"
                    related_davidsonian = "UNASSIGNED"


                    subj = "UNASSIGNED"
                    obj = "UNASSIGNED"

                    subj_val = "UNASSIGNED"
                    obj_val = "UNASSIGNED"

                    VAR_USED = False

                    # the new subject/object of a pending become triple[1]'s related

                    # getting davisdonian, subj and obj of triple[2]
                    for p in pendings:
                        if self.get_first_token(p[0]) == triple[2]:
                            related_davidsonian = p[1]
                            subj = p[2]
                            obj = p[3]

                    # getting triple[1]'s related variable
                    for v in var_list:
                        if v[1] == triple[1]:
                            related_var = v[0]
                        if v[0] == subj:
                            subj_val = v[1]
                        if v[0] == obj:
                            obj_val = v[1]

                    for prep in preps:
                        if related_var in prep:
                            VAR_USED = True

                    if VAR_USED is False:
                        # searching (and changing) the pending's subject/object related to triple[2]
                        for p in pendings:
                            if p[1] == related_davidsonian:
                                if self.get_pos(triple[2]) == "VBN":
                                        p[3] = related_var
                                else:
                                        if self.get_pos(subj_val) not in ["PRP", "NN", "NNP", "NNPS"]:
                                            p[2] = related_var
                                        else:
                                            p[3] = related_var
                                PENDING_FOUND = True


                    if PENDING_FOUND is False and VAR_USED is False:
                        # creating new pending with triple[1] as subject

                        p = []
                        p.append(triple[2])

                        davidsonian_index = davidsonian_index + 1
                        p.append(dav+str(davidsonian_index))

                        p.append(related_var)

                        index_args_counter = index_args_counter + 1
                        p.append(var+str(index_args_counter))

                        assignment = []
                        assignment.append(var+str(index_args_counter))
                        assignment.append('?')
                        var_list.append(assignment)

                        pendings.append(p)

                    if self.VERBOSE is True:
                        print('--------- relcl ----------'+str(triple))
                        print('pendings: ' + str(pendings))
                        print('pending_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                # direct objects
                elif triple[0] == "dobj":

                    PENDING_FOUND = False

                    # updating var_list

                    for p in pendings:
                        if self.get_first_token(p[0]) == triple[1]:
                            pendings_object_found = p[3]
                            PENDING_FOUND = True
                            for v in var_list:
                                if v[0] == pendings_object_found:
                                    if v[1] == '?':
                                        v[1] = triple[2]

                    # imperative case

                    if PENDING_FOUND == False:

                        p = []

                        p.append(triple[1])

                        davidsonian_index = davidsonian_index + 1
                        p.append(dav+ str(davidsonian_index))

                        p.append('_')

                        index_args_counter = index_args_counter + 1
                        p.append(var+str(index_args_counter))

                        assignment = []
                        assignment.append(var+str(index_args_counter))
                        assignment.append(triple[2])
                        var_list.append(assignment)

                        pendings.append(p)

                        prt_found = False

                        for prt in pending_prt:
                            if prt[0] == triple[1]:
                               particle = prt[1]
                               prt_found = True

                        if prt_found is True:
                            for v in var_list:
                                if v[1] == particle:
                                    v[0] = dav+str(davidsonian_index)


                    if self.VERBOSE is True:
                        print('--------- dobj ----------')
                        print('pendings: ' + str(pendings))
                        print('pending_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                # attribute or adjectival complements
                elif triple[0] in ["attr", "acomp"]:

                    # updating var_list
                    var_to_change = 'UNASSIGNED'

                    for p in pendings:
                        if self.get_first_token(p[0]) == triple[1]:
                            var_to_change = p[3]

                    for v in var_list:
                        if v[0] == var_to_change:
                            v[1] = triple[2]

                    if self.VERBOSE is True:
                        print('--------- attr-acomp ----------')
                        print('pendings: ' + str(pendings))
                        print('pending_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                # prepositional modifiers
                elif triple[0] == "prep":

                    davidsonian_found = triple[1]
                    found_var = triple[1]
                    found_mod = "UNASSIGNED"
                    d_found = False

                    pending_prep.append(triple[2])

                    # searching triple[1] in pendings

                    for p in pendings:
                        if self.get_first_token(p[0]) == triple[1] or self.get_first_token(p[0]) == found_mod:
                            davidsonian_found = p[1]
                            d_found = True

                    # searching triple[1] in mods --- case oprd

                    if d_found is False:
                        for m in mods:
                            if m[1] == triple[1]:
                                found_mod = m[0]

                        for v in var_list:
                            if v[1] == found_mod:
                                found_var = v[0]

                        for p in pendings:
                            # case var
                            if p[3] == found_var:
                                davidsonian_found = p[1]
                                d_found = True
                            # case verb
                            if p[0] == found_mod:
                                davidsonian_found = p[1]
                                d_found = True

                    # searching triple[1] in compounds

                    if d_found is False:
                        for m in mods:
                            if m[1] == triple[1]:
                                found_mod = m[0]
                        for v in var_list:
                            if v[1] == found_mod:
                                found_var = v[0]
                        for p in pendings:
                            if p[3] == found_var:
                                davidsonian_found = p[1]
                                d_found = True

                    # searching triple[1] in adv_adj

                    if d_found is False:
                        for v in adv_adj:
                            if v[1] == triple[1]:
                                for p in pendings:
                                    if self.get_first_token(p[0]) == v[0]:
                                        davidsonian_found = p[1]
                                        d_found = True

                    if d_found is False:

                        # retriving triple[1] from var_list

                        for v in var_list:
                            if v[1] == triple[1]:
                                found_var = v[0]

                        # retriving related davidsonian from pendings and preps table

                        for prep in preps:
                            if prep[2] == found_var:
                                davidsonian_found = prep[1]

                        for p in pendings:
                            if p[3] == found_var or p[2] == found_var:
                                davidsonian_found = p[1]


                    # retriving from parent prep
                    if d_found is False:
                        for prep in preps:
                            if triple[1] == prep[0]:
                                found_var = prep[1]

                    # case example: of:IN(e1, x5)
                    if found_var == 'UNASSIGNED':
                        pending_prep.append(davidsonian_found)
                    else:
                        pending_prep.append(found_var)

                    # updating var_list

                    index_args_counter = index_args_counter + 1
                    assignment = []
                    assignment.append(var + str(index_args_counter))
                    assignment.append('?')
                    var_list.append(assignment)

                    pending_prep.append(var + str(index_args_counter))

                    if self.VERBOSE is True:
                        print('--------- prep ----------')
                        print('pendings: ' + str(pendings))
                        print('pending_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                # agents
                elif triple[0] == "agent":

                    pending_agent.append(triple[1])
                    for p in pendings:
                        if p[0] == triple[1]:
                            pending_agent.append(p[1])

                    if self.VERBOSE is True:
                        print('--------- agent ----------')
                        print('pending_agent: ' + str(pending_agent))

                # object/complement of prepositions
                elif triple[0] in ["pobj", "pcomp"]:

                    # updating var_list

                    var_to_change = ""

                    # looking for pending preps...

                    if len(pending_prep) > 0:
                        if triple[1] == pending_prep[0]:
                            for v in var_list:
                                if v[0] == pending_prep[2]:
                                    v[1] = triple[2]

                        preps.append(pending_prep)
                        pending_prep = []

                    # looking for pending agents...

                    VAR_CHANGED = False
                    subj = "UNASSIGNED"
                    obj = "UNASSIGNED"

                    if len(pending_agent) > 0:
                        # retriving related pending var
                        for p in pendings:
                            if p[0] == pending_agent[0]:
                                subj = p[2]
                                obj = p[3]

                        # retriving related pending val
                        for v in var_list:
                            if v[0] == subj:
                                if v[1] == '?':
                                    v[1] = triple[2]
                                    VAR_CHANGED = True
                            if VAR_CHANGED is False and v[0] == obj:
                                if v[1] == '?':
                                   v[1] = triple[2]
                        pending_agent = []

                    if self.VERBOSE is True:
                        print('--------- pobj ----------')
                        print('pendings: ' + str(pendings))
                        print('pending_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                # open clausal complements or adverbial clause modifiers
                elif triple[0] in ["xcomp", "advcl"]:

                    PENDING_FOUND = False
                    PAST_PART_CASE = False
                    object = "UNASSIGNED"

                    #concatenate triple[2] to triple[1] related pending
                    for pend in pendings:
                        if self.get_first_token(pend[0]) == triple[1]:
                            PENDING_FOUND = True
                            if self.get_pos(triple[1]) != "VBN":
                                pend[0] = triple[2]+'_'+pend[0]
                            else:
                                # past participle case
                                PAST_PART_CASE = True
                                object = pend[3]

                    if PENDING_FOUND is False:

                        p = []
                        p.append(triple[2]+"_"+triple[1])

                        davidsonian_index = davidsonian_index + 1
                        p.append(dav + str(davidsonian_index))

                        # void subject
                        index_args_counter = index_args_counter + 1
                        p.append(var + str(index_args_counter))

                        assignment = []
                        assignment.append(var + str(index_args_counter))
                        assignment.append('?')
                        var_list.append(assignment)

                        # void object
                        index_args_counter = index_args_counter + 1
                        p.append(var + str(index_args_counter))

                        assignment = []
                        assignment.append(var + str(index_args_counter))
                        assignment.append('?')
                        var_list.append(assignment)

                        pendings.append(p)

                    elif PAST_PART_CASE:

                        p = []

                        p.append(triple[2])

                        davidsonian_index = davidsonian_index + 1
                        p.append(dav + str(davidsonian_index))

                        p.append(object)

                        index_args_counter = index_args_counter + 1
                        p.append(var + str(index_args_counter))

                        assignment = []
                        assignment.append(var + str(index_args_counter))
                        assignment.append('?')
                        var_list.append(assignment)

                        pendings.append(p)

                        prt_found = False

                        for prt in pending_prt:
                            if prt[0] == triple[2]:
                                particle = prt[1]
                                prt_found = True

                        if prt_found is True:
                            for v in var_list:
                                if v[1] == particle:
                                    v[0] = dav + str(davidsonian_index)

                    if self.VERBOSE is True:
                        print('--------- xcomp/advcl? ----------')
                        print('pendings: ' + str(pendings))
                        print('pending_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                # object predicates
                elif triple[0] == "oprd":

                    var_found = "UNASSIGNED"
                    VAR_CHANGED = False

                    # creating a mod for the predicate of a verb object

                    m = []
                    for p in pendings:
                        if p[0] == triple[1]:
                            var_found = p[3]

                    for v in var_list:
                        if v[0] == var_found:
                            if v[1] == '?':
                                VAR_CHANGED = True
                                v[1] = triple[2]
                            else:
                                m.append(v[1])

                    if VAR_CHANGED is False:
                        m.append(triple[2])
                        mods.append(m)

                    # rectifing mods vector
                    for m_est in mods:
                        for v in var_list:
                            if v[1] == m_est[0]:
                                for m_int in mods:
                                    if m_int[0] == m_est[1]:
                                        m_int[0] = v[1]


                    if self.VERBOSE is True:
                        print('--------- oprd ----------')
                        print('pendings: ' + str(pendings))
                        print('pending_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                # adjectival/possession/number/noun phrase as adverbial/appositional/quantifier modifiers
                elif triple[0] in ["amod", "poss", "nummod", "nmod", "appos", "quantmod"]:

                    m = []
                    m.append(triple[1])
                    m.append(triple[2])
                    mods.append(m)

                    # rectifing bindings vector
                    for mod in mods:
                        if mod[0] == triple[2]:
                            mod[0] = triple[1]

                    # rectifing adv_adj vector
                        for adv in adv_adj:
                            if adv[0] == triple[2]:
                                adv[0] = triple[1]

                    if self.VERBOSE is True:
                        print('--------- amod ----------')
                        print('pendings: ' + str(pendings))
                        print('pending_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                # compound modifiers
                elif triple[0] == "compound":

                    new_compound = []
                    new_compound.append(triple[1])
                    new_compound.append(triple[2])
                    compounds.append(new_compound)

                    # rectifing compounds
                    for cmp in compounds:
                        for cmp2 in compounds:
                            if cmp[1] == cmp2[0]:
                                cmp2[0] = cmp[0]

                    if self.VERBOSE is True:
                        print('--------- compound ----------')
                        print('pendings: ' + str(pendings))
                        print('pendings_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                # conjuncts
                elif triple[0] == "conj":

                    #dealing with not:RB case classified inside a conj

                    if self.get_pos(triple[1]) in self.adv_adj_POS and self.get_pos(triple[2]) in self.adv_adj_POS:

                        # firstly adverb assumed to be cond

                        m = []
                        m.append(triple[1])
                        m.append(triple[2])
                        adv_adj.append(m)
                        new_mod = []

                        # rectifing adv_adj vector
                        for adv in adv_adj:
                            for adv2 in adv_adj:
                                if adv[1] == adv2[0]:
                                    adv2[0] = adv[0]
                    else:

                        found_mod = False

                        # searching into var_list
                        for v in var_list:
                            if v[1] == triple[1]:
                                new_mod = []
                                new_mod.append(v[1])
                                new_mod.append(triple[2])
                                found_mod = True

                        # searching into mods

                        if found_mod is False:
                           for m in mods:
                                if m[0] == triple[1] or m[1] == triple[1]:
                                    new_mod = []
                                    new_mod.append(m[0])
                                    new_mod.append(triple[2])
                                    found_mod = True

                        if found_mod is True:
                            mods.append(new_mod)
                        else:
                            new_mod = []
                            new_mod.append(triple[1])
                            new_mod.append(triple[2])
                            mods.append(new_mod)

                        # rectifing bindings vector
                        for mod in mods:
                            if mod[0] == triple[2]:
                                mod[0] = triple[1]

                    if self.VERBOSE is True:
                        print('--------- conj ----------')
                        print('pendings: ' + str(pendings))
                        print('pending_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                # particles
                elif triple[0] == "prt":

                    PENDING_FOUND = False

                    for pend in pendings:
                        if self.get_first_token(pend[0]) == triple[1]:
                            v = []
                            v.append(pend[1])
                            v.append(triple[2])
                            var_list.append(v)
                            PENDING_FOUND = True

                    if PENDING_FOUND is False:
                        # create an unreferrenced var
                        v = []
                        v.append('?')
                        v.append(triple[2])
                        var_list.append(v)

                        #create a pending prt
                        prt = []
                        prt.append(triple[1])
                        prt.append(triple[2])
                        pending_prt.append(prt)


                    if self.VERBOSE is True:
                        print('--------- prt ----------')
                        print('pendings: ' + str(pendings))
                        print('pending_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                # datives
                elif triple[0] == "dative":

                    lemma_pure = self.get_lemma(triple[2])[:-2]
                    if self.get_pos(triple[2]) == 'PRP' and lemma_pure.lower() not in self.BLACK_LIST_WORDS:

                        # treated as adverb
                        m = []
                        m.append(triple[1])
                        m.append(triple[2])
                        adv_adj.append(m)

                        # rectifing adv_adj vector
                        for adv in adv_adj:
                            if adv[0] == triple[2]:
                                adv[0] = triple[1]

                    elif lemma_pure.lower() not in self.BLACK_LIST_WORDS:

                        # treated as preposition
                        davidsonian_found = "UNASSIGNED"
                        found_var = "UNASSIGNED"
                        found_mod = "UNASSIGNED"
                        d_found = False

                        pending_prep.append(triple[2])

                        # searching triple[1] in mods --- case oprd
                        for m in mods:
                            if m[1] == triple[1]:
                                found_mod = m[0]

                        for v in var_list:
                            if v[1] == found_mod:
                                found_var = v[0]

                        for p in pendings:
                            # case var
                            if p[3] == found_var:
                                davidsonian_found = p[1]
                                d_found = True
                            # case verb
                            if p[0] == found_mod:
                                davidsonian_found = p[1]
                                d_found = True

                        # searching triple[1] in compounds
                        if d_found is False:
                            for m in mods:
                                if m[1] == triple[1]:
                                    found_mod = m[0]
                            for v in var_list:
                                if v[1] == found_mod:
                                    found_var = v[0]
                            for p in pendings:
                                if p[3] == found_var:
                                    davidsonian_found = p[1]
                                    d_found = True

                        # searching triple[1] in pendings
                        if d_found is False:
                            for p in pendings:
                                if self.get_first_token(p[0]) == triple[1] or self.get_first_token(p[0]) == found_mod:
                                    davidsonian_found = p[1]
                                    d_found = True

                        if d_found is False:
                            # retriving triple[1] from var_list
                            for v in var_list:
                                if v[1] == triple[1]:
                                    found_var = v[0]

                            # retriving related davidsonian from pendings and preps table
                            for prep in preps:
                                if prep[2] == found_var:
                                    davidsonian_found = prep[1]

                            for p in pendings:
                                if p[3] == found_var or p[2] == found_var:
                                    davidsonian_found = p[1]

                        pending_prep.append(davidsonian_found)

                        # updating var_list
                        index_args_counter = index_args_counter + 1
                        assignment = []
                        assignment.append(var + str(index_args_counter))
                        assignment.append('?')
                        var_list.append(assignment)
                        pending_prep.append(var + str(index_args_counter))

                    if self.VERBOSE is True:
                        print('--------- dative ----------')
                        print('pendings: ' + str(pendings))
                        print('pending_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                # adverbial modifiers or noun phrase as adverbial modifiers/markers/negations
                elif triple[0] in ["advmod", "mark", "neg", "npadvmod"]:

                    # firstly adverb assumed to be cond
                    m = []
                    m.append(triple[1])
                    m.append(triple[2])
                    adv_adj.append(m)

                    # rectifing adv_adj vector
                    for adv in adv_adj:
                        if adv[0] == triple[2]:
                            adv[0] = triple[1]

                    if self.VERBOSE is True:
                        print('--------- advmod ----------')
                        print('pendings: ' + str(pendings))
                        print('pending_prep: ' + str(pending_prep))
                        print('preps: ' + str(preps))
                        print('var_list: ' + str(var_list))
                        print('mods: ' + str(mods))
                        print('compounds: ' + str(compounds))
                        print('pending_agent: ' + str(pending_agent))
                        print('adv_adj: ' + str(adv_adj))

                else:
                    print('\nDEPENDENCY NOT HANDLED: '+triple[0])

                # correcting davidsonian prep preceding unvalued actions
                for pr in preps:
                    for p in pendings:
                        if pr[1] in p:
                            pr[1] = p[1]

        if len(adv_adj) > 0:

            ADVERB_PROCESSED = []

            #check for references in varlist
            for i in range(len(adv_adj)):
                for v in var_list:
                    if adv_adj[i][0] == v[1]:
                        mods.append(adv_adj[i])
                        ADVERB_PROCESSED.append(adv_adj[i])

            # check for references in mods
            for i in range(len(adv_adj)):
                if adv_adj[i] not in ADVERB_PROCESSED:
                    for m in mods:
                        if adv_adj[i][0] == m[1]:
                            new_mod = []
                            new_mod.append(m[0])
                            new_mod.append(adv_adj[i][1])
                            mods.append(new_mod)
                            ADVERB_PROCESSED.append(adv_adj[i])

            #check for references in preps
            for i in range(len(adv_adj)):
                if adv_adj[i] not in ADVERB_PROCESSED:
                    for prep in preps:
                        if adv_adj[i][0] in prep:
                            v = []
                            v.append(prep[1])
                            v.append(adv_adj[i][1])
                            var_list.append(v)
                            ADVERB_PROCESSED.append(adv_adj[i])

            # adding adverbials and/or conditionals
            for p in pendings:
                for i in range(len(adv_adj)):
                    if adv_adj[i] not in ADVERB_PROCESSED:
                        adv_pure = self.get_lemma(adv_adj[i][1])[:-2]
                        if adv_pure.lower() not in self.BLACK_LIST_WORDS:
                            if self.get_pos(adv_adj[i][1]) not in self.POS_FILTER:
                                if adv_adj[i][0] == self.get_first_token(p[0]) or adv_adj[i][0] == self.get_last_token(p[0]):
                                    if self.get_pos(adv_adj[i][1]) in self.adv_adj_POS:
                                        v = []
                                        v.append(p[1])
                                        v.append(adv_adj[i][1])
                                        var_list.append(v)

                                    else:

                                        #no deal with double conditionals (and aggregates) in the same utterance
                                        if p[1] not in cond:
                                            cond.append(p[1])
                                            for pend in pendings:
                                                if p[1] in pend or p[2] in pend or p[2] in pend:
                                                    if pend[1] not in cond:
                                                        cond.append(pend[1])

                                        #looking for binding verbs in mods

                                        for m in mods:
                                            if m[0] == p[0]:
                                                # getting mod's davidsonian
                                                for m_pend in pendings:
                                                    if m_pend[0] == m[1]:
                                                        # not deal with double conditionals in the same utterance
                                                        if m_pend[1] not in cond:
                                                            cond.append(m_pend[1])

            if self.VERBOSE is True:
                print('--------- var_list/adverb/conditionals ----------')
                print('var_list: ' + str(var_list))
                print('adv_adj: ' + str(adv_adj))
                print('COND: ' + str(cond))

        # post-processing steps ----------------------

        # adding reflective preposition without object
        if len(pending_prep) > 0:
            prep = []
            prep.append(pending_prep[0])
            prep.append(pending_prep[1])
            prep.append(pending_prep[2])
            preps.append(prep)

        # rectifing compound vector
        for c_est in compounds:
            for v in var_list:
                if v[1] == c_est[0]:
                    for c_int in compounds:
                        if c_int[0] == c_est[1]:
                            c_int[0] = v[1]

        # checking for interacting pending
        for c in cond:
            for p in pendings:
                if p[1] == c:
                    obj = p[3]
            for p in pendings:
                 if p[1] == obj:
                     cond.append(obj)

        TABLE = []
        TABLE.append(pendings)
        TABLE.append(var_list)
        TABLE.append(preps)
        TABLE.append(mods)
        TABLE.append(compounds)
        TABLE.append(cond)

        return TABLE


    def get_first_token(self, s):
        s_list = s.split("_")
        result = s_list[0]
        return result


    def get_last_token(self, s):
        s_list = s.split("_")
        if len(s_list) > 1:
            return s_list[len(s_list)-1]
        else:
            return s_list[0]


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

        counter = Counter(words_list)
        # print("\ncounter: ", counter)

        offset_dict = {}
        offset_dict_lemmatized = {}

        for token in reversed(doc):
            index = counter[token.text]
            offset_dict[token.idx] = token.text+"0"+str(index)+":"+token.tag_
            offset_dict_lemmatized[token.idx] = token.lemma_+"0"+str(index)+":"+token.tag_
            counter[token.text] = index - 1

        # print("\ncounter: ", counter)
        # print("\noffset_dict: ", offset_dict)

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


def main():
    VERBOSE = True
    LEMMMATIZED = True

    sentence = "The beast drunk his meal"

    parser = Parse(VERBOSE)
    deps = parser.get_deps(sentence, LEMMMATIZED)
    parser.set_last_deps(deps)
    ner = parser.get_last_ner()
    print("\nner: ", ner)

    for i in range(len(deps)):
        governor = parser.get_lemma(deps[i][1]).capitalize() + ":" + parser.get_pos(deps[i][1])
        dependent = parser.get_lemma(deps[i][2]).capitalize() + ":" + parser.get_pos(deps[i][2])
        deps[i] = [deps[i][0], governor, dependent]

    print("\n" + str(deps))

    MST = parser.create_MST(deps, 'e', 'x')
    print("\nMST: \n" + str(MST))



if __name__ == "__main__":
    main()








