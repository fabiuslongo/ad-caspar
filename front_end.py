
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
l() >> [show_line("\nlistening mode on....."), set_wait(), +WAKE("ON"), +LISTEN("ON")]
r() >> [show_line("\nreasoning mode on....."), -LISTEN('ON'), +REASON("ON")]

t() >> [show_line("\nreasoning mode on....."), set_wait(), +WAKE("ON"), +REASON("ON")]

# simulating sensors
s1() >> [simulate_sensor("be", "time", "12.00")]
s2() >> [simulate_sensor("be", "temperature", "25")]


def_vars('X', 'Y', 'Z', 'T', 'W', 'K', 'J', 'M', 'N', 'D', 'I', 'V', 'L', 'O', 'E', 'U', 'C')


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
+STT(X) / (WAKE("ON") & REASON("ON")) >> [show_line("\nTurning into fact shape....\n"), assert_frames(X), qreason()]

qreason() / SEQUENCE("AUX", X) >> [show_line("\nAUX+POLAR case....\n"), -SEQUENCE("AUX", X), +FS_STT(X)]

qreason() / (SEQUENCE(X, Y, Z) & CASE("who") & ROOT("is") & INV_COP("YES")) >> [show_line("\nWHO case inverted copular...."), -SEQUENCE(X, Y, Z), join_seq(X, Y, Z), qreason()]
qreason() / (SEQUENCE(X, Y, Z) & CASE("who") & ROOT("is")) >> [show_line("\nWHO case normal copular...."), +INV_COP("YES"), join_seq(Z, Y, X), qreason()]
qreason() / (SEQUENCE(X, Y, Z) & CASE("who")) >> [show_line("\nWHO case normal...."), -SEQUENCE(X, Y, Z), join_seq(X, Y, Z), qreason()]
qreason() / (CASE("who") & ROOT("is") & INV_COP("YES")) >> [show_line("\nqreason ended copular...."), -CASE("who"), -ROOT("is"), -INV_COP("YES")]
qreason() / (CASE("who") & ROOT(X)) >> [show_line("\nqreason ended normal...."), -ROOT(X), -CASE("who")]

+FS_STT(X) / (WAKE("ON") & REASON("ON")) >> [+GEN_MASK("FULL"), new_def_clause(X, "ONE", "NOMINAL")]

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