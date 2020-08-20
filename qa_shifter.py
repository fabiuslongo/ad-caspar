
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
       #self.assert_belief(CAND(new_seq))


class aux_included(ActiveBelief):
    def evaluate(self, x):

        var = str(x).split("'")[3]
        # Check for valid aux
        if var in ['do', 'does', 'did']:
            return False
        else:
            return True


class all_not_null(ActiveBelief):
    def evaluate(self, x, y, z):

        var1 = str(x).split("'")[3]
        var2 = str(y).split("'")[3]
        var3 = str(z).split("'")[3]

        # Check for valid aux
        if var1 != "" and var2 != "" and var3 != "":
            return True
        else:
            return False


class null(ActiveBelief):
    def evaluate(self, *args):

        vars = str(args).split("'")

        for i in range(3, len(vars)-1, 4):
            if vars[i] != "":
                return False
        return True


class check_cop(ActiveBelief):
    def evaluate(self, x):

        var = str(x).split("'")[3]

        # Check for valid aux
        if var in COP_VERB:
            return True
        else:
            return False


def_vars('X', 'Y', 'Z', 'V', 'O', 'A', 'K')


# POLAR
getcand() / SEQ("AUX", X) >> [show_line("\nAUX+POLAR....\n"), -SEQ("AUX", X), +CAND(X)]
getcand() / SEQ(X) >> [show_line("\nPOLAR....\n"), -SEQ(X), +CAND(X)]

# --- WHO ---
# who is Donald Trump?
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("who") & null(X, A, Y) & check_cop(V)) >> [show_line("\nWHO cop 3 null..."), -SEQ(X, A, Y, V, O, K), join_seq("Dummy", V, O, K), join_seq(K, V, O, "Dummy"), getcand()]
# who wants to be king?
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("who") & null(X, A, Y)) >> [show_line("\nWHO 3 null..."), -SEQ(X, A, Y, V, O, K), join_seq("Dummy", V, O, K), getcand()]
# who could be the president of United States?
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("who") & null(X, Y) & aux_included(A)) >> [show_line("\nWHO aux 2 null.."), -SEQ(X, A, Y, V, O, K), join_seq("Dummy", X, Y, A, V, O, K), getcand()]
# Who could it be?
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("who") & aux_included(A)) >> [show_line("\nWHO aux..."), -SEQ(X, A, Y, V, O, K), join_seq(X, Y, A, V, O, "Dummy"), getcand()]
# Who did you see?
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("who")) >> [show_line("\nWHO normal..."), -SEQ(X, A, Y, V, O, K), join_seq(X, Y, V, O, K, "Dummy"), getcand()]

# --- WHAT ---
# what is a king?
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("what") & check_cop(V) & null(X, A, Y)) >> [show_line("\nWHAT cop 3 null.."), -SEQ(X, A, Y, V, O, K), join_seq("Dummy", X, Y, V, O, K), join_seq(K, X, Y, V, O, "Dummy"), getcand()]
# what is located in Nevada?
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("what") & aux_included(A) & null(X, Y)) >> [show_line("\nWHAT aux 2 null.."), -SEQ(X, A, Y, V, O, K), join_seq("Dummy", X, Y, A, V, O, K), join_seq(K, X, Y, A, V, O, "Dummy"), getcand()]
# What does Mary want?
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("what") & null(X)) >> [show_line("\nWHAT 1 null.."), -SEQ(X, A, Y, V, O, K), join_seq(X, Y, V, O, K, "Dummy"), getcand()]
# what movies have you seen recently?
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("what") & aux_included(A)) >> [show_line("\nWHAT +aux not null..."), -SEQ(X, A, Y, V, O, K), join_seq("Dummy is", X, Y, A, V, O, K),  join_seq(X, Y, A, V, O, K, "is Dummy"), getcand()]
# what qualities do you think are important in a friend?
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("what")) >> [show_line("\nWHAT -aux all not null.."), -SEQ(X, A, Y, V, O, K), join_seq("Dummy is", X, Y, V, O, K),  join_seq(X, Y, V, O, K, "is Dummy"), getcand()]

# --- WHERE ---
# where is the newspaper?
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("where") & LP("YES") & LOC_PREP(Z) & null(X, A, Y)) >> [show_line("\nWHERE short..."), -LOC_PREP(Z), join_seq(O, V, K, Z, "Dummy"), getcand()]
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("where") & LP("YES") & null(X, A, Y)) >> [show_line("\nWHERE short end..."), -LP("YES"), -SEQ(X, A, Y, V, O, K), getcand()]
# where could your brother live?
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("where") & aux_included(A) & LP("YES") & LOC_PREP(Z)) >> [show_line("\nWHERE aux..."), -LOC_PREP(Z), join_seq(X, Y, A, V, K, O, Z, "Dummy"), getcand()]
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("where") & aux_included(A) & LP("YES")) >> [show_line("\nWHERE aux end..."), -LP("YES"), -SEQ(X, A, Y, V, O, K), getcand()]
# where does your brother live?
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("where") & LP("YES") & LOC_PREP(Z)) >> [show_line("\nWHERE prep: ", Z), -LOC_PREP(Z), join_seq(X, Y, V, K, O, Z, "Dummy"), getcand()]
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("where") & LP("YES")) >> [show_line("\nWHERE prep end..."), -LP("YES"), -SEQ(X, A, Y, V, O, K), getcand()]
# where are you looking at?
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("where") & aux_included(A)) >> [show_line("\nWHERE..."), -SEQ(X, A, Y, V, O, K), join_seq(X, Y, A, V, O, "Dummy"), getcand()]
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("where")) >> [show_line("\nWHERE..."), -SEQ(X, A, Y, V, O, K), join_seq(X, Y, V, K, O, "Dummy"), getcand()]

# --- WHEN ---
# When is the Thanksgiving?
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("when") & TIME_PREP(Z) & null(X, A, Y)) >> [show_line("\nWHEN short..."), -TIME_PREP(Z), join_seq(O, V, K, Z, "Dummy"), getcand()]
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("when") & null(X, A, Y)) >> [show_line("\nWHEN short end..."), -SEQ(X, A, Y, V, O, K), getcand()]
# when could your city become a metropolis?
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("when") & aux_included(A) & TIME_PREP(Z)) >> [show_line("\nWHEN aux prep...", Z), -TIME_PREP(Z), join_seq(X, Y, A, V, K, O, Z, "Dummy"), getcand()]
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("when") & aux_included(A)) >> [show_line("\nWHEN aux prep end..."), -SEQ(X, A, Y, V, O, K), getcand()]
# when do you want to leave the country?
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("when") & TIME_PREP(Z)) >> [show_line("\nWHEN prep: ", Z), -TIME_PREP(Z), join_seq(X, Y, V, K, O, Z, "Dummy"), getcand()]
getcand() / (SEQ(X, A, Y, V, O, K) & CASE("when")) >> [show_line("\nWHEN prep end..."), -SEQ(X, A, Y, V, O, K), getcand()]

getcand() / (CASE(X) & ROOT(Y)) >> [show_line("\nqreason ended normal..."), -CASE(X), -ROOT(Y)]

