
from phidias.Lib import *
from actions import *

# DEFINITE CLAUSES BUILDER

parse() >> [aggr_adj(), aggr_adv(), aggr_nouns(), mod_to_gnd(), gnd_prep_obj(), prep_to_gnd(), gnd_actions(), apply_adv(), actions_to_clauses(), finalize_gnd()]

# aggregate adjectives
aggr_adj() / (ADJ(I, X, L) & ADV(I, X, M)) >> [show_line("\naggregating adj-adv: ", L," - ", M), -ADJ(I, X, L), -ADV(I, X, M), aggregate("ADJ", I, X, L, M), aggr_adj()]
aggr_adj() / (ADJ(I, X, L) & ADJ(I, X, M) & neq(L, M)) >> [show_line("\naggregating adjectives: ", L," - ", M), -ADJ(I, X, L), -ADJ(I, X, M), aggregate("ADJ", I, X, L, M), aggr_adj()]
aggr_adj() / ADJ(I, X, L) >> [show_line("\nAdjectives aggregation done")]

# aggregate adverbs
aggr_adv() / (ADV(I, X, L) & ADV(I, X, M) & neq(L, M)) >> [show_line("\naggregating adverbs: ", L," - ", M), -ADV(I, X, L), -ADV(I, X, M), aggregate("ADV", I, X, L, M), aggr_adv()]
aggr_adv() / ADV(I, X, L) >> [show_line("\nAdverbs aggregation done")]

# aggregate compound nouns
aggr_nouns() / (GND(I, X, L) & GND(I, X, M) & neq(L, M)) >> [show_line("\naggregating nouns: ", L," - ", M), -GND(I, X, L), -GND(I, X, M), aggregate("NN", I, X, L, M), aggr_nouns()]
aggr_nouns() / GND(I, X, L) >> [show_line("\nNouns aggregation done.")]

# applying mods to grounds
mod_to_gnd() / (GND(I, X, L) & ADJ(I, X, M)) >> [show_line("\nadjective to ground: ", M," to ", L), -GND(I, X, L), -ADJ(I, X, M), merge(I, X, M, L), mod_to_gnd() ]
mod_to_gnd() / (GND(I, X, L) & PREP(I, D, W, X) & PREP(I, X, M, Y) & GND(I, Y, U)) >> [show_line("\nint preps...",M," - ",W), -GND(I, X, L), -PREP(I, X, M, Y), -GND(I, Y, U), int_preps_tognd(I, X, Y, M, U, L), mod_to_gnd()]
mod_to_gnd() / GND(I, X, L) >> [show_line("\nAdjective applications done.")]


# grounding object preps
gnd_prep_obj() / (PREP(I, X, L, O) & GND(I, O, M)) >> [show_line("\ngrounding object preps: ", L," <-- ", M), -PREP(I, X, L, O), -GND(I, O, M), ground_prep(I, X, L, O, M), gnd_prep_obj()]
gnd_prep_obj() / PREP(I, X, L, O) >> [show_line("\nPreposition ready: ", L)]

# applying PREP to ground
prep_to_gnd() / (PREP(I, X, L, O) & GND(I, X, M)) >> [show_line("\ngprep to ground: ", L," ---> ", M), -PREP(I, X, L, O), -GND(I, X, M), gprep_to_ground(I, X, L, O, M)]


# grounding actions

# adjective has to be applied before
gnd_actions() / (ACTION(I, V, D, X, Y) & ADJ(I, X, K) & GND(I, X, M)) >> [show_line("\nact subj not ready to be grounded (ground)..."),  mod_to_gnd(), gnd_actions()]
# prep is turned into a ground
gnd_actions() / (ACTION(I, V, D, X, Y) & PREP(I, X, L, O)) >> [show_line("\nact subj not ready to be grounded (prep)..."), prep_to_gnd(), gnd_actions()]
# applying grounds to actions object
gnd_actions() / (ACTION(I, V, D, X, Y) & GND(I, X, M)) >> [show_line("\ngrounds to actions subject: ", M), -ACTION(I, V, D, X, Y), ground_subj_act(I, V, D, X, Y, M), gnd_actions()]
gnd_actions() / (ACTION(I, V, D, X, Y) & ADJ(I, X, M)) >> [show_line("\n", M, " as subject of: ", V), -ACTION(I, V, D, X, Y), -ADJ(I, X, M), ground_subj_act(I, V, D, X, Y, M), gnd_actions()]

# adjective has to be applied before
gnd_actions() / (ACTION(I, V, D, X, Y) & ADJ(I, Y, K) & GND(I, Y, M)) >> [show_line("\nact obj not ready to be grounded..."), mod_to_gnd(), gnd_actions()]
# prep is turned into a ground
gnd_actions() / (ACTION(I, V, D, X, Y) & PREP(I, Y, L, O) & no_dav(Y)) >> [show_line("\nact obj not ready to be grounded (prep)..."), prep_to_gnd(), gnd_actions()]
# applying grounds to actions object
gnd_actions() / (ACTION(I, V, D, X, Y) & GND(I, Y, M)) >> [show_line("\ngrounds to actions object: ", M), -ACTION(I, V, D, X, Y), ground_obj_act(I, V, D, X, Y, M), gnd_actions()]
gnd_actions() / (ACTION(I, V, D, X, Y) & ADJ(I, Y, M)) >> [show_line("\n", M, " as object of ", V), -ACTION(I, V, D, X, Y), -ADJ(I, Y, M), ground_obj_act(I, V, D, X, Y, M), gnd_actions()]
gnd_actions() >> [show_line("\ngrounding actions done.")]

# applying adverbs (if present) to actions label
apply_adv() / (ACTION(I, V, D, X, Y) & ADV(I, D, L)) >> [show_line("\napplying adverbs to actions label: ", L), -ACTION(I, V, D, X, Y), -ADV(I, D, L), adv_to_action(I, V, D, X, Y, L), apply_adv()]
apply_adv() / (ACTION(I, V, D, X, Y)) >> [show_line("\nadverbs application done.")]



# actions to clauses
actions_to_clauses() / (PRE_CROSS(I, D, K) & PREP(I, D, L, O)) >> [show_line("\nfeeding pre-cross: ", L), -PRE_CROSS(I, D, K), -PREP(I, D, L, O), feed_precross(I, D, K, L, O), actions_to_clauses()]
actions_to_clauses() / (ACTION(I, T, O, Y, Z) & ACTION(I, V, D, X, O) & PREP(I, O, L, K)) >> [show_line("\ncreating pre-cross: ", L),-ACTION(I, T, O, Y, Z), -PREP(I, O, L, K), create_precross(I, T, O, Y, Z, L, K), actions_to_clauses()]
actions_to_clauses() / (ACTION(I, V, D, X, O) & PRE_CROSS(I, O, K)) >> [show_line("\nmerging pre-cross: ", O), -ACTION(I, V, D, X, O), -PRE_CROSS(I, O, K), +ACTION(I, V, D, X, K), actions_to_clauses()]
actions_to_clauses() / (ACTION(I, T, O, Y, Z) & ACTION(I, V, D, X, O)) >> [show_line("\napplying action crossed dav: ", O), -ACTION(I, T, O, Y, Z), -ACTION(I, V, D, X, O), merge_act(I, T, Y, Z, V, D, X), actions_to_clauses()]
actions_to_clauses() / ACTION(I, V, D, X, Y) >> [show_line("\nturning action to clause: ", V), -ACTION(I, V, D, X, Y), act_to_clause(I, V, D, X, Y), actions_to_clauses()]
actions_to_clauses() >> [show_line("\nactions to clauses done. "), finalize_clause()]



# applying preps and finalization to clauses
finalize_clause() / (CLAUSE(I, D, X) & PREP(I, D, L, O)) >> [show_line("\napplying prep to clauses: ", L), -CLAUSE(I, D, X), -PREP(I, D, L, O), prep_to_clause(I, D, X, L, O), finalize_clause()]
finalize_clause() / CLAUSE(I, D, X) >> [show_line("\nfinalize clause..."), -CLAUSE(I, D, X), +CLAUSE(I, X), finalize_clause()]
finalize_clause() / (CLAUSE("LEFT", X) & CLAUSE("LEFT", Y) & neq(X, Y)) >> [show_line("\nleft conjunction..."), -CLAUSE("LEFT", X), -CLAUSE("LEFT", Y), conjunct_left_clauses(X, Y), finalize_clause()]
finalize_clause() / (LEFT_CLAUSE(X) & CLAUSE("LEFT", Y)) >> [show_line("\nleft conjunction..."), -LEFT_CLAUSE(X), -CLAUSE("LEFT", Y), conjunct_left_clauses(X, Y), finalize_clause()]

# remains management
finalize_gnd() / (GND(I, X, L) & CLAUSE(I, Y)) >> [show_line("\nretract unuseful grounds...", L), -GND(I, X, L), finalize_gnd()]
finalize_gnd() / (PREP(I, D, L, O) & CLAUSE(I, Y)) >> [show_line("\nretract unuseful preps...", L), -PREP(I, D, L, O), finalize_gnd()]
finalize_gnd() / REMAIN(I, K) >> [show_line("\nturning remain in half clause..."), -REMAIN(I, K), +CLAUSE(I, K), finalize_gnd()]
finalize_gnd() / GND(I, X, L) >> [show_line("\ncreating remain...", L), -GND(I, X, L), create_remain(I, X, L), finalize_gnd()]
finalize_gnd() >> [show_line("\nremains finalization done.")]


# creating merged definite clauses driven by subj-obj
process_clause() / (CLAUSE(I, X) & CLAUSE(I, Y) & neq(X, Y) & ACT_CROSS_VAR(I, Z, V)) >> [show_line("\njoining clauses with...", Z, " and ", V), -CLAUSE(I, X), -CLAUSE(I, Y), -ACT_CROSS_VAR(I, Z, V), join_clauses(X, Y, V, Z), process_clause()]


# creating definite clauses with common left hand-side
process_clause() / (CLAUSE("RIGHT", X) & LEFT_CLAUSE(Y)) >> [show_line("\ncreating multiple definite clause..."), -CLAUSE("RIGHT", X), join_hand_sides(Y, X), process_clause()]

# create normal definite clauses
process_clause() / (CLAUSE("RIGHT", X) & CLAUSE("LEFT", Y)) >> [show_line("\ncreating normal definite clause..."), -CLAUSE("RIGHT", X), join_hand_sides(Y, X), process_clause()]
process_clause() / CLAUSE("FLAT", X) >> [show_line("\nGot R definite clause.\n"), -CLAUSE("FLAT", X), +DEF_CLAUSE(X), process_clause()]

process_clause() / (DEF_CLAUSE(X) & LEFT_CLAUSE(Y)) >> [show_line("\nProcessing definite clause WITH LEFT..."), -LEFT_CLAUSE(Y), process_clause()]
process_clause() / (DEF_CLAUSE(X) & CLAUSE("LEFT", Y)) >> [show_line("\nProcessing definite definite clause WITH CLAUSE LEFT..."), -CLAUSE("LEFT", Y), process_clause()]
process_clause() / CLAUSE("LEFT", Y) >> [show_line("\nRetracting unuseful LEFT clause...", Y), -CLAUSE("LEFT", Y), process_clause()]

process_clause() / (DEF_CLAUSE(X) & REASON("ON") & IS_RULE(Y)) >> [show_line("\nReasoning...............\n"), -DEF_CLAUSE(X), -LISTEN('ON'), -IS_RULE(Y), reason(X), process_clause()]
process_clause() / (DEF_CLAUSE(X) & REASON("ON")) >> [show_line("\nReasoning...............\n"), -DEF_CLAUSE(X), -LISTEN('ON'), reason(X), process_clause()]

process_clause() / (DEF_CLAUSE(X) & LISTEN("ON") & RETRACT("ON")) >> [show_line("\nRetracting clause."), -DEF_CLAUSE(X), -RETRACT("ON"), retract_clause(X), process_clause()]
process_clause() / (DEF_CLAUSE(X) & LISTEN("ON")) >> [show_line("\nAdding definite clause into Fol Kb."), -DEF_CLAUSE(X), new_clause(X), process_clause()]
