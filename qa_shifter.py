
from phidias.Types import *
from phidias.Lib import *
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
COP_VERB = str(config.get('QA', 'COP_VERB')).split(", ")


# Question Answering beliefs
class AUX(Belief): pass
class SNIPPLET(Belief): pass
class SEQ(Belief): pass
class CASE(Belief): pass
class SUBJ(Belief): pass
class ROOT(Belief): pass
class OBJ(Belief): pass
class COP(Belief): pass
class getcand(Procedure): pass
class qreason(Procedure): pass
class LOC_PREP(Belief): pass
class LP(Belief): pass
class TIME_PREP(Belief): pass
class CAND(Belief): pass
class ANSWERED(Belief): pass


class join_seq(Action):
    def execute(self, *args):
       seq = str(args).split("'")
       new_seq = ""

       for s in seq:
           if s not in ['(', ', ', '', 'Variable', '), ', '))', ')']:
               if len(new_seq) == 0:
                   new_seq = s
               else:
                   new_seq = new_seq + " " + s

       print(new_seq)
       self.assert_belief(CAND(new_seq))


class aux_included(ActiveBelief):
    def evaluate(self, x):

        var = str(x).split("'")[3]
        # Check for valid aux
        if var in ['do', 'does', 'did']:
            return False
        else:
            return True


class check_null(ActiveBelief):
    def evaluate(self, x, y, z):

        var1 = str(x).split("'")[3]
        var2 = str(y).split("'")[3]
        var3 = str(z).split("'")[3]

        # Check for valid aux
        if var1 != "" and var2 != "" and var3 != "":
            return True
        else:
            return False


class check_cop(ActiveBelief):
    def evaluate(self, x):

        var = str(x).split("'")[3]

        # Check for valid aux
        if var in COP_VERB:
            return True
        else:
            return False


def_vars('X', 'Y', 'Z', 'V', 'O', 'A', 'K')


# Polar questions
getcand() / SEQ("AUX", X) >> [show_line("\nAUX+POLAR....\n"), -SEQ("AUX", X), +CAND(X)]
getcand() / SEQ(X) >> [show_line("\nPOLAR....\n"), -SEQ(X), +CAND(X)]

# Who questions
getcand() / (SEQ(X, A, Y, V, O) & CASE("who") & aux_included(A)) >> [show_line("\nWHO aux..."), -SEQ(X, A, Y, V, O), join_seq(X, Y, A, V, O, "Dummy"), getcand()]
getcand() / (SEQ(Y, V, O) & CASE("who") & COP("YES")) >> [show_line("\nWHO short inv cop..."), -SEQ(Y, V, O), join_seq("Dummy", Y, V, O), getcand()]
getcand() / (SEQ(Y, V, O) & CASE("who") & ROOT("is")) >> [show_line("\nWHO short cop..."), +COP("YES"), join_seq(O, V, Y, "Dummy"), getcand()]
getcand() / (SEQ(Y, V, O) & CASE("who") & ROOT("was")) >> [show_line("\nWHO short cop..."), +COP("YES"), join_seq(O, V, Y, "Dummy"), getcand()]
getcand() / (SEQ(Y, V, O) & CASE("who")) >> [show_line("\nWHO short..."), -SEQ(Y, V, O), join_seq(Y, V, O, "Dummy"), join_seq("Dummy", Y, V, O), getcand()]

# What questions
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("what") & aux_included(A) & check_null(X, A, Y)) >> [show_line("\nWHAT test not null..."), -SEQ(X, A, Y, V, O, K), join_seq("Dummy is", X, Y, A, V, O, K),  join_seq(X, Y, A, V, O, K, "is Dummy"), getcand()]
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("what") & check_null(X, A, Y)) >> [show_line("\nWHAT test not null 2..."), -SEQ(X, A, Y, V, O, K), join_seq("Dummy is", X, Y, V, O, K),  join_seq(X, Y, V, O, K, "is Dummy"), getcand()]
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("what") & aux_included(A) & check_cop(V)) >> [show_line("\nWHAT test cop..."), -SEQ(X, A, Y, V, O, K), join_seq("Dummy", X, Y, A, V, O, K), join_seq(K, X, Y, A, O, V, "Dummy"), getcand()]
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("what") & aux_included(A)) >> [show_line("\nWHAT test..."), -SEQ(X, A, Y, V, O, K), join_seq("Dummy", X, Y, A, V, O, K), getcand()]
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("what")) >> [show_line("\nWHAT test 2..."), -SEQ(X, A, Y, V, O, K), join_seq(X, Y, V, O, K, "Dummy"), getcand()]

# Where questions
getcand() / (SEQ(X, A, Y, V, O) & CASE("where") & aux_included(A) & LP("YES") & LOC_PREP(K)) >> [show_line("\nWHERE aux..."), -LOC_PREP(K), join_seq(X, Y, A, V, O, K, "Dummy"), getcand()]
getcand() / (SEQ(X, A, Y, V, O) & CASE("where") & aux_included(A) & LP("YES")) >> [show_line("\nWHERE aux end..."), -LP("YES"), -SEQ(X, A, Y, V, O), getcand()]
getcand() / (SEQ(X, A, Y, V, O) & CASE("where") & LP("YES") & LOC_PREP(K)) >> [show_line("\nWHERE prep: ", K), -LOC_PREP(K), join_seq(X, Y, V, O, K, "Dummy"), getcand()]
getcand() / (SEQ(X, A, Y, V, O) & CASE("where") & LP("YES")) >> [show_line("\nWHERE prep end..."), -LP("YES"), -SEQ(X, A, Y, V, O), getcand()]
getcand() / (SEQ(X, A, Y, V, O) & CASE("where") & aux_included(A)) >> [show_line("\nWHERE..."), -SEQ(X, A, Y, V, O), join_seq(X, Y, A, V, O, "Dummy"), getcand()]
getcand() / (SEQ(X, A, Y, V, O) & CASE("where")) >> [show_line("\nWHERE..."), -SEQ(X, A, Y, V, O), join_seq(X, Y, V, O, "Dummy"), getcand()]
getcand() / (SEQ(V, O) & CASE("where") & LP("YES") & LOC_PREP(K)) >> [show_line("\nWHERE short..."), -LOC_PREP(K), join_seq(O, V, K, "Dummy"), getcand()]
getcand() / (SEQ(V, O) & CASE("where") & LP("YES")) >> [show_line("\nWHERE short end..."), -LP("YES"), -SEQ(V, O), getcand()]

# When questions
getcand() / (SEQ(X, A, Y, V, O) & CASE("when") & aux_included(A) & TIME_PREP(K)) >> [show_line("\nWHEN aux..."), -TIME_PREP(K), join_seq(X, Y, A, V, O, K, "Dummy"), getcand()]
getcand() / (SEQ(X, A, Y, V, O) & CASE("when") & aux_included(A)) >> [show_line("\nWHEN aux end..."), -SEQ(X, A, Y, V, O), getcand()]
getcand() / (SEQ(X, A, Y, V, O) & CASE("when") & TIME_PREP(K)) >> [show_line("\nWHEN prep: ", K), -TIME_PREP(K), join_seq(X, Y, V, O, K, "Dummy"), getcand()]
getcand() / (SEQ(X, A, Y, V, O) & CASE("when")) >> [show_line("\nWHEN prep end..."), -SEQ(X, A, Y, V, O), getcand()]
getcand() / (SEQ(X, A, Y, V, O) & CASE("when") & aux_included(A)) >> [show_line("\nWHEN..."), -SEQ(X, A, Y, V, O), join_seq(X, Y, A, V, O, "Dummy"), getcand()]
getcand() / (SEQ(X, A, Y, V, O) & CASE("when")) >> [show_line("\nWHEN..."), -SEQ(X, A, Y, V, O), join_seq(X, Y, V, O, "Dummy"), getcand()]
getcand() / (SEQ(X, V, O) & CASE("when") & TIME_PREP(K)) >> [show_line("\nWHEN short..."), -TIME_PREP(K), join_seq(X, V, O, K, "Dummy"), getcand()]
getcand() / (SEQ(X, V, O) & CASE("when")) >> [show_line("\nWHEN short end..."), -SEQ(X, V, O), getcand()]

getcand() / (CASE(X) & ROOT(Y) & COP("YES")) >> [show_line("\nqreason ended copular..."), -CASE(X), -ROOT(Y), -COP("YES")]
getcand() / (CASE(X) & ROOT(Y)) >> [show_line("\nqreason ended normal..."), -CASE(X), -ROOT(Y)]

