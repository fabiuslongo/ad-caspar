
from phidias.Lib import *
from actions import *

# SMART ENVIRONMENT INTERFACE

+SENSOR(V, X, Y) >> [check_conds()]
check_conds() / (SENSOR(V, X, Y) & COND(I, V, X, Y) & ROUTINE(I, K, J, L, T)) >> [show_line("\nconditional met!"), -COND(I, V, X, Y), +START_ROUTINE(I), check_conds()]
check_conds() / SENSOR(V, X, Y) >> [show_line("\nbelief sensor not more needed..."), -SENSOR(V, X, Y)]

+START_ROUTINE(I) / (COND(I, V, X, Y) & ROUTINE(I, K, J, L, T)) >> [show_line("\nroutines not ready!")]
+START_ROUTINE(I) / ROUTINE(I, K, J, L, T) >> [reset_ct(), show_line("\nexecuting routine..."), -ROUTINE(I, K, J, L, T), +INTENT(K, J, L, T), +START_ROUTINE(I)]


# turn off
+INTENT(X, "Light", "Living Room", T) / lemma_in_syn(X, "change_state.v.01") >> [exec_cmd("change_state.v.01", "Light", "Living Room", T)]

# after +STT("Robert is an inhabitant"),  +STT("Robert is at home"), d2()
+INTENT(X, "Alarm", "Garage", T) / (lemma_in_syn(X, "change_state.v.01") & eval_cls("At_IN(Be_VBZ(Inhabitant_NN(x8), __), Home_NN(x10))")) >> [exec_cmd("change_state.v.01", "Alarm", "Garage", T)]
#+INTENT(X, "Alarm", "Garage", T) / (lemma_in_syn(X, "change_state.v.01") & eval_cls("Be_VBZ(Colonel_NNP_West_NNP(x1), Criminal_NN(x2))")) >> [exec_cmd("change_state.v.01", "Alarm", "Garage", T)]

# turn on
+INTENT(X, "Light", "Living Room", T) / lemma_in_syn(X, "switch.v.03") >> [exec_cmd("switch.v.03", "Light", "Living Room", T)]
+INTENT(X, "Light", Y, T) / lemma_in_syn(X, "switch.v.03") >> [show_line("\n---- Result: failed to execute the command in the specified location")]

# open
+INTENT(X, "Door", "Living Room", T) / lemma_in_syn(X, "open.v.01") >> [exec_cmd("open.v.01", "Door", "Living Room", T)]
+INTENT(X, "Door", "Kitchen", T) / lemma_in_syn(X, "open.v.01") >> [exec_cmd("open.v.01", "Door", "Kitchen", T)]
+INTENT(X, "Door", Y, T) / lemma_in_syn(X, "open.v.01") >> [show_line("\n---- Result: failed to execute the command in the specified location")]

# specify, set, determine, define, fix, limit
+INTENT(X, "Cooler", "Bedroom", T) / lemma_in_syn(X, "specify.v.02") >> [exec_cmd("specify.v.02", "Cooler", "Bedroom", T)]
+INTENT(X, "Cooler", Y, T) / lemma_in_syn(X, "specify.v.02") >> [show_line("\n---- Result: failed to execute the command in the specified location")]

# cut
+INTENT(X, "Grass", "Garden", T) / lemma_in_syn(X, "cut.v.01",) >> [exec_cmd("cut.v.01", "Grass", "Garden", T)]
+INTENT(X, "cut.v.01", "grass", Y, T) / lemma_in_syn(X, "cut.v.01",) >> [show_line("\n---- Result: failed to execute the command in the specified location")]


# any other commands
+INTENT(V, X, L, T) >> [show_line("\n---- Result: failed to execute the command: ", V), show_time()]
