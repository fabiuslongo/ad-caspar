
from phidias.Lib import *
from actions import *


# ROUTINES PARSER

parse_routine() >> [aggr_ent_conds(), produce_mod_conds(), produce_conds(), aggr_ent_rt(), produce_mod_rt(), produce_routine(), show_time()]

# --------- conditional section ---------

# aggregate grounds terms sharing same arguments
aggr_ent_conds() / (COND_GROUND(M, X, Y) & COND_GROUND(N, X, Z) & gt(N, M)) >> [-COND_GROUND(M, X, Y), -COND_GROUND(N, X, Z), join_cond_grounds(X, Y, Z), aggr_ent_conds()]

# turning ground mod into action mod
produce_mod_conds() / (COND_PRE_MOD(Y, M, K) & COND_PRE_MOD(N, J, Y)) >> [-COND_PRE_MOD(Y, M, K), +COND_PRE_MOD(N, M, K), produce_mod_conds()]
produce_mod_conds() / (COND_PRE_MOD(Z, M, K) & PRE_COND(I, V, D, X, Z)) >> [-COND_PRE_MOD(Z, M, K), +COND_PRE_MOD(D, M, K), produce_mod_conds()]
# grounding mod terms
produce_mod_conds() / (COND_GROUND(M, Z, W) & COND_PRE_MOD(X, Y, Z)) >> [-COND_PRE_MOD(X, Y, Z), -COND_GROUND(M, Z, W), produce_mod_conds()]

# grounding pre-conditionals subject terms
produce_conds() / (PRE_COND(I, V, D, X, Y) & COND_GROUND(M, X, J)) >> [-COND_GROUND(M, X, J), -PRE_COND(I, V, D, X, Y), +PRE_COND(I, V, D, J, Y), produce_conds()]
# grounding pre-conditionals object terms
produce_conds() / (PRE_COND(I, V, D, X, Y) & COND_GROUND(M, Y, J)) >> [-COND_GROUND(M, Y, J), -PRE_COND(I, V, D, X, Y), +PRE_COND(I, V, D, X, J), produce_conds()]
# asserting conditionals
produce_conds() / PRE_COND(I, V, D, X, Y) >> [-PRE_COND(I, V, D, X, Y), +COND(I, V, X, Y), produce_conds()]

# --------- routines section ---------

# aggregate grounds terms sharing same arguments
aggr_ent_rt() / (ROUTINE_GROUND(M, X, Y) & ROUTINE_GROUND(N, X, Z) & gt(N, M)) >> [-ROUTINE_GROUND(M, X, Y), -ROUTINE_GROUND(N, X, Z), join_routine_grounds(X, Y, Z), aggr_ent_rt()]

# turning ground mod into action mod
produce_mod_rt() / (ROUTINE_PRE_MOD(X, M, K) & PRE_ROUTINE(I, V, D, X, L, T)) >> [-ROUTINE_PRE_MOD(X, M, K) , +ROUTINE_PRE_MOD(D, M, K), produce_mod_rt()]
# grounding mod terms
produce_mod_rt() / (ROUTINE_GROUND(M, Z, W) & ROUTINE_PRE_MOD(X, Y, Z)) >> [-ROUTINE_PRE_MOD(X, Y, Z), -ROUTINE_GROUND(M, Z, W), +ROUTINE_MOD(X, Y, W), produce_mod_rt()]

# grounding pre-routines terms
produce_routine() / (PRE_ROUTINE(I, V, D, X, L, T) & ROUTINE_GROUND(M, X, W)) >> [-ROUTINE_GROUND(M, X, W), -PRE_ROUTINE(I, V, D, X, L, T), +PRE_ROUTINE(I, V, D, W, L, T), produce_routine()]
# appending pre-routines parameters
produce_routine() / (PRE_ROUTINE(I, V, D, X, L, T) & ROUTINE_MOD(D, W, K)) >> [-PRE_ROUTINE(I, V, D, X, L, T), -ROUTINE_MOD(D, W, K), append_routine_params(I, V, D, X, W, K, L, T), produce_routine()]
# appending pre-routines modificators
produce_routine() / (PRE_ROUTINE(I, V, D, X, L, T) & ROUTINE_GROUND(M, D, K)) >> [-PRE_ROUTINE(I, V, D, X, L, T), -ROUTINE_GROUND(M, D, K), append_routine_mods(I, V, D, X, K, L, T), produce_routine()]
# asserting routines
produce_routine() / PRE_ROUTINE(I, V, D, X, L, T) >> [-PRE_ROUTINE(I, V, D, X, L, T), +ROUTINE(I, V, X, L, T), produce_routine()]