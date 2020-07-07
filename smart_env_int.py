
from phidias.Lib import *
from actions import *

# SMART ENVIRONMENT INTERFACE

+SENSOR(V, X, Y) >> [check_conds()]
check_conds() / (SENSOR(V, X, Y) & COND(I, V, X, Y) & ROUTINE(I, K, J, L, T)) >> [show_line("\nconditional met!"), -COND(I, V, X, Y), +START_ROUTINE(I), check_conds()]
check_conds() / SENSOR(V, X, Y) >> [show_line("\nbelief sensor not more needed..."), -SENSOR(V, X, Y)]

+START_ROUTINE(I) / (COND(I, V, X, Y) & ROUTINE(I, K, J, L, T)) >> [show_line("\nroutines not ready!")]
+START_ROUTINE(I) / ROUTINE(I, K, J, L, T) >> [show_line("\nexecuting routine..."), -ROUTINE(I, K, J, L, T), +INTENT(K, J, L, T), +START_ROUTINE(I)]


# turn off
+INTENT(X, "light", "living room", T) / lemma_in_syn(X, "change_state.v.01") >> [exec_cmd("change_state.v.01", "light", "living room", T)]
+INTENT(X, "alarm", "garage", T) / (lemma_in_syn(X, "change_state.v.01") & eval_cls("At_IN(Be_VBP(I_PRP(x1), __), Home_NN(x2))")) >> [exec_cmd("change_state.v.01", "alarm", "garage", T)]

# turn on
+INTENT(X, "light", "living room", T) / lemma_in_syn(X, "switch.v.03") >> [exec_cmd("switch.v.03", "light", "living room", T)]
+INTENT(X, "light", Y, T) / lemma_in_syn(X, "switch.v.03") >> [show_line("\n---- Result: failed to execute the command in the specified location")]

# open
+INTENT(X, "door", "living room", T) / lemma_in_syn(X, "open.v.01") >> [exec_cmd("open.v.01", "door", "living room", T)]
+INTENT(X, "door", "kitchen", T) / lemma_in_syn(X, "open.v.01") >> [exec_cmd("open.v.01", "door", "kitchen", T)]
+INTENT(X, "door", Y, T) / lemma_in_syn(X, "open.v.01") >> [show_line("\n---- Result: failed to execute the command in the specified location")]

# specify, set, determine, define, fix, limit
+INTENT(X, "cooler", "bedroom", T) / lemma_in_syn(X, "specify.v.02") >> [exec_cmd("specify.v.02", "cooler", "bedroom", T)]
+INTENT(X, "cooler", Y, T) / lemma_in_syn(X, "specify.v.02") >> [show_line("\n---- Result: failed to execute the command in the specified location")]

# cut
+INTENT(X, "grass", "garden", T) / lemma_in_syn(X, "cut.v.01",) >> [exec_cmd("cut.v.01", "grass", "garden", T)]
+INTENT(X, "cut.v.01", "grass", Y, T) / lemma_in_syn(X, "cut.v.01",) >> [show_line("\n---- Result: failed to execute the command in the specified location")]

# any other commands
+INTENT(V, X, L, T) >> [show_line("\n---- Result: failed to execute the command: ", V)]
