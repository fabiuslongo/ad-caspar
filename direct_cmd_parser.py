from phidias.Lib import *
from actions import *

# DIRECT COMMAND PARSER

parse_command() >> [aggr_entities(), produce_mod(), produce_intent()]

# aggregate grounds terms sharing same arguments
aggr_entities() / (GROUND(M, X, Y) & GROUND(N, X, Z) & gt(N, M)) >> [-GROUND(M, X, Y), -GROUND(N, X, Z), join_grounds(X, Y, Z), aggr_entities()]

# turning ground mod into action mod
produce_mod() / (PRE_MOD(Y, M, K) & PRE_MOD(D, J, Y)) >> [-PRE_MOD(Y, M, K) , +PRE_MOD(D, M, K), produce_mod()]
produce_mod() / (PRE_MOD(X, M, K) & PRE_INTENT(V, D, X, L, T)) >> [-PRE_MOD(X, M, K) , +PRE_MOD(D, M, K), produce_mod()]
# grounding mod terms
produce_mod() / (PRE_MOD(X, Y, Z) & GROUND(M, Z, W)) >> [-PRE_MOD(X, Y, Z), -GROUND(M, Z, W), +MOD(X, Y, W), produce_mod()]

# grounding pre-actions terms
produce_intent() / (PRE_INTENT(V, D, X, L, T) & GROUND(M, X, W)) >> [-GROUND(M, X, W), -PRE_INTENT(V, D, X, L, T), +PRE_INTENT(V, D, W, L, T), produce_intent()]
# appending pre-action parameters
produce_intent() / (PRE_INTENT(V, D, X, L, T) & MOD(D, W, K)) >> [-PRE_INTENT(V, D, X, L, T), -MOD(D, W, K), append_intent_params(V, D, X, W, K, L, T), produce_intent()]
# appending pre-action modificators
produce_intent() / (PRE_INTENT(V, D, X, L, T) & GROUND(M, D, K)) >> [-PRE_INTENT(V, D, X, L, T), -GROUND(M, D, K), append_intent_mods(V, D, X, K, L, T), produce_intent()]
# asserting and executing actions
produce_intent() / PRE_INTENT(V, D, X, L, T) >> [-PRE_INTENT(V, D, X, L, T), +INTENT(V, X, L, T)]