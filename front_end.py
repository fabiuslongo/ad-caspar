
#from phidias.Types import *
from actions import *
from qa_shifter import *
from sensors import *



# SIMULATING EVENTS

# Routines
# +STT("turn off the lights in the living room, when the temperature is 25 and the time is 12.00")
# +STT("set the cooler in the bedroom to 25 degrees and cut the grass in the garden, when the time is 12.00")

# Direct Commands
# +STT("set the cooler at 27 degrees in the bedroom")
# +STT("turn off the lights in the living room")

# definite clauses for reasoning purposes
c1() >> [+TEST("Cuba is an hostile nation")]
c2() >> [+TEST("Colonel West is American")]
c3() >> [+TEST("Missiles are weapons")]
c4() >> [+TEST("Colonel West sells missiles to Cuba")]
c5() >> [+TEST("When an American sells weapons to a hostile nation, that American is a criminal")]

# Query
q() >> [reset_ct(), +STT("Colonel West is a criminal?")]

+TEST(X) >> [reset_ct(), parse_rules(X, "DISOK"), parse_deps(), feed_mst(), +PROCESS_STORED_MST("OK")]



# simulating keywords
d() >> [show_line("\ndomotic mode on....."), set_wait(), +WAKE("ON"), -REASON("ON"), -LISTEN("ON")]
l() >> [show_line("\nlistening mode on....."), set_wait(), +WAKE("ON"), -REASON("ON"), +LISTEN("ON")]
r() >> [show_line("\nreasoning mode on....."), set_wait(), +WAKE("ON"), -LISTEN('ON'), +REASON("ON")]

t() >> [go(), r()]

# simulating sensors
s1() >> [simulate_sensor("Be", "Time", "12.00")]
s2() >> [simulate_sensor("Be", "Temperature", "25")]





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

# chat bot wake word
+message(C, "hello") / WAIT(W) >> [Reply(C, "Hello!"), +WAKE("ON"), +CHAT_ID(C), Timer(W).start]
+message(C, X) / WAKE("ON") >> [reset_ct(), +CHAT_ID(C), +MSG(X), Timer(W).start]

# Assertion detected
+MSG(X) / (CHAT_ID(C) & check_last_char(X, ".")) >> [Reply(C, "Got it."), -REASON("ON"), +LISTEN("ON"), reset_ct(), parse_rules(X, "DISOK"), parse_deps(), feed_mst(), +PROCESS_STORED_MST("OK"), Timer(W).start]

# Question detected
+MSG(X) / (CHAT_ID(C) & check_last_char(X, "?")) >> [Reply(C, "Let me think..."), -LISTEN("ON"), +REASON("ON"), +STT(X), Timer(W).start]
# Domotic command detected
+MSG(X) / CHAT_ID(C) >> [Reply(C, "Domotic command detected..."), +STT(X), Timer(W).start]

# Give back X as chatbot answer
+OUT(X) / CHAT_ID(C) >> [Reply(C, X), Timer(W).start]


# Reasoning
+STT(X) / (WAKE("ON") & REASON("ON")) >> [show_line("\nTurning question into fact shapes....\n"), reset_ct(), assert_sequence(X, "DISOK"), getcand(), qreason(), tense_debt_paid()]

qreason() / (CAND(X) & WAKE("ON") & REASON("ON") & ANSWERED('YES')) >> [-CAND(X), qreason()]

qreason() / (CAND(X) & WAKE("ON") & REASON("ON")) >> [show_line("\nProcessing candidate....", X), -CAND(X), +GEN_MASK("FULL"), parse_rules(X, "DISOK"), parse_deps(), feed_mst(), new_def_clause("ONE", "NOMINAL"), Reset_var_cnt(), qreason()]

qreason() / (WAKE("ON") & REASON("ON") & ANSWERED('YES') & RELATED(X)) >> [-RELATED(X), +OUT(X), qreason()]
qreason() / (WAKE("ON") & REASON("ON") & ANSWERED('YES')) >> [-ANSWERED('YES')]
qreason() / (WAKE("ON") & REASON("ON") & RELATED(X)) >> [-RELATED(X), +OUT(X), qreason()]




# Nominal clauses assertion --> single: FULL", "ONE" ---  multiple: "BASE", "MORE"
+PROCESS_STORED_MST("OK") / (WAKE("ON") & LISTEN("ON")) >> [show_line("\nGot it.\n"), +GEN_MASK("BASE"), new_def_clause("MORE", "NOMINAL"), Reset_var_cnt(), process_rule()]
# processing rules --> single: FULL", "ONE" ---  multiple: "BASE", "MORE"
process_rule() / IS_RULE("TRUE") >> [show_line("\n------> rule detected!!\n"), -IS_RULE("TRUE"), +GEN_MASK("BASE"), new_def_clause("MORE", "RULE"), Reset_var_cnt()]

# Generalization assertion
new_def_clause(M, T) / GEN_MASK("BASE") >> [-GEN_MASK("BASE"), preprocess_clause("BASE", M, T), parse(), process_clause(), new_def_clause(M, T), Reset_var_cnt()]
new_def_clause(M, T) / GEN_MASK(Y) >> [-GEN_MASK(Y), preprocess_clause(Y, M, T), parse(), process_clause(), new_def_clause(M, T), Reset_var_cnt()]
new_def_clause(M, T) / (WAIT(W) & CHAT_ID(C)) >> [show_line("\n------------- Done.\n"), Timer(W).start]
new_def_clause(M, T) / WAIT(W) >> [show_line("\n------------- Done.\n"), Timer(W).start]


# Domotic Reasoning
+STT(X) / WAKE("ON") >> [reset_ct(), show_line("\nProcessing domotic command...\n"), parse_rules(X, "NODIS"), parse_deps(), feed_mst(), assert_command(X), parse_command(), parse_routine()]

+TIMEOUT("ON") / (WAKE("ON") & LISTEN("ON") & REASON("ON") & CHAT_ID(C)) >> [show_line("Returning to sleep..."), Reply(C, "Returning to sleep..."), -WAKE("ON"), -LISTEN("ON"), -REASON("ON")]
+TIMEOUT("ON") / (WAKE("ON") & REASON("ON") & CHAT_ID(C)) >> [show_line("Returning to sleep..."), Reply(C, "Returning to sleep..."), -REASON("ON"), -WAKE("ON")]
+TIMEOUT("ON") / (WAKE("ON") & LISTEN("ON") & CHAT_ID(C)) >> [show_line("Returning to sleep..."), Reply(C, "Returning sleep..."), -LISTEN("ON"), -WAKE("ON")]
+TIMEOUT("ON") / (WAKE("ON") & CHAT_ID(C)) >> [show_line("Returning to sleep..."), Reply(C, "Returning to sleep..."), -WAKE("ON")]