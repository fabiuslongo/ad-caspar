
from phidias.Lib import *

from actions import *
from sensors import *

# SIMULATING EVENTS

# Routines
# turn off the lights in the living room, when the temperature is 25 and the time is 12.00
# set the cooler in the bedroom to 25 degrees and cut the grass in the garden, when the time is 12.00

# Direct Commands
# set the cooler at 27 degrees in the bedroom
# turn off the lights in the living room

# definite clauses for reasoning purposes
c1() >> [+STT("Cuba is an hostile nation")]
c2() >> [+STT("Colonel West is American")]
c3() >> [+STT("Missiles are weapons")]
c4() >> [+STT("Colonel West sells missiles to Cuba")]
c5() >> [+STT("When an American sells weapons to a hostile nation, that American is a criminal")]

# Query
q() >> [+STT("Colonel West is a criminal")]


# simulating keywords
d() >> [show_line("\ndomotic mode on....."), set_wait(), +WAKE("ON"), -REASON("ON"), -LISTEN("ON")]
l() >> [show_line("\nlistening mode on....."), set_wait(), +WAKE("ON"), -REASON("ON"), +LISTEN("ON")]
r() >> [show_line("\nreasoning mode on....."), -LISTEN('ON'), +REASON("ON")]

t() >> [show_line("\nreasoning mode on....."), set_wait(), +WAKE("ON"), -LISTEN('ON'), +REASON("ON")]

# simulating sensors
s1() >> [simulate_sensor("be", "time", "12.00")]
s2() >> [simulate_sensor("be", "temperature", "25")]


def_vars('X', 'Y', 'Z', 'T', 'W', 'K', 'J', 'M', 'N', 'D', 'I', 'V', 'L', 'O', 'E', 'U', 'C', 'A')


# Front-End STT

# Start agent command
go() >> [show_line("AD-Caspar started! Bot is running..."), Chatbot().start, set_wait()]


# show higher Clauses kb
hkb() >> [show_fol_kb()]
# show lower Clauses kb
lkb() >> [show_lkb()]

# initialize Higher Clauses Kb
chkb() >> [clear_hkb()]
# initialize Lower Clauses Kb
clkb() >> [clear_lkb()]

# managing bot beliefs
+message(C, "hello") / WAIT(W) >> [Reply(C, "Hello! ;-)"), +WAKE("ON"), +CHAT_ID(C), Timer(W).start]
+message(C, X) / WAKE("ON") >> [+CHAT_ID(C), +MSG(X), Timer(W).start]

+MSG(X) / (CHAT_ID(C) & check_last_char(X, ".")) >> [Reply(C, "Assertion detected"), +LISTEN("ON"), +STT(X), Timer(W).start]
+MSG(X) / (CHAT_ID(C) & check_last_char(X, "?")) >> [Reply(C, "Question detected"), +REASON("ON"), +STT(X), Timer(W).start]
+MSG(X) / CHAT_ID(C) >> [Reply(C, "Domotic command detected"), +STT(X), Timer(W).start]

+OUT(X) / CHAT_ID(C) >> [Reply(C, X), Timer(W).start]


# Reasoning
+STT(X) / (WAKE("ON") & REASON("ON")) >> [show_line("\nTurning question into fact shapes....\n"), assert_sequence(X), getcand(), qreason()]

# Polar questions
getcand() / SEQ("AUX", X) >> [show_line("\nAUX+POLAR....\n"), -SEQ("AUX", X), +CAND(X)]
# Who questions
getcand() / (SEQ(X, A, Y, V, O) & CASE("who") & aux_included(A)) >> [show_line("\nWHO aux..."), -SEQ(X, A, Y, V, O), join_seq(X, Y, A, V, O, "Dummy"), getcand()]
getcand() / (SEQ(Y, V, O) & CASE("who") & COP("YES")) >> [show_line("\nWHO short inv cop..."), -SEQ(Y, V, O), join_seq("Dummy", Y, V, O), getcand()]
getcand() / (SEQ(Y, V, O) & CASE("who") & ROOT("is")) >> [show_line("\nWHO short cop..."), +COP("YES"), join_seq(O, V, Y, "Dummy"), getcand()]
getcand() / (SEQ(Y, V, O) & CASE("who")) >> [show_line("\nWHO short..."), -SEQ(Y, V, O), join_seq(Y, V, O, "Dummy"), getcand()]
# What questions
getcand() / (SEQ(X, A, Y, V, O) & CASE("what") & aux_included(A)) >> [show_line("\nWHAT aux..."), -SEQ(X, A, Y, V, O), join_seq("Dummy is", X, Y, A, V, O), join_seq(X, Y, A, V, O, "is Dummy"), getcand()]
getcand() / (SEQ(X, A, Y, V, O) & CASE("what")) >> [show_line("\nWHAT copular..."), -SEQ(X, A, Y, V, O), join_seq("Dummy is", X, Y, V, O), join_seq(X, Y, V, O, "is Dummy"), getcand()]
getcand() / (SEQ(Y, V, O) & CASE("what") & COP("YES")) >> [show_line("\nWHAT short inv cop..."), -SEQ(Y, V, O), join_seq("Dummy", Y, V, O), getcand()]
getcand() / (SEQ(Y, V, O) & CASE("what") & ROOT("is")) >> [show_line("\nWHAT short cop..."), +COP("YES"), join_seq(O, V, Y, "Dummy"), getcand()]
getcand() / (SEQ(Y, V, O) & CASE("what")) >> [show_line("\nWHAT short..."), -SEQ(Y, V, O), join_seq(Y, V, O, "Dummy"), getcand()]
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
getcand() / (SEQ(V, O) & CASE("when") & TIME_PREP(K)) >> [show_line("\nWHEN short..."), -TIME_PREP(K), join_seq(O, V, K, "Dummy"), getcand()]
getcand() / (SEQ(V, O) & CASE("when")) >> [show_line("\nWHEN short end..."), -SEQ(V, O), getcand()]

getcand() / (CASE(X) & ROOT(Y) & COP("YES")) >> [show_line("\nqreason ended copular..."), -CASE(X), -ROOT(Y), -COP("YES")]
getcand() / (CASE(X) & ROOT(Y)) >> [show_line("\nqreason ended normal..."), -CASE(X), -ROOT(Y)]

qreason() / (CAND(X) & WAKE("ON") & REASON("ON")) >> [-CAND(X), +GEN_MASK("FULL"), new_def_clause(X, "ONE", "NOMINAL"), qreason()]



# Nominal clauses assertion --> single: FULL", "ONE" ---  multiple: "BASE", "MORE"
+STT(X) / (WAKE("ON") & LISTEN("ON")) >> [show_line("\nGot it.\n"), +GEN_MASK("BASE"), new_def_clause(X, "MORE", "NOMINAL"), process_rule()]
# processing rules --> single: FULL", "ONE" ---  multiple: "BASE", "MORE"
process_rule() / IS_RULE(X) >> [show_line("\n", X, " ----> is a rule!\n"), -IS_RULE(X), +GEN_MASK("BASE"), new_def_clause(X, "MORE", "RULE")]

# Generalization assertion
new_def_clause(X, M, T) / GEN_MASK("BASE") >> [-GEN_MASK("BASE"), preprocess_clause(X, "BASE", M, T), parse(), process_clause(), new_def_clause(X, M, T)]
new_def_clause(X, M, T) / GEN_MASK(Y) >> [-GEN_MASK(Y), preprocess_clause(X, Y, M, T), parse(), process_clause(), new_def_clause(X, M, T)]
new_def_clause(X, M, T) / (WAIT(W) & CHAT_ID(C)) >> [show_line("\n------------- Done.\n"), flush(), Timer(W).start]
new_def_clause(X, M, T) / WAIT(W) >> [flush(), show_line("\n------------- Done.\n"), Timer(W).start]


# Domotic Reasoning
+STT(X) / WAKE("ON") >> [show_line("\nProcessing domotic command...\n"), assert_command(X), parse_command(), parse_routine()]

+TIMEOUT("ON") / (WAKE("ON") & LISTEN("ON") & REASON("ON") & CHAT_ID(C)) >> [show_line("Returning to sleep..."), Reply(C, "Returning to sleep..."), -WAKE("ON"), -LISTEN("ON"), -REASON("ON")]
+TIMEOUT("ON") / (WAKE("ON") & REASON("ON") & CHAT_ID(C)) >> [show_line("Returning to sleep..."), Reply(C, "Returning to sleep..."), -REASON("ON"), -WAKE("ON")]
+TIMEOUT("ON") / (WAKE("ON") & LISTEN("ON") & CHAT_ID(C)) >> [show_line("Returning to sleep..."), Reply(C, "Returning sleep..."), -LISTEN("ON"), -WAKE("ON")]
+TIMEOUT("ON") / (WAKE("ON") & CHAT_ID(C)) >> [show_line("Returning to sleep..."), Reply(C, "Returning to sleep..."), -WAKE("ON")]