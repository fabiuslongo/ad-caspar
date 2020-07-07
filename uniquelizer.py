from collections import Counter


class Uniquelizer(object):
    def __init__(self, VERBOSE, language):

        self.VERBOSE = VERBOSE

        if language == "eng":
            self.BACK_DEPS = ['det', 'nsubj', 'compound', 'aux', 'poss', 'auxpass', 'nsubjpass', 'mark', 'csubj', 'nummod', 'quantmod', 'expl', 'amod']
            self.FORW_DEPS = ['pobj', 'attr', 'cc', 'conj', 'acomp', 'oprd', 'agent', 'xcomp', 'prt', 'relcl', 'acl', 'expl']
            self.BIDIRECT_DEPS = ['prep', 'advmod' 'advcl', 'dobj', 'npadvmod', 'punct', 'neg', 'dative']




    def morph_deps(self, deps):

        words_list = []
        for d in deps:
            words_list.append(d[2])

        counter = Counter(words_list)
        counter_cost = Counter(words_list)

        m_deps = []
        dep_vect = []

        for d in reversed(deps):
            if counter[d[1]] < 10:
                zero = "0"
            else:
                zero = ""

            new_dep = self.get_lemma(d[2]) + zero + str(counter[d[2]]) + ":" + self.get_pos(d[2])
            dep_vect.append(new_dep)
            counter[d[2]] = counter[d[2]] - 1

        count = len(dep_vect)-1

        for i in range(len(deps)):
            new_dep = []
            new_dep.append(deps[i][0])
            new_dep.append(deps[i][1])
            new_dep.append(dep_vect[count])
            m_deps.append(new_dep)
            count = count - 1

        for i in range(len(m_deps)):

            if m_deps[i][0] == "ROOT":
                m_deps[i][1] = m_deps[i][2]

            elif counter_cost[m_deps[i][1]] == 1:
                m_deps[i][1] = self.get_lemma(m_deps[i][1]) + "01:" + self.get_pos(m_deps[i][1])

            elif m_deps[i][0] in self.BACK_DEPS:
                dep = self.find_forward(m_deps[i][1], i, m_deps)
                m_deps[i][1] = dep

            elif m_deps[i][0] in self.FORW_DEPS:
                dep = self.find_backward(m_deps[i][1], i, m_deps)
                m_deps[i][1] = dep
            else:
                dep = self.find_backward(m_deps[i][1], i, m_deps)
                if dep == "NOT_FOUND":
                    dep = self.find_forward(m_deps[i][1], i, m_deps)
                    m_deps[i][1] = dep
                else:
                    m_deps[i][1] = dep

        return m_deps



    def find_forward(self, gov, start_index, deps):
        dep = "NOT_FOUND"
        for i in range(start_index+1, len(deps)):
            cleaned_dep = self.clean_from_counter(deps[i][2])
            if gov == cleaned_dep:
                return deps[i][2]
        return dep



    def find_backward(self, gov, start_index, deps):
        dep = "NOT_FOUND"
        for i in range(start_index-1, -1, -1):
            cleaned_dep = self.clean_from_counter(deps[i][2])
            if gov == cleaned_dep:
                return deps[i][2]
        return dep


    def clean_from_counter(self, dep):
        d = dep.split(':')
        cleaned_dep = d[0][0:-2]+":"+d[1]
        return cleaned_dep


    def get_pos(self, s):
        s_list = s.split(':')
        return s_list[1]


    def get_lemma(self, s):
        s_list = s.split(':')
        return s_list[0]



