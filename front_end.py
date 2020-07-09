
from phidias.Lib import *

from actions import *
from sensors import *

# SIMULATING EVENTS

# simulating routines
r1() >> [+STT("turn off the lights in the living room, when the temperature is 25 and the time is 12.00")]
r2() >> [+STT("set the cooler in the bedroom to 25 degrees and cut the grass in the garden, when the time is 12.00")]

# simulating direct commands
d1() >> [+STT("set the cooler at 27 degrees in the bedroom")]
d2() >> [+STT("turn off the lights in the living room")]

# definite clauses for reasoning purposes
c1() >> [+STT("Nono is an hostile nation")]
c2() >> [+STT("Colonel West is American")]
c3() >> [+STT("missiles are weapons")]
c4() >> [+STT("Colonel West sells missiles to Nono")]
c5() >> [+STT("When an American sells weapons to a hostile nation, that American is a criminal")]

# Query
q() >> [+STT("Colonel West is a criminal")]


# simulating keywords
w() >> [+HOTWORD_DETECTED("ON")]
l() >> [+STT("listen")]
r() >> [+STT("reason")]

# simulating sensors
s1() >> [simulate_sensor("be", "time", "12.00")]
s2() >> [simulate_sensor("be", "temperature", "25")]

# test assertions
t() >> [go(), w(), l()]



# Front-End STT

# Start agent command
go() >> [show_line("Starting AD-Caspar..."), set_wait(), HotwordDetect().start]

# show higher Clauses kb
hkb() >> [show_fol_kb()]
# show lower Clauses kb
lkb() >> [show_lkb()]

# initialize Higher Clauses Kb
chkb() >> [clear_hkb()]
# initialize Lower Clauses Kb
clkb() >> [clear_lkb()]

# Hotwords processing
+HOTWORD_DETECTED("ON") / WAIT(W) >> [show_line("\n\nYes, I'm here!\n"), HotwordDetect().stop, UtteranceDetect().start, +WAKE("ON"), Timer(W).start]
+STT("listen") / (WAKE("ON") & WAIT(W)) >> [+LISTEN("ON"), show_line("\nWaiting for knowledge...\n"), Timer(W).start]
+STT("reason") / (WAKE("ON") & WAIT(W)) >> [+REASON("ON"), show_line("\nWaiting for query...\n"), Timer(W).start]

# Query KB
+STT(X) / (WAKE("ON") & REASON("ON")) >> [show_line("\nGot it.\n"), +GEN_MASK("FULL"), new_def_clause(X, "ONE", "NOMINAL")]

# Nominal clauses assertion --> single: FULL", "ONE" ---  multiple: "BASE", "MORE"
+STT(X) / (WAKE("ON") & LISTEN("ON")) >> [show_line("\nGot it.\n"), +GEN_MASK("BASE"), new_def_clause(X, "MORE", "NOMINAL"), process_rule()]
# processing rules --> single: FULL", "ONE" ---  multiple: "BASE", "MORE"
process_rule() / IS_RULE(X) >> [show_line("\n", X, " ----> is a rule!\n"), -IS_RULE(X), +GEN_MASK("BASE"), new_def_clause(X, "MORE", "RULE")]

# Generalization assertion
new_def_clause(X, M, T) / GEN_MASK("BASE") >> [-GEN_MASK("BASE"), preprocess_clause(X, "BASE", M, T), parse(), process_clause(), new_def_clause(X, M, T)]
new_def_clause(X, M, T) / GEN_MASK(Y) >> [-GEN_MASK(Y), preprocess_clause(X, Y, M, T), parse(), process_clause(), new_def_clause(X, M, T)]
new_def_clause(X, M, T) / WAIT(W) >> [show_line("\n------------- Done.\n"), Timer(W).start]


# Reactive Reasoning
+STT(X) / WAKE("ON") >> [UtteranceDetect().stop, -WAKE("ON"), show_line("\nProcessing domotic command...\n"), assert_command(X), parse_command(), parse_routine(), HotwordDetect().start]

+TIMEOUT("ON") / (WAKE("ON") & LISTEN("ON") & REASON("ON")) >> [show_line("\nReturning to idle state...\n"), -WAKE("ON"), -LISTEN("ON"), -REASON("ON"), UtteranceDetect().stop, HotwordDetect().start]
+TIMEOUT("ON") / (WAKE("ON") & REASON("ON")) >> [show_line("\nReturning to idle state...\n"), -REASON("ON"), -WAKE("ON"), UtteranceDetect().stop, HotwordDetect().start]
+TIMEOUT("ON") / (WAKE("ON") & LISTEN("ON")) >> [show_line("\nReturning to idle state...\n"), -LISTEN("ON"), -WAKE("ON"), UtteranceDetect().stop, HotwordDetect().start]
+TIMEOUT("ON") / WAKE("ON") >> [show_line("\nReturning to idle state...\n"), -WAKE("ON"), UtteranceDetect().stop, HotwordDetect().start]