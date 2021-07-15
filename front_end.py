from actions import *
from qa_shifter import *
from sensors import *

class MST_STORED(Belief): pass
class process_mst(Procedure): pass
class process_cmd(Procedure): pass

# SIMULATING EVENTS

# Routines
# turn off the lights in the living room, when the temperature is 25 and the time is 12.00
# set the cooler in the bedroom to 25 degrees and cut the grass in the garden, when the time is 12.00

# Direct Commands
# set the cooler at 27 degrees in the bedroom
# turn off the lights in the living room

# Sensors
s1() >> [simulate_sensor("Be", "Time", "12.00")]
s2() >> [simulate_sensor("Be", "Temperature", "25")]

make_feed() / TEST(X) >> [-TEST(X), reset_ct(), parse_rules(X), parse_deps(), feed_mst(), process_mst(), log_cmd("Feed", X), show_ct(), make_feed()]
make_feed() >> [show_line("\nFeeding KBs ended.\n")]

# Feeding Clauses KB with sentences in feed.txt
feed() >> [show_line("\nFeeding KBs from file....\n"), +WAKE("ON"),  +LISTEN("ON"), feed_kbs(), make_feed()]


# Front-End STT

# Start agent command
go() >> [show_line("AD-Caspar started! Bot is running..."), Chatbot().start(), set_wait()]


# show higher Clauses kb
hkb() >> [show_fol_kb()]
# show lower Clauses kb
lkb() >> [show_lkb()]

# initialize Higher Clauses Kb
chkb() >> [log_op(">>> Flushing High Clauses KB..."), clear_hkb()]
# initialize Lower Clauses Kb
clkb() >> [log_op(">>> Flushing Low Clauses KB..."), clear_lkb()]

# chatbot wake word
+message(C, "hello") / WAIT(W) >> [Reply(C, "Hello!"), +WAKE("ON"), +CHAT_ID(C), Timer(W).start()]
+message(C, X) / WAKE("ON") >> [reset_ct(), +CHAT_ID(C), +MSG(X), manage_msg(), Timer(W).start()]

# Assertion management
manage_msg() / (MSG(X) & CHAT_ID(C) & check_last_char(X, ".")) >> [Reply(C, "Got it."), -MSG(X), -REASON("ON"), +LISTEN("ON"), parse_rules(X), parse_deps(), feed_mst(), process_mst(), log_cmd("Feed", X), manage_msg()]
# Questions management
manage_msg() / (MSG(X) & CHAT_ID(C) & check_last_char(X, "?")) >> [Reply(C, "Let me think..."), -MSG(X), -LISTEN("ON"), +REASON("ON"), +STT(X), log_cmd("Query", X), qreason(), manage_msg()]
# Domotic command management
manage_msg() / (MSG(X) & CHAT_ID(C)) >> [Reply(C, "Domotic command detected"), -MSG(X), parse_rules(X), parse_deps(), feed_mst(), process_cmd(), log_cmd("IoT", X), manage_msg()]
# Ending operation
manage_msg() >> [show_ct(), show_line("\n------------- End of operations.\n"), Timer(W).start()]


# Give back X as chatbot answer
+OUT(X) / CHAT_ID(C) >> [Reply(C, X), Timer(W).start()]

# Reasoning
qreason() / (STT(X) & WAKE("ON") & REASON("ON")) >> [show_line("\nTurning question into fact shapes....\n"), -STT(X), assert_sequence(X), getcand(), tense_debt_paid(), qreason()]
qreason() / (CAND(X) & WAKE("ON") & REASON("ON") & ANSWERED('YES')) >> [-CAND(X), qreason()]
qreason() / (CAND(X) & WAKE("ON") & REASON("ON")) >> [show_line("\nProcessing candidate....", X), -CAND(X), +GEN_MASK("FULL"), parse_rules(X), parse_deps(), feed_mst(), new_def_clause("ONE", "NOMINAL"), qreason()]
qreason() / (WAKE("ON") & REASON("ON") & ANSWERED('YES') & RELATED(X)) >> [-RELATED(X), +OUT(X), qreason()]
qreason() / (WAKE("ON") & REASON("ON") & ANSWERED('YES')) >> [-ANSWERED('YES')]
qreason() / (WAKE("ON") & REASON("ON") & RELATED(X)) >> [-RELATED(X), +OUT(X), qreason()]


# Nominal clauses assertion --> single: FULL", "ONE" ---  multiple: "BASE", "MORE"
process_mst() / (WAKE("ON") & LISTEN("ON")) >> [show_line("\nGot it.\n"), +GEN_MASK("BASE"), new_def_clause("MORE", "NOMINAL"), process_rule()]
# processing rules --> single: FULL", "ONE" ---  multiple: "BASE", "MORE"
process_rule() / IS_RULE("TRUE") >> [show_line("\n------> rule detected!!\n"), -IS_RULE("TRUE"), +GEN_MASK("BASE"), new_def_clause("MORE", "RULE")]

# Generalization assertion
new_def_clause(M, T) / GEN_MASK("BASE") >> [-GEN_MASK("BASE"), preprocess_clause("BASE", M, T), parse(), process_clause(), new_def_clause(M, T)]
new_def_clause(M, T) / GEN_MASK(Y) >> [-GEN_MASK(Y), preprocess_clause(Y, M, T), parse(), process_clause(), new_def_clause(M, T)]
new_def_clause(M, T) / (WAIT(W) & CHAT_ID(C)) >> [show_line("\n------------- Done.\n"), Timer(W).start()]
new_def_clause(M, T) / WAIT(W) >> [show_line("\n------------- Done.\n"), Timer(W).start()]


# Domotic Reasoning
process_cmd() / (WAKE("ON")) >> [show_line("\nProcessing domotic command...\n"), assert_command(), parse_command(), parse_routine()]

+TIMEOUT("ON") / (WAKE("ON") & LISTEN("ON") & REASON("ON") & CHAT_ID(C)) >> [show_line("Returning to sleep..."), Reply(C, "Returning to sleep..."), -WAKE("ON"), -LISTEN("ON"), -REASON("ON")]
+TIMEOUT("ON") / (WAKE("ON") & REASON("ON") & CHAT_ID(C)) >> [show_line("Returning to sleep..."), Reply(C, "Returning to sleep..."), -REASON("ON"), -WAKE("ON")]
+TIMEOUT("ON") / (WAKE("ON") & LISTEN("ON") & CHAT_ID(C)) >> [show_line("Returning to sleep..."), Reply(C, "Returning sleep..."), -LISTEN("ON"), -WAKE("ON")]
+TIMEOUT("ON") / (WAKE("ON") & CHAT_ID(C)) >> [show_line("Returning to sleep..."), Reply(C, "Returning to sleep..."), -WAKE("ON")]