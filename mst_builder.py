from phidias.Lib import *
from actions import *



# MST components creations

# noun subjects
parse_deps() / DEP("nsubj", X, Y) >> [show_line("\nprocessing nsubj: ", X), -DEP("nsubj", X, Y), create_MST_ACT(X, Y), parse_deps()]
# noun subjects passive
parse_deps() / DEP("nsubjpass", X, Y) >> [show_line("\nprocessing nsubjpass: ", X), -DEP("nsubjpass", X, Y), create_MST_ACT_PASS(X, Y), parse_deps()]

# particles
parse_deps() / (MST_ACT(X, D, Y, Z) & DEP("prt", X, K)) >> [show_line("\nprocessing prt: ", Y), -DEP("prt", X, K), +MST_VAR(D, K), parse_deps()]

# expletive existentials (there) in the subject position.
parse_deps() / DEP("expl", X, Y) >> [show_line("\nprocessing expl..."), -DEP("expl", X, Y), create_MST_ACT_EX(X), parse_deps()]

# open clausal complements or adverbial clause modifiers
parse_deps() / (MST_ACT(X, D, Y, Z) & DEP("xcomp", T, K)) >> [show_line("\nprocessing xcomp...", T), +MST_ACT(K, D, Y, Z), -DEP("xcomp", T, K), parse_deps()]

# attribute or adjectival complements
parse_deps() / (MST_ACT(X, D, Y, Z) & MST_VAR(Z, "?") & DEP("attr", X, K)) >> [show_line("\nprocessing attr obj..."), -DEP("attr", X, K), -MST_VAR(Z, "?"), +MST_VAR(Z, K), parse_deps()]
parse_deps() / (MST_ACT(X, D, Y, Z) & MST_VAR(Y, "?") & DEP("attr", X, K)) >> [show_line("\nprocessing attr subj..."), -DEP("attr", X, K), -MST_VAR(Z, "?"), +MST_VAR(Z, K), parse_deps()]
parse_deps() / (MST_ACT(X, D, Y, Z) & MST_VAR(Z, "?") & DEP("acomp", X, K)) >> [show_line("\nprocessing acomp..."), -DEP("acomp", X, K), -MST_VAR(Z, "?"), +MST_VAR(Z, K), parse_deps()]

# direct objects
parse_deps() / (MST_ACT(X, D, Y, Z) & MST_VAR(Z, "?") & DEP("dobj", X, K)) >> [show_line("\nprocessing dobj..."), -DEP("dobj", X, K), -MST_VAR(Z, "?"), +MST_VAR(Z, K), parse_deps()]
parse_deps() / (MST_ACT(X, D, Y, Z) & DEP("dobj", X, K)) >> [show_line("\nprocessing dobj as adv..."), -DEP("dobj", X, K), +MST_VAR(D, K), parse_deps()]


# object predicates
parse_deps() / (MST_ACT(V, D, S, O) & MST_VAR(O, "?") & DEP("oprd", V, K)) >> [show_line("\nprocessing oprd var..."), -DEP("oprd", V, K), -MST_VAR(O, "?"), +MST_VAR(O, K), parse_deps()]
parse_deps() / (MST_VAR(V, X) & DEP("oprd", X, Y)) >> [show_line("\nprocessing oprd bind..."), -DEP("oprd", X, Y), +MST_BIND(X, Y), parse_deps()]
parse_deps() / (MST_ACT(V, D, S, O) & MST_VAR(O, U) & DEP("oprd", V, K)) >> [show_line("\nprocessing oprd bind passive..."), -DEP("oprd", V, K), +MST_BIND(U, K), parse_deps()]


parse_deps() / (MST_ACT(X, D, Y, Z) & DEP("dative", X, K)) >> [show_line("\nprocessing dative..."), -DEP("dative", X, K), create_MST_PREP(D, K), parse_deps()]
parse_deps() / (MST_ACT(X, D, Y, Z) & DEP("prep", X, K)) >> [show_line("\nprocessing action prep..."), -DEP("prep", X, K), create_MST_PREP(D, K), parse_deps()]

# compound modifiers
parse_deps() / (MST_VAR(V, X) & DEP("compound", X, Y)) >> [show_line("\nprocessing compound..."), -DEP("compound", X, Y), +MST_COMP(X, Y), parse_deps()]

# adjectival/possession/number/noun phrase as adverbial/appositional/quantifier modifiers
parse_deps() / DEP("amod", X, Y) >> [show_line("\nprocessing amod..."), -DEP("amod", X, Y), +MST_BIND(X, Y), parse_deps()]
parse_deps() / (MST_BIND(V, X) & DEP("amod", X, Y)) >> [show_line("\nprocessing bind related amod..."), -DEP("amod", X, Y), +MST_BIND(V, Y), parse_deps()]

parse_deps() / DEP("poss", X, Y) >> [show_line("\nprocessing poss..."), -DEP("poss", X, Y), +MST_BIND(X, Y), parse_deps()]
parse_deps() / (MST_BIND(V, X) & DEP("poss", X, Y)) >> [show_line("\nprocessing bind related poss..."), -DEP("poss", X, Y), +MST_BIND(V, Y), parse_deps()]

parse_deps() / DEP("nummod", X, Y) >> [show_line("\nprocessing nummod..."), -DEP("nummod", X, Y), +MST_BIND(X, Y), parse_deps()]
parse_deps() / (MST_BIND(V, X) & DEP("nummod", X, Y)) >> [show_line("\nprocessing bind related nummod..."), -DEP("nummod", X, Y), +MST_BIND(V, Y), parse_deps()]

parse_deps() / DEP("nmod", X, Y) >> [show_line("\nprocessing nmod..."), -DEP("nmod", X, Y), +MST_BIND(X, Y), parse_deps()]
parse_deps() / (MST_BIND(V, X) & DEP("nmod", X, Y)) >> [show_line("\nprocessing bind related nmod..."), -DEP("nmod", X, Y), +MST_BIND(V, Y), parse_deps()]

parse_deps() / DEP("appos", X, Y) >> [show_line("\nprocessing appos..."), -DEP("appos", X, Y), +MST_BIND(X, Y), parse_deps()]
parse_deps() / (MST_BIND(V, X) & DEP("appos", X, Y)) >> [show_line("\nprocessing bind related appos..."), -DEP("appos", X, Y), +MST_BIND(V, Y), parse_deps()]

parse_deps() / DEP("quantmod", X, Y) >> [show_line("\nprocessing quantmod..."), -DEP("quantmod", X, Y), +MST_BIND(X, Y), parse_deps()]
parse_deps() / (MST_BIND(V, X) & DEP("quantmod", X, Y)) >> [show_line("\nprocessing bind related quantmod..."), -DEP("quantmod", X, Y), +MST_BIND(V, Y), parse_deps()]


# prepositional modifiers
parse_deps() / (MST_VAR(V, X) & MST_BIND(X, Y) & DEP("prep", Y, K)) >> [show_line("\nprocessing bind prep..."), -DEP("prep", Y, K), create_MST_PREP(V, K), parse_deps()]
parse_deps() / (MST_VAR(V, X) & DEP("prep", X, K)) >> [show_line("\nprocessing prep..."), -DEP("prep", X, K), create_MST_PREP(V, K), parse_deps()]

# object/complement of prepositions
parse_deps() / (MST_PREP(X, Y, Z) & DEP("pobj", X, O) & MST_VAR(Z, "?")) >> [show_line("\nprocessing pobj..."), -MST_VAR(Z, "?"), -DEP("pobj", X, O), +MST_VAR(Z, O), parse_deps()]
parse_deps() / (MST_PREP(X, Y, Z) & DEP("pcomp", X, O) & MST_VAR(Z, "?")) >> [show_line("\nprocessing pcomp..."), -MST_VAR(Z, "?"), -DEP("pcomp", X, O), +MST_VAR(Z, O), parse_deps()]

# adverbial modifiers or noun phrase as adverbial modifiers/markers/negations
parse_deps() / (MST_ACT(X, D, Y, Z) & DEP("advmod", X, K) & COND_WORD(K)) >> [show_line("\nprocessing CONDS +",D), -DEP("advmod", X, K), +MST_COND(D), parse_deps()]
parse_deps() / (MST_ACT(X, D, Y, Z) & DEP("advmod", X, K)) >> [show_line("\nprocessing advmod..."), -DEP("advmod", X, K), +MST_VAR(D, K), parse_deps()]
parse_deps() / (MST_ACT(V, D, S, O) & MST_PREP(X, D, Y) & DEP("advmod", X, K)) >> [show_line("\nprocessing advmod prep..."), -DEP("advmod", X, K), +MST_VAR(D, K), parse_deps()]

parse_deps() / (MST_ACT(X, D, Y, Z) & DEP("npadvmod", X, K)) >> [show_line("\nprocessing npadvmod..."), -DEP("npadvmod", X, K), +MST_VAR(D, K), parse_deps()]
parse_deps() / (MST_ACT(X, D, Y, Z) & DEP("neg", X, K)) >> [show_line("\nprocessing neg..."), -DEP("neg", X, K), +MST_VAR(D, K), parse_deps()]
parse_deps() / (MST_ACT(X, D, Y, Z) & DEP("mark", X, K) & NBW(K)) >> [show_line("\nprocessing mark...", K), -DEP("mark", X, K), +MST_COND(D), parse_deps()]

# agents
parse_deps() / (MST_ACT(X, D, Y, Z) & MST_VAR(Y, "?") & DEP("agent", X, K) & DEP("pobj", K, O)) >> [show_line("\nprocessing agent..."), -MST_VAR(Y, "?"), -DEP("agent", X, K), -DEP("pobj", K, O), +MST_VAR(Y, O), parse_deps()]

# clausal subjects
parse_deps() / (MST_ACT(V, D, S, O) & DEP("csubj", U, V)) >> [show_line("\nprocessing csubj..."), -DEP("csubj", U, V), create_MST_ACT_SUBJ(U, D), parse_deps()]

# clausal complements
parse_deps() / (MST_ACT(X, D, Y, Z) & MST_ACT(T, E, W, K) & DEP("ccomp", X, T)) >> [show_line("\nprocessing ccomp..."), -DEP("ccomp", X, T), -MST_ACT(X, D, Y, Z), +MST_ACT(X, D, Y, E), parse_deps()]
parse_deps() / (MST_ACT(V, E, W, K) & MST_VAR(K, Y) & DEP("ccomp", X, T)) >> [show_line("\nprocessing ccomp combined..."), -DEP("ccomp", X, T), create_MST_ACT_SUBJ(T, K), parse_deps()]
parse_deps() / (DEP("ccomp", X, Y)) >> [show_line("\nprocessing ccomp as nsubj..."), -DEP("ccomp", X, Y), create_MST_ACT(X, Y), parse_deps()]

# relative clause modifiers
parse_deps() / (MST_ACT(T, D, U, X) & MST_VAR(X, K) & MST_ACT(V, E, S, O) & MST_ACT(W, J, O, M) & DEP("relcl", K, V)) >> [show_line("\nprocessing relcl connecting 3 actions objects..."), -DEP("relcl", K, V), -MST_ACT(V, E, S, O), +MST_ACT(V, E, S, X), -MST_ACT(W, J, O, M), +MST_ACT(W, J, X, M), parse_deps()]
parse_deps() / (MST_ACT(X, D, Y, Z) & MST_VAR(W, K) & DEP("relcl", K, X) & Past_Part(X)) >> [show_line("\nprocessing relcl pp..."), -DEP("relcl", K, X), -MST_ACT(X, D, Y, Z), +MST_ACT(X, D, Y, W), parse_deps()]
parse_deps() / (MST_ACT(X, D, Y, Z) & MST_VAR(W, K) & MST_VAR(Z, U) & DEP("relcl", K, X) & Wh_Det(U)) >> [show_line("\nprocessing relcl wh..."), -DEP("relcl", K, X), -MST_ACT(X, D, Y, Z), +MST_ACT(X, D, Y, W), parse_deps()]
parse_deps() / (MST_ACT(X, D, Y, Z) & MST_VAR(W, K) & DEP("relcl", K, X)) >> [show_line("\nprocessing relcl..."), -DEP("relcl", K, X), -MST_ACT(X, D, Y, Z), +MST_ACT(X, D, W, Z), parse_deps()]
parse_deps() / (DEP("relcl", X, Y) & MST_VAR(W, X) & MST_ACT(T, D, U, W)) >> [show_line("\nprocessing relcl as nsubj..."), -DEP("relcl", X, Y), create_MST_ACT_SUBJ(Y, W), parse_deps()]




# clausal modifiers of noun
parse_deps() / (MST_ACT(V, D, X, Y) & MST_VAR(Y, K) & DEP("acl", K, U)) >> [show_line("\nprocessing acl as nsubj var pass..."), -DEP("acl", K, U), create_MST_ACT_SUBJ(U, Y), parse_deps()]
parse_deps() / (MST_ACT(V, D, X, Y) & MST_VAR(X, K) & DEP("acl", K, U)) >> [show_line("\nprocessing acl as nsubj var..."), -DEP("acl", K, U), create_MST_ACT_SUBJ(U, X), parse_deps()]
parse_deps() / DEP("acl", K, U) >> [show_line("\nprocessing acl as nsubj..."), -DEP("acl", K, U), create_MST_ACT(U, K), parse_deps()]


parse_deps() / (MST_ACT(V, D, S, O) & DEP("conj", V, U)) >> [show_line("\nprocessing action related conj.."), -DEP("conj", V, U), +MST_BIND(V, U), parse_deps()]
parse_deps() / (MST_ACT(V, E, X, Y) & MST_ACT(U, D, S, O) & MST_COND(E) & MST_BIND(V, U)) >> [show_line("\nupdating CONDS +", D), -MST_BIND(V, U), +MST_COND(D), parse_deps()]
parse_deps() / (MST_ACT(V, D, S, O) & MST_ACT(U, E, X, Y) & MST_BIND(V, U)) >> [show_line("\ndeleting needless bind: ", U), -MST_BIND(V, U), parse_deps()]
parse_deps() / (MST_ACT(V, D, S, O) & MST_BIND(V, U)) >> [show_line("\ngenerating new action from bind: ", U), -MST_BIND(V, U), create_MST_ACT_SUBJ(U, S), parse_deps()]

parse_deps() / (MST_BIND(V, U) & DEP("conj", U, K)) >> [show_line("\nprocessing var related conj..."), -DEP("conj", U, K), +MST_BIND(V, K), parse_deps()]
parse_deps() / (MST_VAR(V, X) & DEP("conj", X, Y)) >> [show_line("\nprocessing var related conj.."), -DEP("conj", X, Y), +MST_BIND(X, Y), parse_deps()]

# parataxis
parse_deps() / (MST_ACT(V, D, S, O) & MST_ACT(U, E, X, Y) & DEP("parataxis", V, U)) >> [show_line("\nprocessing parataxis..."), -DEP("parataxis", V, U), -MST_ACT(U, E, X, Y), +MST_ACT(U, E, X, D), parse_deps()]


# imperatives
parse_deps() / DEP("dobj", X, Y) >> [show_line("\nprocessing imperative dobj: ", X), -DEP("dobj", X, Y), create_IMP_MST_ACT(X, Y), parse_deps()]


# linking together composite verbal actions
parse_deps() / (MST_ACT(X, D, Y, Z) & MST_ACT(T, D, Y, Z) & neq(X, T)) >> [show_line("\nconcat composite verbals..."), -MST_ACT(X, D, Y, Z), -MST_ACT(T, D, Y, Z), concat_mst_verbs(X, T, D, Y, Z), parse_deps()]

parse_deps() / (MST_PREP(X, Y, Z) & MST_VAR(Z, '?')) >> [show_line("\nchanging unactive prep in adv..."), -MST_PREP(X, Y, Z), -MST_VAR(Z, '?'), +MST_VAR(Y, X), parse_deps()]

parse_deps() / DEP("ROOT", X, X) >> [show_line("\nremoving ROOT..."), -DEP("ROOT", X, X), parse_deps()]
parse_deps() / DEP(Z, X, Y) >> [show_line("\nremoving ", Z), -DEP(Z, X, Y), parse_deps()]


# Feeding parser's MST components section
feed_mst() / MST_ACT(X, Y, Z, T) >> [show_line("\nfeeding MST with an action..."), -MST_ACT(X, Y, Z, T), feed_mst_actions_parser(X, Y, Z, T), feed_mst()]
feed_mst() / MST_VAR(X, Y) >> [show_line("\nfeeding MST with a var..."), -MST_VAR(X, Y), feed_mst_vars_parser(X, Y), feed_mst()]
feed_mst() / MST_BIND(X, Y) >> [show_line("\nfeeding MST with a bind..."), -MST_BIND(X, Y), feed_mst_binds_parser(X, Y), feed_mst()]
feed_mst() / MST_PREP(X, Y, Z) >> [show_line("\nfeeding MST with a prep..."), -MST_PREP(X, Y, Z), feed_mst_preps_parser(X, Y, Z), feed_mst()]
feed_mst() / MST_COMP(X, Y) >> [show_line("\nfeeding MST a comp..."), -MST_COMP(X, Y), feed_mst_comps_parser(X, Y), feed_mst()]
feed_mst() / MST_COND(X) >> [show_line("\nfeeding MST with a cond..."), -MST_COND(X), feed_mst_conds_parser(X), feed_mst()]




