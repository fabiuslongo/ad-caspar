from nltk.corpus import wordnet




class ManageFols(object):
    def __init__(self, VERBOSE, language):

        # Original sources
        self.sentences = []

        # Preliminary Knowledge base
        self.PKB = []

        self.VERBOSE = VERBOSE

        self.NEG_SYNS = ['no.r.01', 'no.r.02', 'no.r.03', 'not.r.01']
        self.ISA_SYNS = ['be.v.01', 'be.v.02', 'equal.v.01', 'be.v.08', 'embody.v.02']

        self.language = language


    def get_PKB(self):
        return self.PKB


    def add_PKB(self, element):
        self.PKB.append(element)


    def get_pos(self, s):
        s_list = s.split(':')
        if len(s_list) > 1:
            return s_list[1]
        else:
            return s_list[0]


    def get_lemma(self, s):
        s_list = s.split(':')
        return s_list[0]


    def build_fol(self, table, dav):

        fol = []

        ACTIONS = table[0]
        VARLIST = table[1]
        PREPS = table[2]
        BINDINGS = table[3]
        COMPOUNDS = table[4]

        # building actions predicates

        for act in ACTIONS:

            first_arg = '__'
            second_arg = '__'

            # scanning var_list

            for v in VARLIST:

                if v[0] == act[1]:
                    # adding adverb term to fol
                    var = []
                    var.append(v[1])
                    var.append(v[0])

                    if var not in fol:
                        fol.append(var)

                if act[2][0] == dav:
                    first_arg = act[2]

                elif v[0] == act[2] and v[1] != '?':

                    # adding grounded first argument to fol
                    var = []
                    var.append(v[1])
                    var.append(v[0])

                    if var not in fol:
                        fol.append(var)

                    first_arg = act[2]

                if act[3][0] == dav:
                    second_arg = act[3]

                elif v[0] == act[3] and v[1] != '?':

                    # adding grounded second argument to fol
                    var = []
                    var.append(v[1])
                    var.append(v[0])

                    if var not in fol:
                        fol.append(var)
                    second_arg = act[3]

            action = []
            action.append(act[0])
            action.append(act[1])
            action.append(first_arg)
            action.append(second_arg)

            fol.append(action)

        for p in PREPS:
            for v in VARLIST:
                if v[0] == p[2]:

                    prep = []
                    prep.append(p[0])
                    prep.append(p[1])

                    # check if reflective case
                    if v[1] == '?':
                        prep.append(' __')
                    else:
                        prep.append(p[2])

                    fol.append(prep)

                    if v[1] != '?':

                        var = []
                        var.append(v[1])
                        var.append(v[0])

                        if var not in fol:
                            fol.append(var)

        for b in BINDINGS:

            # looking into compounds for possible bindings
            for c in COMPOUNDS:
                if c[0] == b[1]:
                    for v in VARLIST:
                        if v[1] == b[0]:
                            bind = []
                            bind.append(c[1])
                            bind.append(v[0])
                            fol.append(bind)

            for v in VARLIST:
                if v[1] == b[0]:
                    bind = []
                    bind.append(b[1])
                    bind.append(v[0])
                    fol.append(bind)

            ACT_CONJ_PRESENT = False

            # check for actions existence
            for act_conj in ACTIONS:
                if act_conj[0] == b[1]:
                    ACT_CONJ_PRESENT = True

            if ACT_CONJ_PRESENT is False:
                for act_conj in ACTIONS:
                    if act_conj[0] == b[0]:
                        new_act = act_conj
                        new_act[0] = b[1]

                        arg1_present = True
                        arg2_present = True

                        for v in VARLIST:
                            if v[0] == new_act[2] and v[1] == '?':
                                arg1_present = False
                            if v[0] == new_act[3] and v[1] == '?':
                                arg2_present = False

                        if arg1_present is False:
                            new_act[2] = '__'

                        if arg2_present is False:
                            new_act[3] = '__'

                        fol.append(new_act)

        # commons direct var linked compounds
        for b in COMPOUNDS:
            for v in VARLIST:
                if v[1] == b[0]:
                    comp = []
                    comp.append(b[1])
                    comp.append(v[0])
                    fol.append(comp)

        return fol


    def build_LR_fol(self, table, dav):

        fol = []

        ACTIONS = table[0]
        VARLIST = table[1]
        PREPS = table[2]
        BINDINGS = table[3]
        COMPOUNDS = table[4]
        CONDITIONALS = table[5]

        LHS_temp = []

        RHS_temp = []

        # building compounds predicates

        for b in COMPOUNDS:
            for v in VARLIST:
                if v[1] == b[0]:
                    comp = []
                    comp.append(b[1])
                    comp.append(v[0])
                    fol.append(comp)

        # building bindings predicates

        for b in BINDINGS:

            # looking into compounds for possible bindings
            for c in COMPOUNDS:
                if c[0] == b[1]:
                    for v in VARLIST:
                        if v[1] == b[0]:
                            bind = []
                            bind.append(c[1])
                            bind.append(v[0])
                            fol.append(bind)

            # looking direct var bindings
            for v in VARLIST:
                if v[1] == b[0]:
                    bind = []
                    bind.append(b[1])
                    bind.append(v[0])
                    fol.append(bind)

            ACT_CONJ_PRESENT = False

            #check for actions existence
            for act_conj in ACTIONS:
                if act_conj[0] == b[1]:
                    ACT_CONJ_PRESENT = True

            if ACT_CONJ_PRESENT is False:
                for act_conj in ACTIONS:
                    if act_conj[0] == b[0]:
                        new_act = act_conj
                        new_act[0] = b[1]

                        arg1_present = True
                        arg2_present = True

                        for v in VARLIST:
                            if v[0] == new_act[2] and v[1] == '?':
                                arg1_present = False
                            if v[0] == new_act[3] and v[1] == '?':
                                arg2_present = False

                        if arg1_present is False:
                            new_act[2] = '__'

                        if arg2_present is False:
                            new_act[3] = '__'

                        fol.append(new_act)

        #building actions predicates

        for act in ACTIONS:

            first_arg = '__'
            second_arg = '__'

            #scanning var_list

            for v in VARLIST:

                if v[0] == act[1]:
                    # adding adverb term to fol
                    var =[]
                    var.append(v[1])
                    var.append(v[0])

                    if var not in fol:
                        fol.append(var)

                if act[2][0] == dav:
                    first_arg = act[2]

                elif v[0] == act[2] and v[1] != '?':

                    # adding grounded first argument to fol
                    var = []
                    var.append(v[1])
                    var.append(v[0])

                    if var not in fol:
                        fol.append(var)

                    first_arg = act[2]

                if act[3][0] == dav:
                    second_arg = act[3]

                elif v[0] == act[3] and v[1] != '?':

                    # adding grounded second argument to fol
                    var = []
                    var.append(v[1])
                    var.append(v[0])

                    if var not in fol:
                        fol.append(var)
                    second_arg = act[3]

            action = []
            action.append(act[0])
            action.append(act[1])
            action.append(first_arg)
            action.append(second_arg)

            fol.append(action)

        for p in PREPS:
            for v in VARLIST:
                if v[0] == p[2]:

                    prep = []
                    prep.append(p[0])
                    prep.append(p[1])

                    # check if reflective case
                    if v[1] == '?':
                        prep.append(' __')
                    else:
                        prep.append(p[2])

                    fol.append(prep)

                    if v[1] != '?':
                        var = []
                        var.append(v[1])
                        var.append(v[0])

                        if var not in fol:
                            fol.append(var)

        if len(CONDITIONALS) > 0:

            # initilized preliminary LHS
            for cond in CONDITIONALS:
                for term in fol:
                    if cond in term:
                        if len(term) == 4:
                            if term[1] == cond:
                                LHS_temp.append(term)
                        else:
                            LHS_temp.append(term)

            #print("\nLHS_temp: "+str(LHS_temp))

            left_RHS_inserted = []

            # initialized preliminary RHS and Inserted vector
            for term in fol:
                if term not in LHS_temp:
                    RHS_temp.append(term)
                    left_RHS_inserted.append(False)

            #print("RHS_temp: " + str(RHS_temp))

            new_LHS1_temp = LHS_temp[:]

            for l in LHS_temp:
                for i in range(len(RHS_temp)):
                    # ground terms case
                    if len(RHS_temp[i]) == 2:
                        if RHS_temp[i][1] in l and RHS_temp[i] not in new_LHS1_temp:
                            new_LHS1_temp.append(RHS_temp[i])
                            left_RHS_inserted[i] = True
                    # prepositions terms case
                    elif len(RHS_temp[i]) == 3:
                        if RHS_temp[i][1] in l and RHS_temp[i] not in new_LHS1_temp:
                            new_LHS1_temp.append(RHS_temp[i])
                            left_RHS_inserted[i] = True
                        if RHS_temp[i][2] in l and RHS_temp[i] not in new_LHS1_temp:
                            new_LHS1_temp.append(RHS_temp[i])
                            left_RHS_inserted[i] = True

            #print("\nnew_LHS1_temp: " + str(new_LHS1_temp))

            new_LHS2_temp = new_LHS1_temp[:]

            for l in new_LHS1_temp:
                for i in range(len(RHS_temp)):
                    # ground terms case
                    if len(RHS_temp[i]) == 2:
                        if RHS_temp[i][1] in l:
                            if left_RHS_inserted[i] is False:
                                new_LHS2_temp.append(RHS_temp[i])
                    # prepositions terms case
                    if len(RHS_temp[i]) == 3:
                        if RHS_temp[i][1] in l:
                            if left_RHS_inserted[i] is False:
                                new_LHS2_temp.append(RHS_temp[i])
                        if RHS_temp[i][2] in l:
                            if left_RHS_inserted[i] is False:
                                new_LHS2_temp.append(RHS_temp[i])

            #print("\nnew_LHS2_temp: " + str(new_LHS2_temp))

            new_RHS1_temp = RHS_temp[:]

            # non-related prepositions elimination
            for term_est in RHS_temp:
                if len(term_est) == 3:
                    PREP_OK = False
                    for term_int in RHS_temp:
                        if len(term_int) == 4:
                            if term_est[1] in term_int:
                                PREP_OK = True
                            elif term_est[2] in term_int:
                                PREP_OK = True
                        if len(term_int) == 3:
                            if term_est[1] in term_int:
                                PREP_OK = True
                            elif term_est[2] in term_int:
                                PREP_OK = True
                    if PREP_OK == False:
                        new_RHS1_temp.remove(term_est)

            #print("\nnew_RHS1_temp: " + str(new_RHS1_temp))

            new_RHS2_temp = new_RHS1_temp[:]

            # non-related ground terms elimination
            for term_est in new_RHS1_temp:
                if len(term_est) == 2:
                    TERM_OK = False
                    for term_int in new_RHS1_temp:
                        if len(term_int) == 4:
                            if term_est[1] in term_int:
                                TERM_OK = True
                        if len(term_int) == 3:
                            if term_est[1] in term_int:
                                TERM_OK = True
                    if TERM_OK == False:
                        new_RHS2_temp.remove(term_est)

            #print("\nnew_RHS2_temp: " + str(new_RHS2_temp))
            #print("\n----------------------------------")

            fol = []
            implication = ['==>']

            fol.append(new_LHS2_temp)
            fol.append(implication)
            fol.append(new_RHS2_temp)

        return fol


    def term_vect_to_gentle_term(self, term):
        # action case
        gentle_term = []
        if len(term) == 4:
            gentle_term.append(str(term[0]) + '(' + str(term[1]) + ', ' + str(term[2]) + ', ' + str(term[3]) + ')')

        # preposition case
        elif len(term) == 3:
            gentle_term.append(str(term[0]) + '(' + str(term[1]) + ', ' + str(term[2]) + ')')

        # ground case
        else:
            gentle_term.append(str(term[0]) + '(' + str(term[1]) + ')')
        return gentle_term


    def fol_vect_to_gentle_fol(self, fol_vect):

        gentle_table = []

        if len(fol_vect) > 1 and fol_vect[1] == "==>":

            LHS = []

            #build LSH
            for term in fol_vect[0]:

                    # action case
                    if len(term) == 4:
                        new_term = str(term[0])+'('+str(term[1])+', '+str(term[2])+', '+str(term[3])+')'
                        LHS.append(new_term)

                    # preposition case
                    elif len(term) == 3:
                        new_term = str(term[0])+'('+str(term[1])+', '+str(term[2])+')'
                        LHS.append(new_term)

                    # ground case
                    elif len(term) == 2:
                        new_term = str(term[0])+'('+str(term[1])+')'
                        LHS.append(new_term)

            # adding ==> symbol
            gentle_table.append(LHS)
            gentle_table.append('==>')

            RHS = []

            # build RSH
            for term in fol_vect[2]:

                # action case
                if len(term) == 4:
                    new_term = str(term[0]) + '(' + str(term[1]) + ', ' + str(term[2]) + ', ' + str(term[3]) + ')'
                    RHS.append(new_term)

                # preposition case
                elif len(term) == 3:
                    new_term = str(term[0]) + '(' + str(term[1]) + ', ' + str(term[2]) + ')'
                    RHS.append(new_term)

                # ground case
                elif len(term) == 2:
                    new_term = str(term[0]) + '(' + str(term[1]) + ')'
                    RHS.append(new_term)

            gentle_table.append(RHS)

        else:

            # build normal formula
            for term in fol_vect:

                    # action case
                    if len(term) == 4:
                        new_term = str(term[0])+'('+str(term[1])+', '+str(term[2])+', '+str(term[3])+')'
                        gentle_table.append(new_term)

                    # preposition case
                    elif len(term) == 3:
                        new_term = str(term[0])+'('+str(term[1])+', '+str(term[2])+')'
                        gentle_table.append(new_term)

                    # ground case
                    elif len(term) == 2:
                        new_term = str(term[0])+'('+str(term[1])+')'
                        gentle_table.append(new_term)

        return gentle_table


    def check_implication(self, clause_vect):
        if len(clause_vect) == 3:
            if clause_vect[1][0] == '==>':
                return True
        return False


    def check_neg(self, word):
        pos = wordnet.ADV
        syns = wordnet.synsets(word, pos=pos, lang=self.language)
        for synset in syns:
            if str(synset.name()) in self.NEG_SYNS:
                return True
        return False


    def check_be(self, word):
        pos = wordnet.VERB
        syns = wordnet.synsets(word, pos=pos, lang=self.language)
        for synset in syns:
            if str(synset.name()) in self.ISA_SYNS:
                return True
        return False


    def check_isa(self, vect_fol, deps):
        NEG_BE_PRESENT = False
        dav_neg = []
        verb_be = ""

        #creating list of negations
        for f in vect_fol:
            lemma = self.get_lemma(f[0])
            if self.check_neg(lemma[:-2]):
                dav_neg.append(f[1])

        # searching davidsonian neg into "be" actions
        for f in vect_fol:
            lemma = self.get_lemma(str(f[0]))
            if self.check_be(lemma[:-2]):
                for dn in dav_neg:
                    if dn in f:
                        NEG_BE_PRESENT = True
                        verb_be = f[0]
        for d in deps:
            if d[0] == 'ROOT':
                lemma = self.get_lemma(d[1])
                pos = self.get_pos(d[1])
                if self.check_be(lemma[:-2]) and pos in ['VBZ', 'VBP']:
                    if NEG_BE_PRESENT:
                        if d[1] == verb_be:
                            return False
                    else:
                        return True
        return False


    def check_for_rule(self, deps, fol):
        for d in deps:
            if d[0] == 'ROOT':
                lemma = self.get_lemma(d[1])
                pos = self.get_pos(d[1])
                if self.check_be(lemma[:-2]) and pos in ['VBZ', 'VBP']:
                    for f in fol:
                        if d[1] in f:
                            if f[3] != "__":
                                return True
        return False


    def build_isa_fol(self, fol, deps):
        isa_fol = []
        isa_term = ""
        subj = ""
        d = ""
        root_value = ""

        # getting the ROOT value (governor-dependent)
        for dep in deps:
            if dep[0] == 'ROOT':
                root_value = dep[1]

        # getting subject-object related to ROOT
        for f in fol:
            if f[0] == root_value:
                d = f[1]
                subj = f[2]
                isa_term = f

        lhs = []
        rhs = []
        rhs_temp = []

        for f in fol:
            if f != isa_term:
                if subj in f or d in f:
                    lhs.append(f)
                else:
                    rhs_temp.append(f)

        # preposition and adverb cases
        for r in rhs_temp:
            term_inserted = False
            for l in lhs:
                if d in l and l != isa_term:
                    if l[2] in r:
                        lhs.append(r)
                        term_inserted = True
            if term_inserted == False:
                rhs.append(r)

        #checking related lhs terms in rhs
        for l in lhs:

            remove_list = []

            if len(l) == 4:
                for r in rhs:
                    if l[1] in r or l[3] in r:
                        remove_list.append(r)

            if len(l) == 3:
                for r in rhs:
                    if l[2] in r:
                        remove_list.append(r)

            for rem in remove_list:
                rhs.remove(rem)
                lhs.append(rem)

        isa_fol.append(lhs)
        isa_fol.append(isa_term)
        isa_fol.append(rhs)

        return isa_fol


    def vect_LR_to_gentle_LR(self, LR_fol, deps, check_implication, check_isa):

        gentle_LR_fol = []

        if check_implication is False:

            if check_isa:
                # isa case
                isa_fol = self.build_isa_fol(LR_fol, deps)

                # LHS
                if len(isa_fol[0]) == 1:
                    lhs = self.term_vect_to_gentle_term(isa_fol[0][0])
                else:
                    lhs = self.fol_vect_to_gentle_fol(self.fol_to_nocount(isa_fol[0]))
                # ISA action
                middle = self.term_vect_to_gentle_term(self.term_to_nocount(isa_fol[1]))

                # RHS
                if len(isa_fol[2]) == 1:
                    rhs = self.term_vect_to_gentle_term(isa_fol[2][0])
                else:
                    rhs = self.fol_vect_to_gentle_fol(self.fol_to_nocount(isa_fol[2]))

                gentle_LR_fol.append(lhs)
                gentle_LR_fol.append(middle)
                gentle_LR_fol.append(rhs)

            else:
                # flat case
                gentle_LR_fol = self.fol_vect_to_gentle_fol(self.fol_to_nocount(LR_fol))

        else:
            # implication case
            lhs = rhs = []

            # LHS
            if len(LR_fol[0]) > 0:
                lhs = self.fol_vect_to_gentle_fol(self.fol_to_nocount(LR_fol[0]))

            # implication symbol
            middle = []
            middle.append(LR_fol[1])

            # RHS
            if len(LR_fol[2]) > 0:
                rhs = self.fol_vect_to_gentle_fol(self.fol_to_nocount(LR_fol[2]))

            gentle_LR_fol.append(lhs)
            gentle_LR_fol.append(middle)
            gentle_LR_fol.append(rhs)

        return gentle_LR_fol


    def term_to_nocount(self, term):
       new_term = []
       total_lemma_nocount = ""
       total_lemma_count = term[0].split('_')
       for i in range(len(total_lemma_count)):
           lemma_nocount = self.get_lemma(total_lemma_count[i])[:-2]
           pos = self.get_pos(total_lemma_count[i])

           if i == 0:
               total_lemma_nocount = lemma_nocount + ":" + pos
           else:
               total_lemma_nocount = total_lemma_nocount+"_"+lemma_nocount + ":" + pos

       new_term.append(total_lemma_nocount)
       for i in range(1, len(term)):
           new_term.append(term[i])
       return new_term


    def fol_to_nocount(self, fol):
        nocount_fol = []
        for term in fol:
            new_term = self.term_to_nocount(term)
            nocount_fol.append(new_term)
        return nocount_fol


    def count_vect_from_lemma(self, lemma):
        count_vect = []
        lemma_vect = lemma.split(":")
        for i in range(len(lemma_vect) - 1):
            count_vect.append(lemma_vect[i][-2:])
        return count_vect


    def vect_LR_plus_isa(self, LR_fol, deps, check_implication, check_isa):

        vect_LR_fol = []

        if check_implication is False:
            if check_isa:
                lhs = rhs = []

                # isa case
                isa_fol = self.build_isa_fol(LR_fol, deps)

                # LHS
                if len(isa_fol[0][0]) == 1:
                    lhs.append(self.term_to_nocount(isa_fol[0][0]))
                else:
                    lhs = self.fol_to_nocount(isa_fol[0])

                # RHS
                if len(isa_fol[2][0]) == 1:
                    rhs.append(self.term_to_nocount(isa_fol[2][0]))
                else:
                    rhs = self.fol_to_nocount(isa_fol[2])

                vect_LR_fol.append(lhs)
                vect_LR_fol.append(self.term_to_nocount(isa_fol[1]))
                vect_LR_fol.append(rhs)

            else:
                # flat case
                vect_LR_fol = self.fol_to_nocount(LR_fol)

        else:
            # implication case
            lhs = rhs = []

            # LHS
            if len(LR_fol[0]) > 0:
                lhs = self.fol_to_nocount(LR_fol[0])

            # implication symbol
            middle = []
            middle.append(LR_fol[1])

            # RHS
            if len(LR_fol[2]) > 0:
                rhs = self.fol_to_nocount(LR_fol[2])

            vect_LR_fol.append(lhs)
            vect_LR_fol.append(middle)
            vect_LR_fol.append(rhs)

        return vect_LR_fol


    def seek_and_change_var(self, fol, origin_var, dest_var):
        new_fol = fol[:]
        for i in range(len(fol)):
            for j in range(len(fol[i])):
                if fol[i][j] == origin_var:
                    fol[i][j] = dest_var
        return new_fol


    def isa_fol_to_clause(self, isa_fol):
        new_isa_fol = []
        subj_var = isa_fol[1][2]
        obj_var = isa_fol[1][3]

        lhs = self.seek_and_change_var(isa_fol[0], subj_var, "x")
        rhs = self.seek_and_change_var(isa_fol[2], obj_var, "x")

        middle = ["==>"]

        new_isa_fol.append(lhs)
        new_isa_fol.append(middle)
        new_isa_fol.append(rhs)

        return new_isa_fol

