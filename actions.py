from parse_en import *
from nl_to_fol import *
import sys
sys.path.insert(0, "../logic")
from logic.logic import *
from phidias.Types import *
import configparser
import math
import time
import datetime
from difflib import SequenceMatcher

config = configparser.ConfigParser()
config.read('config.ini')

VERBOSE = config.getboolean('NL_TO_FOL', 'VERBOSE')
LANGUAGE = config.get('NL_TO_FOL', 'LANGUAGE')
ASSIGN_RULES_ADMITTED = config.getboolean('NL_TO_FOL', 'ASSIGN_RULES_ADMITTED')
UNIQUE_NOUNS = config.getboolean('NL_TO_FOL', 'UNIQUE_NOUNS')
UNIQUE_ACT = config.getboolean('NL_TO_FOL', 'UNIQUE_ACT')
UNIQUE_ADJ = config.getboolean('NL_TO_FOL', 'UNIQUE_ADJ')
UNIQUE_PRP = config.getboolean('NL_TO_FOL', 'UNIQUE_PRP')
UNIQUE_ADV = config.getboolean('NL_TO_FOL', 'UNIQUE_ADV')
WAIT_TIME = config.getint('AGENT', 'WAIT_TIME')
INCLUDE_ACT_POS = config.getboolean('POS', 'INCLUDE_ACT_POS')
INCLUDE_NOUNS_POS = config.getboolean('POS', 'INCLUDE_NOUNS_POS')
INCLUDE_ADJ_POS = config.getboolean('POS', 'INCLUDE_ADJ_POS')
INCLUDE_PRP_POS = config.getboolean('POS', 'INCLUDE_PRP_POS')
INCLUDE_ADV_POS = config.getboolean('POS', 'INCLUDE_ADV_POS')
GEN_PREP = config.getboolean('GEN', 'GEN_PREP')
GEN_ADJ = config.getboolean('GEN', 'GEN_ADJ')
GEN_ADV = config.getboolean('GEN', 'GEN_ADV')
GEN_EXTRA = config.getboolean('GEN', 'GEN_EXTRA')
GEN_EXTRA_POS = config.get('GEN', 'EXTRA_GEN_POS').split(", ")

parser = Parse(VERBOSE)

# Clauses Knowledge Base instantion
kb_fol = FolKB([])

# FOl Reasoning procedures
class aggr_adj(Procedure): pass
class aggr_adv(Procedure): pass
class aggr_nouns(Procedure): pass
class mod_to_gnd(Procedure): pass
class gnd_prep_obj(Procedure): pass
class prep_to_gnd(Procedure): pass
class finalize_clause(Procedure): pass
class parse(Procedure): pass
class process_clause(Procedure): pass
class finalize_gnd(Procedure): pass
class apply_adv(Procedure): pass
class actions_to_clauses(Procedure): pass
class gnd_actions(Procedure): pass
class new_def_clause(Procedure): pass
class process_rule(Procedure): pass

# Reactive procedures - direct commands
class parse_command(Procedure): pass
class aggr_entities(Procedure): pass
class produce_intent(Procedure): pass
class produce_mod(Procedure): pass

# Reactive procedures - routines
class parse_routine(Procedure): pass

class produce_conds(Procedure): pass
class aggr_ent_conds(Procedure): pass
class produce_mod_conds(Procedure): pass

class produce_routine(Procedure): pass
class aggr_ent_rt(Procedure): pass
class produce_mod_rt(Procedure): pass

# check for routines execution
class check_conds(Procedure): pass

# start agent command
class go(Procedure): pass

# STT Front-End procedures
class w(Procedure): pass
class l(Procedure): pass
class r(Procedure): pass
class s(Procedure): pass

# initialize Clauses Kb
class c(Procedure): pass

# test assertions
class t(Procedure): pass

# mode reactors
class HOTWORD_DETECTED(Reactor): pass
class STT(Reactor): pass
class WAKE(Belief): pass
class LISTEN(Belief): pass
class REASON(Belief): pass
class RETRACT(Belief): pass
class IS_RULE(Belief): pass
class WAIT(Belief): pass

# domotic reactive routines
class r1(Procedure): pass
class r2(Procedure): pass

# domotic direct commands
class d1(Procedure): pass
class d2(Procedure): pass

# domotic sensor simulatons
class s1(Procedure): pass
class s2(Procedure): pass

# Fol reasoning utterances
class c1(Procedure): pass
class c2(Procedure): pass
class c3(Procedure): pass
class c4(Procedure): pass
class c5(Procedure): pass
class c6(Procedure): pass

# Fol query utterance
class q(Procedure): pass

# normal requests beliefs
class GROUND(Belief): pass
class PRE_MOD(Belief): pass
class MOD(Belief): pass
class PRE_INTENT(Belief): pass
class INTENT(Reactor): pass

# routines beliefs
class PRE_ROUTINE(Belief): pass
class ROUTINE(Belief): pass
class ROUTINE_PRE_MOD(Belief): pass
class ROUTINE_MOD(Belief): pass
class ROUTINE_GROUND(Belief): pass

# conditionals beliefs
class PRE_COND(Belief): pass
class COND(Belief): pass
class COND_GROUND(Belief): pass
class COND_PRE_MOD(Belief): pass

class SENSOR(Belief): pass
class START_ROUTINE(Reactor): pass

# clause
class CLAUSE(Belief): pass
# action
class ACTION(Belief): pass
# preposition
class PREP(Belief): pass
# ground
class GND(Belief): pass
# adverb
class ADV(Belief): pass
# adjective
class ADJ(Belief): pass
# left clause
class LEFT_CLAUSE(Belief): pass
# definite clause
class DEF_CLAUSE(Belief): pass
# remain
class REMAIN(Belief): pass
# preposition accumlator
class PRE_CROSS(Belief): pass
# Modificators number
class GEN_MASK(Belief): pass
# Actions crossing var
class ACT_CROSS_VAR(Belief): pass


class set_wait(Action):
    def execute(self):
        self.assert_belief(WAIT(WAIT_TIME))


class eval_cls(ActiveBelief):
    def evaluate(self, arg1):

        utterance = str(arg1).split("'")[1]

        bc_result = kb_fol.ask(expr(utterance))
        print("\n ---- NOMINAL REASONING ---\n")
        print("Result: " + str(bc_result))

        if bc_result is False:

            print("\n\n ---- NESTED REASONING ---")
            candidates = []

            nested_result = kb_fol.nested_ask(expr(utterance), candidates)
            if nested_result is None:
                return True
            elif nested_result is False:
                return False
            else:
                return True
        else:
            return True


class lemma_in_syn(ActiveBelief):
    def evaluate(self, arg1, arg2):

        verb = str(arg1).split("'")[3]
        synset = str(arg2).split("'")[1]

        pos = wordnet.VERB
        language = "eng"

        syns = wordnet.synsets(verb, pos=pos, lang=language)
        for syn in syns:
            if syn.name() == synset:
                return True
        return False


class join_clauses(Action):
    def execute(self, arg1, arg2, arg3):

        clause1 = str(arg1).split("'")[3]
        clause2 = str(arg2).split("'")[3]
        verb = str(arg3).split("'")[3]

        match = SequenceMatcher(None, clause1, clause2).find_longest_match(0, len(clause1), 0, len(clause2))
        common = clause1[match.a: match.a + match.size]

        while common[0] == "(":
            common = common[1:]
        while common[-1] != ")":
            common = common[:len(common) - 1]

        if str(clause1).find(verb) == -1:
            new_clause = clause1.replace(common, clause2)
        else:
            new_clause = clause2.replace(common, clause1)

        self.assert_belief(DEF_CLAUSE(new_clause))


class preprocess_clause(Action):

    def execute(self, *args):
        sentence = args[0]()
        gen_mask = str(args[1]())
        mode = str(args[2]())
        type = str(args[3]())

        print("\n--------- NEW GENERALIZATION ---------\n ")
        print("gen_mask: " + gen_mask)
        print("mode: " + mode)
        print("type: " + type + "\n")

        if mode == "ONE":
            Gen_mode = False
        else:
            Gen_mode = True

        self.MAIN_NEG_PRESENT = False

        print("\n" + sentence)
        deps = parser.get_deps(sentence)

        for i in range(len(deps)):
            governor = self.get_lemma(deps[i][1]).capitalize() + ":" + self.get_pos(deps[i][1])
            dependent = self.get_lemma(deps[i][2]).capitalize() + ":" + self.get_pos(deps[i][2])
            deps[i] = [deps[i][0], governor, dependent]

        # Dependencies Uniquezation
        Ren = Uniquelizer(VERBOSE, LANGUAGE)
        m_deps = Ren.morph_deps(deps)
        print("\n" + str(m_deps))

        MST = parser.create_MST(m_deps, 'e', 'x')
        print("\nMST: \n" + str(MST))

        # MST varlist correction on cases of adj-obj
        for v in MST[1]:
            if self.get_pos(v[1]) in ['JJ', 'JJR', 'JJS']:
                old_value = v[1]
                new_value = self.get_lemma(v[1]) + ":NNP"
                v[1] = new_value
                for b in MST[3]:
                    if b[0] == old_value:
                        b[0] = new_value

        m = ManageFols(VERBOSE, LANGUAGE)
        vect_LR_fol = m.build_LR_fol(MST, 'e')

        print("\nBefore dealing case:\n" + str(vect_LR_fol))

        if type == "NOMINAL":
            # NOMINAL CASE
            CHECK_IMPLICATION = m.check_implication(vect_LR_fol)
            if not CHECK_IMPLICATION:
                if ASSIGN_RULES_ADMITTED:
                    check_isa = m.check_for_rule(m_deps, vect_LR_fol)
                    if check_isa:
                        self.assert_belief(IS_RULE(sentence))
                dclause = vect_LR_fol[:]
            else:
                dclause = vect_LR_fol[:]
                dclause[1] = ["==>"]
        else:
            # RULE CASE
            ent_root = self.get_ent_ROOT(m_deps)
            dav_rule = self.get_dav_rule(vect_LR_fol, ent_root)
            positive_vect_LR_fol = []
            for v in vect_LR_fol:
                lemma = self.get_lemma(v[0])[:-2]
                if self.check_neg(lemma, LANGUAGE) and v[1] == dav_rule:
                    self.assert_belief(RETRACT("ON"))
                else:
                    positive_vect_LR_fol.append(v)

            vect_LR_fol_plus_isa = m.build_isa_fol(positive_vect_LR_fol, m_deps)
            dclause = m.isa_fol_to_clause(vect_LR_fol_plus_isa)

        print("\nAfter dealing case:\n" + str(dclause))

        # IMPLICATION CASES
        if dclause[1][0] == "==>":

            mods = []

            for v in dclause[2]:
                if self.get_pos(v[0]) in GEN_EXTRA_POS and GEN_EXTRA is True:
                    mods.append(v[0])
                if self.get_pos(v[0]) == "IN" and GEN_PREP is True:
                    mods.append(v[0])
                elif self.get_pos(v[0]) == "JJ" and GEN_ADJ is True:
                    mods.append(v[0])

                elif self.get_pos(v[0]) in ['RB', 'RBR', 'RBS']:
                    if GEN_ADV is True:
                        mods.append(v[0])
                    lemma = self.get_lemma(v[0])[:-2]
                    if self.check_neg(lemma, LANGUAGE):
                        print("\nNot a definite clause!")
                        return

            if gen_mask == "BASE":

                print("\nmods: " + str(mods))
                nmods = int(math.pow(2, len(mods))) - 1
                print("\ngereralizations number: " + str(nmods) + "\n")

                actual_mask = ""
                for i in range(len(mods)):
                    actual_mask = actual_mask + "0"
                gen_mask = actual_mask

                # creating dictionary
                voc = {}
                for i in range(len(mods)):
                    if gen_mask[i] == '1':
                        val = True
                    else:
                        val = False
                    voc.update({mods[i]: val})

                # triggering generalizations production
                if len(mods) > 0 and Gen_mode is True:
                    inc_mask = self.get_inc_mask(actual_mask)
                    self.assert_belief(GEN_MASK(inc_mask))

            elif gen_mask == "FULL":
                # creating dictionary
                voc = {}
                for i in range(len(mods)):
                    voc.update({mods[i]: True})

            else:

                # creating dictionary
                voc = {}
                full_true_voc = {}
                for i in range(len(mods)):
                    if gen_mask[i] == '1':
                        val = True
                    else:
                        val = False
                    voc.update({mods[i]: val})
                    full_true_voc.update({mods[i]: True})

                inc_mask = self.get_inc_mask(gen_mask)
                if len(inc_mask) == len(gen_mask):
                    self.assert_belief(GEN_MASK(inc_mask))

            print("\nPROCESSING LEFT HAND-SIDE...")
            self.process_fol(dclause[0], "LEFT", voc)

            print("\nPROCESSING RIGHT HAND-SIDE...")
            self.process_fol(dclause[2], "RIGHT", voc)

        # FLAT CASES
        else:
            mods = []
            nomain_negs = []
            ent_root = self.get_ent_ROOT(m_deps)
            dav_act = self.get_dav_rule(dclause, ent_root)
            for v in dclause:
                if self.get_pos(v[0]) in GEN_EXTRA_POS and GEN_EXTRA is True:
                    mods.append(v[0])
                elif self.get_pos(v[0]) == "IN" and GEN_PREP is True:
                    mods.append(v[0])
                elif self.get_pos(v[0]) == "JJ" and GEN_ADJ is True:
                    mods.append(v[0])

                if self.get_pos(v[0]) in ['RB', 'RBR', 'RBS']:
                    lemma = self.get_lemma(v[0])[:-2]
                    if self.check_neg(lemma, LANGUAGE):
                        if v[1] == dav_act:
                            self.MAIN_NEG_PRESENT = True
                            self.assert_belief(RETRACT("ON"))
                            main_neg_index = len(mods) - 1
                            dclause.remove(v)
                        else:
                            if GEN_ADV is True:
                                mods.append(v[0])
                                nomain_negs.append(v)
                    else:
                        if GEN_ADV is True:
                            mods.append(v[0])

            # every verb/adj will carry its non-main negative
            negs = {}
            for n in nomain_negs:
                for v in dclause:
                    if v[1] == n[1]:
                        if v not in nomain_negs:
                            negs.update({v[0]: n[0]})

            # only reason
            if gen_mask == "FULL":
                # creating dictionary
                voc = {}
                for i in range(len(mods)):
                    voc.update({mods[i]: True})

            elif gen_mask == "BASE":

                actual_mask = ""

                if self.MAIN_NEG_PRESENT:
                    for i in range(len(mods)):
                        if i == main_neg_index:
                            actual_mask = actual_mask + "0"
                        else:
                            actual_mask = actual_mask + "1"
                else:
                    for i in range(len(mods)):
                        actual_mask = actual_mask + "0"

                gen_mask = actual_mask

                # creating vocabolary
                voc = {}
                for i in range(len(mods)):
                    if gen_mask[i] == '1':
                        val = True
                    else:
                        val = False
                    voc.update({mods[i]: val})

                # voc rectification for carrying negations, other negations = True
                for nm in nomain_negs:
                    voc[nm[0]] = True
                for ng in negs:
                    if ng in voc:
                        voc[negs[ng]] = voc[ng]

                nmods = int(math.pow(2, len(mods))) - 1
                print("\ngereralizations number: " + str(nmods))

                # triggering generalizations production
                if len(mods) > 0 and Gen_mode and not self.MAIN_NEG_PRESENT:
                    inc_mask = self.get_inc_mask(actual_mask)
                    self.assert_belief(GEN_MASK(inc_mask))
            else:

                # creating vocabolary
                voc = {}
                for i in range(len(mods)):
                    if gen_mask[i] == '1':
                        val = True
                    else:
                        val = False
                    voc.update({mods[i]: val})

                # voc rectification for carrying negations, other negations = True
                for nm in nomain_negs:
                    voc[nm[0]] = True
                for ng in negs:
                    if ng in voc:
                        voc[negs[ng]] = voc[ng]

                inc_mask = self.get_inc_mask(gen_mask)
                if len(inc_mask) == len(gen_mask):
                    self.assert_belief(GEN_MASK(inc_mask))

            self.process_fol(dclause, "FLAT", voc)

    def get_ent_ROOT(self, deps):
        for d in deps:
            if d[0] == "ROOT":
                return d[1]

    def get_dav_rule(self, fol, ent_root):
        for f in fol:
            if f[0] == ent_root:
                return f[1]
        return False

    def check_neg(self, word, language):
        pos = wordnet.ADV
        syns = wordnet.synsets(word, pos=pos, lang=language)
        for synset in syns:
            if str(synset.name()) in ['no.r.01', 'no.r.02', 'no.r.03', 'not.r.01']:
                return True
        return False

    def get_inc_mask(self, n):
        diff = str(bin(int(n, 2) + int("1", 2)))[2:]
        delta = len(n) - len(diff)
        for i in range(delta):
            diff = "0" + diff
        return diff

    def get_dec_mask(self, n):
        diff = str(bin(int(n, 2) - int("00001", 2)))[2:]
        delta = len(n) - len(diff)
        for i in range(delta):
            diff = "0" + diff
        return diff

    def get_nocount_lemma(self, lemma):
        lemma_nocount = ""
        total_lemma = lemma.split("_")

        for i in range(len(total_lemma)):
            if i == 0:
                lemma_nocount = total_lemma[i].split(':')[0][:-2] + ":" + total_lemma[i].split(':')[1]
            else:
                lemma_nocount = total_lemma[i].split(':')[0][:-2] + ":" + total_lemma[i].split(':')[
                    1] + "_" + lemma_nocount
        return lemma_nocount

    def process_fol(self, vect_fol, id, voc):

        print("\n------DICTIONARY------")
        print(voc)
        print("----------------------\n")

        # actions-crossing var list
        var_crossing = []
        admissible_vars = ['x']

        # prepositions
        for v in vect_fol:
            if len(v) == 3:

                if UNIQUE_PRP:
                    label = v[0]
                else:
                    label = self.get_nocount_lemma(v[0])

                if GEN_PREP is False or id == "LEFT":
                    if INCLUDE_PRP_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    self.assert_belief(PREP(str(id), v[1], lemma, v[2]))
                    print("PREP(" + str(id) + ", " + v[1] + ", " + lemma + ", " + v[2] + ")")
                    if v[1] not in admissible_vars:
                        admissible_vars.append(v[1])
                    if v[2] not in admissible_vars:
                        admissible_vars.append(v[2])

                elif v[0] in voc and voc[v[0]] is True:
                    if INCLUDE_PRP_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    self.assert_belief(PREP(str(id), v[1], lemma, v[2]))
                    print("PREP(" + str(id) + ", " + v[1] + ", " + lemma + ", " + v[2] + ")")
                    if v[1] not in admissible_vars:
                        admissible_vars.append(v[1])
                    if v[2] not in admissible_vars:
                        admissible_vars.append(v[2])

        # actions
        for v in vect_fol:
            ACTION_ASSERTED = False
            if len(v) == 4:

                if UNIQUE_ACT:
                    label = v[0]
                else:
                    label = self.get_nocount_lemma(v[0])
                    pos = self.get_pos(v[0])

                if INCLUDE_ACT_POS:
                    lemma = label
                else:
                    lemma = parser.get_lemma(label)

                if GEN_EXTRA is True and pos in GEN_EXTRA_POS:
                    if (v[0] in voc and voc[v[0]] is True):
                        self.assert_belief(ACTION(str(id), lemma, v[1], v[2], v[3]))
                        print("ACTION(" + str(id) + ", " + lemma + ", " + v[1] + ", " + v[2] + ", " + v[3] + ")")
                        ACTION_ASSERTED = True
                else:
                    self.assert_belief(ACTION(str(id), lemma, v[1], v[2], v[3]))
                    print("ACTION(" + str(id) + ", " + lemma + ", " + v[1] + ", " + v[2] + ", " + v[3] + ")")
                    ACTION_ASSERTED = True

                if ACTION_ASSERTED:
                    # check for var action crossing
                    if v[2] in var_crossing:
                        self.assert_belief(ACT_CROSS_VAR(str(id), v[2], lemma))
                        print("ACT_CROSS_VAR(" + str(id) + ")")
                    else:
                        var_crossing.append(v[2])

                    if v[3] in var_crossing:
                        self.assert_belief(ACT_CROSS_VAR(str(id), v[3], lemma))
                        print("ACT_CROSS_VAR(" + str(id) + ")")
                    else:
                        var_crossing.append(v[3])

                    if v[1] not in admissible_vars:
                        admissible_vars.append(v[1])
                    if v[2] not in admissible_vars:
                        admissible_vars.append(v[2])
                    if v[3] not in admissible_vars:
                        admissible_vars.append(v[3])

        # nouns
        for v in vect_fol:
            if len(v) == 2:
                if self.get_pos(v[0]) in ['NNP', 'NNPS', 'PRP', 'CD', 'NN', 'NNS', 'PRP', 'PRP$']:
                    if UNIQUE_NOUNS:
                        label = v[0]
                    else:
                        label = self.get_nocount_lemma(v[0])

                    if INCLUDE_NOUNS_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    if v[1] in admissible_vars:
                        self.assert_belief(GND(str(id), v[1], lemma))
                        print("GND(" + str(id) + ", " + v[1] + ", " + lemma + ")")

        # adjectives, adverbs
        for v in vect_fol:
            if self.get_pos(v[0]) in ['JJ', 'JJR', 'JJS']:

                if UNIQUE_ADJ:
                    label = v[0]
                else:
                    label = self.get_nocount_lemma(v[0])

                if GEN_ADJ is False or id == "LEFT":

                    if INCLUDE_ADJ_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    if v[1] in admissible_vars:
                        self.assert_belief(ADJ(str(id), v[1], lemma))
                        print("ADJ(" + str(id) + ", " + v[1] + ", " + lemma + ")")

                elif v[0] in voc and voc[v[0]] is True:
                    if INCLUDE_ADJ_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    if v[1] in admissible_vars:
                        self.assert_belief(ADJ(str(id), v[1], lemma))
                        print("ADJ(" + str(id) + ", " + v[1] + ", " + lemma + ")")

            elif self.get_pos(v[0]) in ['RB', 'RBR', 'RBS']:

                if UNIQUE_ADV:
                    label = v[0]
                else:
                    label = self.get_nocount_lemma(v[0])

                if GEN_ADV is False or id == "LEFT":
                    if INCLUDE_ADV_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    if v[1] in admissible_vars:
                        self.assert_belief(ADV(str(id), v[1], lemma))
                        print("ADV(" + str(id) + ", " + v[1] + ", " + lemma + ")")

                elif v[0] in voc and voc[v[0]] is True:
                    if INCLUDE_ADV_POS:
                        lemma = label
                    else:
                        lemma = parser.get_lemma(label)

                    if v[1] in admissible_vars:
                        self.assert_belief(ADV(str(id), v[1], lemma))
                        print("ADV(" + str(id) + ", " + v[1] + ", " + lemma + ")")

    def get_pos(self, s):
        first = s.split('_')[0]
        s_list = first.split(':')
        if len(s_list) > 1:
            return s_list[1]
        else:
            return s_list[0]

    def get_lemma(self, s):
        s_list = s.split(':')
        return s_list[0]


class retract_clause(Action):

    def execute(self, *args):
        sentence = args[0]()
        mf = parser.morph(sentence)
        print("\n" + mf)

        def_clause = expr(mf)

        if def_clause in kb_fol.clauses:
            kb_fol.retract(def_clause)


class new_clause(Action):

    def execute(self, *args):
        sentence = args[0]()

        start_time = time.time()

        print("\n" + sentence)
        mf = parser.morph(sentence)
        def_clause = expr(mf)

        kb_fol.nested_tell(def_clause)

        end_time = time.time()
        assert_time = end_time - start_time
        print("\nAssert time: ", assert_time)


class reason(Action):

    def execute(self, *args):
        definite_clause = args[0]()

        start_time = time.time()

        q = parser.morph(definite_clause)
        print("Query: " + q)
        print("OCCUR_CHECK: ", exec_occur_check)

        bc_result = kb_fol.ask(expr(q))
        print("\n ---- NOMINAL REASONING ---\n")
        print("Result: " + str(bc_result))

        end_time1 = time.time()
        query_time1 = end_time1 - start_time
        print("Backward-Chaining Query time: ", query_time1)

        if bc_result is False:

            print("\n\n ---- NESTED REASONING ---")
            candidates = []

            nested_result = kb_fol.nested_ask(expr(q), candidates)
            if nested_result is None:
                print("\nClause present in kb. No substitutions needed.")
            else:
                print("\nResult: ", nested_result)

            end_time2 = time.time()
            query_time2 = end_time2 - start_time
            print("\nQuery time: ", query_time2)


class assert_command(Action):

    def execute(self, *args):

        sentence = args[0]()

        # ----> words or chars not dealing well with fol conversion
        # verb_i2 must not be part of some verb_j1, with i!=j
        # [verb_i1, verb_i2]

        SWAP_STR = [["turn on", "change"], [":", "."], ["_", "-"]]

        for s in SWAP_STR:
            sentence = sentence.lower().replace(s[0], s[1])

        print(sentence)

        deps = parser.get_deps(sentence)

        # Dependencies Uniquezation
        Ren = Uniquelizer(VERBOSE, LANGUAGE)
        m_deps = Ren.morph_deps(deps)

        TABLE = parser.create_MST(m_deps, 'd', 'x')

        m = ManageFols(VERBOSE, LANGUAGE)
        vect_LR_fol = m.build_LR_fol(TABLE, 'd')

        # getting fol's type
        check_isa = False
        check_implication = m.check_implication(vect_LR_fol)
        if check_implication is False:
            check_isa = m.check_isa(vect_LR_fol, m_deps)

        gentle_LR_fol = m.vect_LR_to_gentle_LR(vect_LR_fol, m_deps, check_implication, check_isa)
        print(str(gentle_LR_fol))

        if vect_LR_fol[1][0] == "==>":

            dateTimeObj = datetime.datetime.now()
            id_routine = dateTimeObj.microsecond

            self.process_conditions(vect_LR_fol[0], id_routine)
            self.process_routine(vect_LR_fol[2], id_routine)
        else:
            self.process(vect_LR_fol)

    def process_conditions(self, vect_fol, id_routine):
        dateTimeObj = datetime.datetime.now()
        id_ground = dateTimeObj.microsecond
        for g in vect_fol:
            if len(g) == 3:
                lemma = self.get_lemma(g[0])[:-2]
                self.assert_belief(COND_PRE_MOD(g[1], lemma, g[2]))
        for g in vect_fol:
            if len(g) == 2:
                lemma = self.get_lemma(g[0])[:-2]
                self.assert_belief(COND_GROUND(str(id_ground), g[1], lemma))
                id_ground = id_ground + 1
        for g in vect_fol:
            if len(g) == 4:
                verb = self.get_verbs_nopos(g[0])
                self.assert_belief(PRE_COND(str(id_routine), verb, g[1], g[2], g[3]))

    def process_routine(self, vect_fol, id_routine):
        dateTimeObj = datetime.datetime.now()
        id_ground = dateTimeObj.microsecond
        for g in vect_fol:
            if len(g) == 3:
                lemma = self.get_lemma(g[0])[:-2]
                self.assert_belief(ROUTINE_PRE_MOD(g[1], lemma, g[2]))
        for g in vect_fol:
            if len(g) == 2:
                lemma = self.get_lemma(g[0])[:-2]
                self.assert_belief(ROUTINE_GROUND(str(id_ground), g[1], lemma))
                id_ground = id_ground + 1
        for g in vect_fol:
            if len(g) == 4:
                verb = self.get_verbs_nopos(g[0])
                self.assert_belief(PRE_ROUTINE(str(id_routine), verb, g[1], g[3], "", ""))

    def process(self, vect_fol):

        dateTimeObj = datetime.datetime.now()
        id_ground = dateTimeObj.microsecond

        for g in vect_fol:
            if len(g) == 3:
                lemma = self.get_lemma(g[0])[:-2]
                self.assert_belief(PRE_MOD(g[1], lemma, g[2]))
            if len(g) == 2:
                lemma = self.get_lemma(g[0])[:-2]
                self.assert_belief(GROUND(str(id_ground), g[1], lemma))
                id_ground = id_ground + 1
            if len(g) == 4:
                verb = self.get_verbs_nopos(g[0])
                self.assert_belief(PRE_INTENT(verb, g[1], g[3], "", ""))

    def get_verbs_nopos(self, lemma):
        lemma_nopos = ""
        total_lemma = lemma.split("_")

        for i in range(len(total_lemma)):
            if i == 0:
                lemma_nopos = total_lemma[i].split(':')[0][:-2]
            else:
                lemma_nopos = total_lemma[i].split(':')[0][:-2] + " " + lemma_nopos
        return lemma_nopos

    def get_lemma(self, s):
        s_list = s.split(':')
        return s_list[0]


class join_grounds(Action):
    def execute(self, *args):
        dateTimeObj = datetime.datetime.now()
        id_ground = dateTimeObj.microsecond

        union = self.get_arg(str(args[1])) + " " + self.get_arg(str(args[2]))
        self.assert_belief(GROUND(str(id_ground), self.get_arg(str(args[0])), union))

    def get_arg(self, arg):
        s = arg.split("'")
        return s[3]


class join_cond_grounds(Action):
    def execute(self, *args):
        dateTimeObj = datetime.datetime.now()
        id_ground = dateTimeObj.microsecond

        union = self.get_arg(str(args[1])) + " " + self.get_arg(str(args[2]))
        self.assert_belief(COND_GROUND(str(id_ground), self.get_arg(str(args[0])), union))

    def get_arg(self, arg):
        s = arg.split("'")
        return s[3]


class join_routine_grounds(Action):
    def execute(self, *args):
        dateTimeObj = datetime.datetime.now()
        id_ground = dateTimeObj.microsecond

        union = self.get_arg(str(args[1])) + " " + self.get_arg(str(args[2]))
        self.assert_belief(ROUTINE_GROUND(str(id_ground), self.get_arg(str(args[0])), union))

    def get_arg(self, arg):
        s = arg.split("'")
        return s[3]


class mods_grounds(Action):
    def execute(self, *args):
        union = self.get_arg(str(args[1])) + ", " + self.get_arg(str(args[2]) + " " + self.get_arg(str(args[3])))
        self.assert_belief(GROUND(self.get_arg(str(args[0])), union))

    def get_arg(self, arg):
        s = arg.split("'")
        return s[3]


class append_intent_params(Action):
    def execute(self, *args):
        parameters_list = self.get_arg(str(args[6]))
        location = self.get_arg(str(args[5]))

        verb = self.get_arg(str(args[0]))
        dav = self.get_arg(str(args[1]))
        obj = self.get_arg(str(args[2]))

        prep = self.get_arg(str(args[3]))
        prep_obj = self.get_arg(str(args[4]))

        if prep == "in":
            location = prep_obj
        else:

            if len(parameters_list) == 0:
                parameters_list = prep + " " + prep_obj
            else:
                parameters_list = parameters_list + ", " + prep + " " + prep_obj

        self.assert_belief(PRE_INTENT(verb, dav, obj, location, parameters_list))

    def get_arg(self, arg):
        s = arg.split("'")
        return s[3]


class append_routine_params(Action):
    def execute(self, *args):

        id_routine = self.get_arg(str(args[0]))
        verb = self.get_arg(str(args[1]))
        dav = self.get_arg(str(args[2]))
        object_routine = self.get_arg(str(args[3]))

        prep = self.get_arg(str(args[4]))
        prep_obj = self.get_arg(str(args[5]))

        location = self.get_arg(str(args[6]))
        parameters_list = self.get_arg(str(args[7]))

        if prep == "in":
            location = prep_obj
        else:
            if len(parameters_list) == 0:
                parameters_list = prep + " " + prep_obj
            else:
                parameters_list = parameters_list + ", " + prep + " " + prep_obj

        self.assert_belief(PRE_ROUTINE(id_routine, verb, dav, object_routine, location, parameters_list))

    def get_arg(self, arg):
        s = arg.split("'")
        return s[3]


class append_intent_mods(Action):
    def execute(self, *args):

        verb = self.get_arg(str(args[0]))
        dav = self.get_arg(str(args[1]))
        object = self.get_arg(str(args[2]))

        mod = self.get_arg(str(args[3]))

        location = self.get_arg(str(args[4]))
        parameters_list = self.get_arg(str(args[5]))

        if len(parameters_list) == 0:
            parameters_list = mod
        else:
            parameters_list = parameters_list + ", " + mod

        self.assert_belief(PRE_INTENT(verb, dav, object, location, parameters_list))

    def get_arg(self, arg):
        s = arg.split("'")
        return s[3]


class append_routine_mods(Action):
    def execute(self, *args):

        id_routine = self.get_arg(str(args[0]))
        verb = self.get_arg(str(args[1]))
        dav = self.get_arg(str(args[2]))
        object_routine = self.get_arg(str(args[3]))

        location = self.get_arg(str(args[5]))
        parameters_list = self.get_arg(str(args[6]))
        mod = self.get_arg(str(args[4]))

        if len(parameters_list) == 0:
            parameters_list = mod
        else:
            parameters_list = parameters_list + ", " + mod

        self.assert_belief(PRE_ROUTINE(id_routine, verb, dav, object_routine, location, parameters_list))

    def get_arg(self, arg):
        s = arg.split("'")
        return s[3]


class exec_cmd(Action):
    def execute(self, *args):

        command = self.get_arg(str(args[0]))
        object = self.get_arg(str(args[1]))
        location = self.get_arg(str(args[2]))
        parameters = self.get_arg(str(args[3]))

        SWAP_STR = [[":", "."], ["_", "-"]]

        for s in SWAP_STR:
            object = object.replace(s[1], s[0])
            parameters = parameters.replace(s[1], s[0])

        print("\n---- Result: execution successful")
        print("\nAction: " + command)
        print("Object: " + object)

        if len(location) > 0:
            print("Location: " + location)

        if len(parameters) > 0:
            print("Parameters: " + parameters)
        print("\n")

    def get_arg(self, arg):
        s = arg.split("'")
        if len(s) == 3:
            return s[1]
        else:
            return s[3]


class simulate_sensor(Action):
    def execute(self, *args):
        verb = args[0]
        subject = args[1]
        object = args[2]
        print("\n\nasserting SENSOR(" + str(verb) + "," + str(subject) + "," + str(object) + ")...")
        self.assert_belief(SENSOR(verb, subject, object))


class NLP_Parser(object):
    def __init__(self):
        self.VERBOSE = False
        self.parser = Parse(self.VERBOSE)

    def get_parser(self):
        return self.parser


class aggregate(Action):
    def execute(self, arg0, arg1, arg2, arg3, arg4):

        type = str(arg0).split("'")[1]
        id = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        label1 = str(arg3).split("'")[3]
        label2 = str(arg4).split("'")[3]

        if len(label1.split('_')) > 1:
            conc_label = label1 + "_" + label2
        else:
            conc_label = label2 + "_" + label1

        if type == "ADJ":
            self.assert_belief(ADJ(id, var, conc_label))

        elif type == "ADV":
            self.assert_belief(ADV(id, var, conc_label))
        else:
            self.assert_belief(GND(id, var, conc_label))

    def get_arg(self, arg):
        s = arg.split("'")
        return s[3]

    def get_pos(self, s):
        first = s.split('_')[0]
        s_list = first.split(':')
        if len(s_list) > 1:
            return s_list[1]
        else:
            return s_list[0]


class merge(Action):
    def execute(self, arg1, arg2, arg3, arg4):
        id = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        adj = str(arg3).split("'")[3]
        noun = str(arg4).split("'")[3]

        new_label = adj + "(" + noun + ")"
        self.assert_belief(GND(id, var, new_label))


class ground_prep(Action):
    def execute(self, arg1, arg2, arg3, arg4, arg5):

        id = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        prep_label = str(arg3).split("'")[3]
        var_ground = str(arg4).split("'")[3]
        label_ground = str(arg5).split("'")[3]

        pn = self.get_par_number(label_ground)
        if pn == 0:
            new_object = label_ground + "(" + var_ground + ")"
        else:
            ls = label_ground.split(' ')
            if len(ls) > 1:
                new_object = label_ground
            else:
                new_object = label_ground[:-pn] + "(" + var_ground + ")"
                for i in range(pn):
                    new_object = new_object + ")"

        self.assert_belief(PREP(id, var, prep_label, new_object))

    def get_par_number(self, s):
        count = 0
        while (s[len(s) - (count + 1)] == ")"):
            count = count + 1
        return count


class int_preps_tognd(Action):
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6):
        id = str(arg1).split("'")[3]
        var_ground_est = str(arg2).split("'")[3]
        var_ground_int = str(arg3).split("'")[3]
        prep_est_label = str(arg4).split("'")[3]
        prep_int_object = str(arg5).split("'")[3]
        ground_label = str(arg6).split("'")[3]

        new_label = prep_est_label + "(" + ground_label + "(" + var_ground_est + "), " + prep_int_object + "(" + var_ground_int + "))"
        self.assert_belief(GND(id, var_ground_est, new_label))


class gprep_to_ground(Action):
    def execute(self, arg1, arg2, arg3, arg4, arg5):
        id = str(arg1).split("'")[3]
        var_prep_ground = str(arg2).split("'")[3]
        prep_label = str(arg3).split("'")[3]
        prep_object = str(arg4).split("'")[3]
        ground_label = str(arg5).split("'")[3]

        new_label = prep_label + "(" + ground_label + ", " + prep_object + ")"
        self.assert_belief(GND(id, var_prep_ground, new_label))


class adv_to_action(Action):
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6):
        id = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3]
        dav = str(arg3).split("'")[3]
        subj = str(arg4).split("'")[3]
        obj = str(arg5).split("'")[3]
        adv_label = str(arg6).split("'")[3]

        new_verb = adv_label + "(" + verb + ")"

        self.assert_belief(ACTION(id, new_verb, dav, subj, obj))


class act_to_clause(Action):
    def execute(self, arg1, arg2, arg3, arg4, arg5):

        id = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3]
        dav = str(arg3).split("'")[3]
        subj = str(arg4).split("'")[3]
        obj = str(arg5).split("'")[3]

        pn = self.get_par_number(verb)
        if pn == 0:
            action = verb + "(" + subj + ", " + obj + ")"
        else:
            action = verb[:-pn] + "(" + subj + ", " + obj + ")"
            for i in range(pn):
                action = action + ")"

        self.assert_belief(CLAUSE(id, dav, action))

    def get_par_number(self, s):
        count = 0
        while (s[len(s) - (count + 1)] == ")"):
            count = count + 1
        return count


class ground_subj_act(Action):
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6):

        id = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3]

        dav = str(arg3).split("'")[3]
        subj = str(arg4).split("'")[3]
        obj = str(arg5).split("'")[3]
        ground_label = str(arg6).split("'")[3]

        pn_label = self.get_par_number(ground_label)
        t = ground_label.split(" ")

        if len(t) > 1:  # prep applied to ground case

            token1 = t[0][:-1]  # first token, without comma
            pn_token1 = self.get_par_number(token1)  # first token right-parentesys number

            if pn_token1 == 0:
                token1 = token1 + "(" + subj + ")"
            else:
                token1 = token1[:-pn_token1] + "(" + subj + ")"

            for i in range(pn_token1):
                token1 = token1 + ")"

            rem = ' '.join(t[1:])

            new_subj = token1 + ", " + rem[:-pn_label]

        else:
            if pn_label == 0:
                new_subj = ground_label + "(" + subj + ")"
            else:
                new_subj = ground_label[:-pn_label] + "(" + subj + ")"

        for i in range(pn_label):
            new_subj = new_subj + ")"

        self.assert_belief(ACTION(id, verb, dav, new_subj, obj))

    def get_par_number(self, s):
        count = 0
        while (s[len(s) - (count + 1)] == ")"):
            count = count + 1
        return count


class ground_obj_act(Action):
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6):

        id = str(arg1).split("'")[3]
        verb = str(arg2).split("'")[3]

        dav = str(arg3).split("'")[3]
        subj = str(arg4).split("'")[3]
        obj = str(arg5).split("'")[3]
        ground_label = str(arg6).split("'")[3]

        pn_label = self.get_par_number(ground_label)

        t = ground_label.split(" ")
        if len(t) > 1:
            token1 = t[0][:-1]  # first token, without comma

            pn_token1 = self.get_par_number(token1)  # first token right-parentesys number

            if pn_token1 == 0:
                token1 = token1 + "(" + obj + ")"
            else:
                token1 = token1[:-pn_token1] + "(" + obj + ")"

            for i in range(pn_token1):
                token1 = token1 + ")"

            rem = ' '.join(t[1:])
            new_obj = token1 + ", " + rem[:-pn_label]

        else:
            if pn_label == 0:
                new_obj = ground_label + "(" + obj + ")"
            else:
                new_obj = ground_label[:-pn_label] + "(" + obj + ")"

        for i in range(pn_label):
            new_obj = new_obj + ")"

        self.assert_belief(ACTION(id, verb, dav, subj, new_obj))

    def get_par_number(self, s):
        count = 0
        while (s[len(s) - (count + 1)] == ")"):
            count = count + 1
        return count


class prep_to_clause(Action):
    def execute(self, arg1, arg2, arg3, arg4, arg5):
        id = str(arg1).split("'")[3]
        dav = str(arg2).split("'")[3]
        clause = str(arg3).split("'")[3]
        prep_label = str(arg4).split("'")[3]
        prep_obj = str(arg5).split("'")[3]

        new_clause = prep_label + "(" + clause + ", " + prep_obj + ")"

        self.assert_belief(CLAUSE(id, dav, new_clause))


class join_hand_sides(Action):
    def execute(self, arg1, arg2):
        lhs = str(arg1).split("'")[3]
        rhs = str(arg2).split("'")[3]

        new_clause = lhs + " ==> " + rhs
        self.assert_belief(DEF_CLAUSE(new_clause))


class conjunct_left_clauses(Action):
    def execute(self, arg1, arg2):
        left_clause1 = str(arg1).split("'")[3]
        left_clause2 = str(arg2).split("'")[3]

        clauses_conjunction = left_clause1 + " & " + left_clause2
        self.assert_belief(LEFT_CLAUSE(clauses_conjunction))


class create_remain(Action):
    def execute(self, arg1, arg2, arg3):

        id = str(arg1).split("'")[3]
        var = str(arg2).split("'")[3]
        label = str(arg3).split("'")[3]

        pn_label = self.get_par_number(label)

        t = label.split(" ")
        if len(t) > 1:
            token1 = t[0][:-1]  # first token, without comma

            pn_token1 = self.get_par_number(token1)  # first token right-parentesys number

            if pn_token1 == 0:
                token1 = token1 + "(" + var + ")"
            else:
                token1 = token1[:-pn_token1] + "(" + var + ")"

            for i in range(pn_token1):
                token1 = token1 + ")"

            new_label = token1 + ", " + t[1][:-pn_label]

        else:
            if pn_label == 0:
                new_label = label + "(" + var + ")"
            else:
                new_label = label[:-pn_label] + "(" + var + ")"

        for i in range(pn_label):
            new_label = new_label + ")"

        self.assert_belief(REMAIN(id, new_label))

    def get_par_number(self, s):
        count = 0
        while (s[len(s) - (count + 1)] == ")"):
            count = count + 1
        return count


class no_dav(ActiveBelief):
    def evaluate(self, x):

        var = str(x).split("'")[3]
        # Check for davidsonian
        if var[0] == 'e':
            return False
        else:
            return True


class merge_act(Action):
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6, arg7):

        id = str(arg1).split("'")[3]

        verb_act_merged = str(arg2).split("'")[3]
        subj_act_merged = str(arg3).split("'")[3]
        obj_act_merged = str(arg4).split("'")[3]

        verb_act_merging = str(arg5).split("'")[3]
        dav_act_merging = str(arg6).split("'")[3]
        subj_act_merging = str(arg7).split("'")[3]

        pn_label = self.get_par_number(verb_act_merged)

        if pn_label > 0:
            new_obj = verb_act_merged[:-pn_label] + "(" + subj_act_merged + ", " + obj_act_merged + ")"
        else:
            new_obj = verb_act_merged + "(" + subj_act_merged + ", " + obj_act_merged + ")"

        for i in range(pn_label):
            new_obj = new_obj + ")"

        self.assert_belief(ACTION(id, verb_act_merging, dav_act_merging, subj_act_merging, new_obj))

    def get_par_number(self, s):
        count = 0
        while (s[len(s) - (count + 1)] == ")"):
            count = count + 1
        return count


class create_precross(Action):
    def execute(self, arg1, arg2, arg3, arg4, arg5, arg6, arg7):

        id = str(arg1).split("'")[3]
        verb_act_merged = str(arg2).split("'")[3]
        dav_act_merged = str(arg3).split("'")[3]
        subj_act_merged = str(arg4).split("'")[3]
        obj_act_merged = str(arg5).split("'")[3]

        prep_label = str(arg6).split("'")[3]
        prep_obj = str(arg7).split("'")[3]

        pn_label = self.get_par_number(verb_act_merged)

        act_merged = prep_label + "(" + verb_act_merged[
                                        :-pn_label] + "(" + subj_act_merged + ", " + obj_act_merged + ")"
        for i in range(pn_label):
            act_merged = act_merged + ")"
        act_merged = act_merged + ", " + prep_obj + ")"

        self.assert_belief(PRE_CROSS(id, dav_act_merged, act_merged))

    def get_par_number(self, s):
        count = 0
        while (s[len(s) - (count + 1)] == ")"):
            count = count + 1
        return count


class feed_precross(Action):
    def execute(self, arg1, arg2, arg3, arg4, arg5):
        id = str(arg1).split("'")[3]
        precross_dav = str(arg2).split("'")[3]
        precross_arg = str(arg3).split("'")[3]
        prep_label = str(arg4).split("'")[3]
        prep_obj = str(arg5).split("'")[3]

        new_precross_arg = prep_label + "(" + precross_arg + ", " + prep_obj + ")"

        self.assert_belief(PRE_CROSS(id, precross_dav, new_precross_arg))


class show_fol_kb(Action):
    def execute(self):
        print("\n" + str(len(kb_fol.clauses)) + " clauses in Clauses kb:\n")
        for cls in kb_fol.clauses:
            print(cls)


class clear_clauses_kb(Action):
    def execute(self):
        print("\nClauses kb initialized.")
        kb_fol.clauses = []
