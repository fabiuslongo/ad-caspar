
from phidias.Lib import *
from actions import *

# SMART ENVIRONMENT INTERFACE

+SENSOR(V, X, Y) >> [check_conds()]
check_conds() / (SENSOR(V, X, Y) & COND(I, V, X, Y) & ROUTINE(I, K, J, L, T)) >> [show_line("\nconditional met!"), -COND(I, V, X, Y), +START_ROUTINE(I), check_conds()]
check_conds() / SENSOR(V, X, Y) >> [show_line("\nbelief sensor not more needed..."), -SENSOR(V, X, Y)]

+START_ROUTINE(I) / (COND(I, V, X, Y) & ROUTINE(I, K, J, L, T)) >> [show_line("\nroutines not ready!")]
+START_ROUTINE(I) / ROUTINE(I, K, J, L, T) >> [show_line("\nexecuting routine..."), -ROUTINE(I, K, J, L, T), +INTENT(K, J, L, T), +START_ROUTINE(I)]


# turn off
+INTENT(X, "Light", "Living Room", T) / lemma_in_syn(X, "change_state.v.01") >> [+OUT("Result: execution successful"), exec_cmd("change_state.v.01", "light", "living room", T)]
+INTENT(X, "Alarm", "Garage", T) / (lemma_in_syn(X, "change_state.v.01") & eval_cls("At_IN(Be_VBP(I_PRP(x1), __), Home_NN(x2))")) >> [+OUT("Result: execution successful"), exec_cmd("change_state.v.01", "alarm", "garage", T)]

# turn on
+INTENT(X, "Light", "Living Room", T) / lemma_in_syn(X, "switch.v.03") >> [+OUT("Result: execution successful"), exec_cmd("switch.v.03", "light", "living room", T)]
+INTENT(X, "Light", Y, T) / lemma_in_syn(X, "switch.v.03") >> [+OUT("Result: execution failed in the specified location")]

# open
+INTENT(X, "Door", "Living Room", T) / lemma_in_syn(X, "open.v.01") >> [+OUT("Result: execution successful"), exec_cmd("open.v.01", "door", "living room", T)]
+INTENT(X, "Door", "Kitchen", T) / lemma_in_syn(X, "open.v.01") >> [+OUT("Result: execution successful"), exec_cmd("open.v.01", "door", "kitchen", T)]
+INTENT(X, "Door", Y, T) / lemma_in_syn(X, "open.v.01") >> [+OUT("Result: execution failed in the specified location")]

# specify, set, determine, define, fix, limit
+INTENT(X, "Cooler", "Bedroom", T) / lemma_in_syn(X, "specify.v.02") >> [+OUT("Result: execution successful"), exec_cmd("specify.v.02", "cooler", "bedroom", T)]
+INTENT(X, "Cooler", Y, T) / lemma_in_syn(X, "specify.v.02") >> [+OUT("Result: execution failed in the specified location")]

# cut
+INTENT(X, "Grass", "Garden", T) / lemma_in_syn(X, "cut.v.01",) >> [+OUT("Result: execution successful"), exec_cmd("cut.v.01", "grass", "garden", T)]
+INTENT(X, "cut.v.01", "Grass", Y, T) / lemma_in_syn(X, "cut.v.01",) >> [+OUT("Result: execution failed in the specified location")]

# any other commands
+INTENT(V, X, L, T) >> [+OUT("Result: execution failed")]
