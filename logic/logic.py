

from utils import (
    first, issequence, Expr, expr, subexpressions
)

import itertools
import copy
import configparser

# ______________________________________________________________________________


class KB:

    """A knowledge base to which you can tell and ask sentences.
    To create a KB, first subclass this class and implement
    tell, ask_generator, and retract.  Why ask_generator instead of ask?
    The book is a bit vague on what ask means --
    For a Propositional Logic KB, ask(P & Q) returns True or False, but for an
    FOL KB, something like ask(Brother(x, y)) might return many substitutions
    such as {x: Cain, y: Abel}, {x: Abel, y: Cain}, {x: George, y: Jeb}, etc.
    So ask_generator generates these one at a time, and ask either returns the
    first one or returns False."""

    def __init__(self, exec_occur_check):
        self.exec_occurr_check = exec_occur_check


    def __init__(self, sentence=None):
        raise NotImplementedError

    def tell(self, sentence):
        """Add the sentence to the KB."""
        raise NotImplementedError

    def ask(self, query):
        """Return a substitution that makes the query true, or, failing that, return False."""
        return first(self.ask_generator(query), default=False)

    def ask_generator(self, query):
        """Yield all the substitutions that make query true."""
        raise NotImplementedError

    def retract(self, sentence):
        """Remove sentence from the KB."""
        raise NotImplementedError



def KB_AgentProgram(KB):
    """A generic logical knowledge-based agent program. [Figure 7.1]"""
    steps = itertools.count()

    def program(percept):
        t = next(steps)
        KB.tell(make_percept_sentence(percept, t))
        action = KB.ask(make_action_query(t))
        KB.tell(make_action_sentence(action, t))
        return action

    def make_percept_sentence(percept, t):
        return Expr("Percept")(percept, t)

    def make_action_query(t):
        return expr("ShouldDo(action, {})".format(t))

    def make_action_sentence(action, t):
        return Expr("Did")(action[expr('action')], t)

    return program


def is_symbol(s):
    """A string s is a symbol if it starts with an alphabetic char.
    >>> is_symbol('R2D2')
    True
    """
    return isinstance(s, str) and s[:1].isalpha()


def is_var_symbol(s):
    """A logic variable symbol is an initial-lowercase string.
    >>> is_var_symbol('EXE')
    False
    """
    return is_symbol(s) and s[0].islower()


def is_prop_symbol(s):
    """A proposition logic symbol is an initial-uppercase string.
    >>> is_prop_symbol('exe')
    False
    """
    return is_symbol(s) and s[0].isupper()


def variables(s):
    """Return a set of the variables in expression s.
    >>> variables(expr('F(x, x) & G(x, y) & H(y, z) & R(A, z, 2)')) == {x, y, z}
    True
    """
    return {x for x in subexpressions(s) if is_variable(x)}


def is_definite_clause(s):
    """Returns True for exprs s of the form A & B & ... & C ==> D,
    where all literals are positive.  In clause form, this is
    ~A | ~B | ... | ~C | D, where exactly one clause is positive.
    >>> is_definite_clause(expr('Farmer(Mac)'))
    True
    """
    if is_symbol(s.op):
        return True
    elif s.op == '==>':
        antecedent, consequent = s.args
        return (is_symbol(consequent.op) and
                all(is_symbol(arg.op) for arg in conjuncts(antecedent)))
    else:
        return False


def parse_definite_clause(s):
    """Return the antecedents and the consequent of a definite clause."""
    assert is_definite_clause(s)
    if is_symbol(s.op):
        return [], s
    else:
        antecedent, consequent = s.args
        return conjuncts(antecedent), consequent




def dissociate(op, args):
    """Given an associative op, return a flattened list result such
    that Expr(op, *result) means the same as Expr(op, *args).
    >>> dissociate('&', [A & B])
    [A, B]
    """
    result = []

    def collect(subargs):
        for arg in subargs:
            if arg.op == op:
                collect(arg.args)
            else:
                result.append(arg)
    collect(args)
    return result


def conjuncts(s):
    """Return a list of the conjuncts in the sentence s.
    >>> conjuncts(A & B)
    [A, B]
    >>> conjuncts(A | B)
    [(A | B)]
    """
    return dissociate('&', [s])





def unify(x, y, s={}):
    """Unify expressions x,y with substitution s; return a substitution that
    would make x,y equal, or None if x,y can not unify. x and y can be
    variables (e.g. Expr('x')), constants, lists, or Exprs. [Figure 9.1]
    >>> unify(x, 3, {})
    {x: 3}
    """
    if s is None:
        return None
    elif x == y:
        return s
    elif is_variable(x):
        return unify_var(x, y, s)
    elif is_variable(y):
        return unify_var(y, x, s)
    elif isinstance(x, Expr) and isinstance(y, Expr):
        return unify(x.args, y.args, unify(x.op, y.op, s))
    elif isinstance(x, str) or isinstance(y, str):
        return None
    elif issequence(x) and issequence(y) and len(x) == len(y):
        if not x:
            return s
        return unify(x[1:], y[1:], unify(x[0], y[0], s))
    else:
        return None


def is_variable(x):
    """A variable is an Expr with no args and a lowercase symbol as the op."""
    return isinstance(x, Expr) and not x.args and x.op[0].islower()


def unify_var(var, x, s):
    if var in s:
        return unify(s[var], x, s)
    elif x in s:
        return unify(var, s[x], s)
    elif exec_occur_check and occur_check(var, x, s):
        return None
    else:
        return extend(s, var, x)


def occur_check(var, x, s):
    """Return true if variable var occurs anywhere in x
    (or in subst(s, x), if s has a binding for x)."""
    if var == x:
        return True
    elif is_variable(x) and x in s:
        return occur_check(var, s[x], s)
    elif isinstance(x, Expr):
        return (occur_check(var, x.op, s) or
                occur_check(var, x.args, s))
    elif isinstance(x, (list, tuple)):
        return first(e for e in x if occur_check(var, e, s))
    else:
        return False


def extend(s, var, val):
    """Copy the substitution s and extend it by setting var to val; return copy.
    >>> extend({x: 1}, y, 2) == {x: 1, y: 2}
    True
    """
    s2 = s.copy()
    s2[var] = val
    return s2


def subst(s, x):
    """Substitute the substitution s into the expression x.
    >>> subst({x: 42, y:0}, F(x) + y)
    (F(42) + 0)
    """
    if isinstance(x, list):
        return [subst(s, xi) for xi in x]
    elif isinstance(x, tuple):
        return tuple([subst(s, xi) for xi in x])
    elif not isinstance(x, Expr):
        return x
    elif is_var_symbol(x.op):
        return s.get(x, x)
    else:
        return Expr(x.op, *[subst(s, arg) for arg in x.args])


def standardize_variables(sentence, dic=None):
    """Replace all the variables in sentence with new variables."""
    if dic is None:
        dic = {}
    if not isinstance(sentence, Expr):
        return sentence
    elif is_var_symbol(sentence.op):
        if sentence in dic:
            return dic[sentence]
        else:
            v = Expr('v_{}'.format(next(standardize_variables.counter)))
            dic[sentence] = v
            return v
    else:
        return Expr(sentence.op,
                    *[standardize_variables(a, dic) for a in sentence.args])


standardize_variables.counter = itertools.count()

config = configparser.ConfigParser()
config.read('config.ini')
exec_occur_check = config.getboolean('REASONING', 'OCCUR_CHECK')

# ______________________________________________________________________________


class FolKB(KB):

    def __init__(self, initial_clauses=None):
        self.clauses = []  # inefficient: no indexing
        if initial_clauses:
            for clause in initial_clauses:
                self.tell(clause)

    def tell(self, sentence):
        if is_definite_clause(sentence):
            self.clauses.append(sentence)
        else:
            raise Exception("Not a definite clause: {}".format(sentence))

    def ask_generator(self, query):
        return fol_bc_ask(self, query)

    def retract(self, sentence):
        self.clauses.remove(sentence)

    def fetch_rules_for_goal(self, goal):
        return self.clauses

    def fetch_rules(self):
        return self.clauses

    def produce_clauses(self, clause, derived):
        return produce_clauses_inner(self, clause, derived)

    def nested_ask(self, goal, candidates):
        return nested_ask_inner(self, goal, candidates)

    def nested_tell(self, clause):
        return nested_tell_inner(self, clause)


def nested_tell_inner(KB, clause):
    """ Assert a clause and, when lhs(clause) is not null, also a set of implications where lhs is clause
        and rhs a derived clause pruducted by produce_clauses accordingly to a specific knowledge base."""
    if str(clause).find("==>") == -1:
        derived = []
        KB.produce_clauses(clause, derived)
        for derived_clause in derived:
            if unify(clause, derived_clause) is None:
                new_clause = str(clause) + " ==> " + str(derived_clause)
                KB.tell(expr(new_clause))
    KB.tell(clause)


def expr_to_string(e):
    str = ""
    for i in range(len(e)):
        if i == 0:
            str = e[i]
        else:
            str = str + ", " + e[i]
    return str


def produce_clauses_inner(KB, clause, derived):
    """ Produces a set of single positive literals derived from an initial clause,
    accordingly to a specific knowledge base."""
    for kb_clause in KB.clauses:
        lhs, rhs = parse_definite_clause(kb_clause)
        args_list = list(clause.args)
        args_list_std = list(clause.args)
        for n, arg in enumerate(args_list):
            lhs_str = expr_to_string(lhs)
            if unify(lhs_str, arg) is not None:
                args_list_std[n] = standardize_variables(rhs)
                new_clause_std = copy.deepcopy(clause)
                new_clause_std.args = tuple(args_list_std)
                CLAUSE_UNIFIED = False

                for der in derived:
                    if unify(der, new_clause_std) is not None:
                        CLAUSE_UNIFIED = True
                        break
                if CLAUSE_UNIFIED is False:
                    derived.append(new_clause_std)
                    produce_clauses_inner(KB, new_clause_std, derived)





def nested_ask_inner(KB, goal, candidates):
    """Checks if a single positive literal taken as query can be considered true 
    accordingly to the clauses contained in a knowledge base also 
    taking in account all the possible candidates that can be derived from
    the original query through unifications and substitutions."""
    for clause in KB.clauses:
        lhs, rhs = parse_definite_clause(clause)
        args_list = list(goal.args)
        for n, arg in enumerate(args_list):
            lhs_str = expr_to_string(lhs)
            if unify(lhs_str, arg) is not None:
                args_list[n] = standardize_variables(rhs)
                new_candidate = copy.deepcopy(goal)
                new_candidate.args = tuple(args_list)
                CANDIDATE_UNIFIED = False

                for cand in candidates:
                    if unify(cand, new_candidate) is not None:
                        CANDIDATE_UNIFIED = True
                        break

                if CANDIDATE_UNIFIED is False:
                    candidates.append(new_candidate)
                    result = KB.ask(new_candidate)
                    if (result != False):
                        return str(result)
                    else:
                        return nested_ask_inner(KB, new_candidate, candidates)
    return False




def fol_bc_ask(KB, query):
    return fol_bc_or(KB, query, {})


def fol_bc_or(KB, goal, theta):
    for rule in KB.fetch_rules_for_goal(goal):
        lhs, rhs = parse_definite_clause(standardize_variables(rule))
        for theta1 in fol_bc_and(KB, lhs, unify(rhs, goal, theta)):
            yield theta1


def fol_bc_and(KB, goals, theta):
    if theta is None:
        pass
    elif not goals:
        yield theta
    else:
        first, rest = goals[0], goals[1:]
        for theta1 in fol_bc_or(KB, subst(theta, first), theta):
            for theta2 in fol_bc_and(KB, rest, theta1):
                yield theta2







