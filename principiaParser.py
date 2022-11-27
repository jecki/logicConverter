#!/usr/bin/env python3

#######################################################################
#
# SYMBOLS SECTION - Can be edited. Changes will be preserved.
#
#######################################################################


import collections
import copy
from functools import partial, reduce
import os
import sys
from typing import Tuple, List, Union, Any, Optional, Callable, cast

try:
    scriptpath = os.path.dirname(__file__)
except NameError:
    scriptpath = ''
if scriptpath and scriptpath not in sys.path:
    sys.path.append(scriptpath)

try:
    import regex as re
except ImportError:
    import re
from DHParser import start_logging, suspend_logging, resume_logging, is_filename, load_if_file, \
    Grammar, Compiler, nil_preprocessor, PreprocessorToken, Whitespace, Drop, AnyChar, Parser, \
    Lookbehind, Lookahead, Alternative, Pop, Text, Synonym, Counted, Interleave, INFINITE, ERR, \
    Option, NegativeLookbehind, OneOrMore, RegExp, Retrieve, Series, Capture, TreeReduction, \
    ZeroOrMore, Forward, NegativeLookahead, Required, CombinedParser, Custom, mixin_comment, \
    compile_source, grammar_changed, last_value, matching_bracket, PreprocessorFunc, is_empty, \
    remove_if, Node, TransformationDict, TransformerCallable, transformation_factory, traverse, \
    remove_children_if, move_fringes, normalize_whitespace, is_anonymous, name_matches, \
    reduce_single_child, replace_by_single_child, replace_or_reduce, remove_whitespace, \
    replace_by_children, remove_empty, remove_tokens, flatten, all_of, any_of, \
    merge_adjacent, collapse, collapse_children_if, transform_result, WHITESPACE_PTYPE, \
    TOKEN_PTYPE, remove_children, remove_content, remove_brackets, change_name, \
    remove_anonymous_tokens, keep_children, is_one_of, not_one_of, content_matches, apply_if, peek, \
    remove_anonymous_empty, keep_nodes, traverse_locally, strip, lstrip, rstrip, \
    replace_content_with, forbid, assert_content, remove_infix_operator, \
    add_error, error_on, recompile_grammar, left_associative, lean_left, set_config_value, \
    get_config_value, node_maker, access_thread_locals, access_presets, PreprocessorResult, \
    finalize_presets, ErrorCode, RX_NEVER_MATCH, set_tracer, resume_notices_on, \
    trace_history, has_descendant, neg, has_ancestor, optional_last_value, insert, \
    positions_of, replace_child_names, add_attributes, delimit_children, merge_connected, \
    has_attr, has_parent, ThreadLocalSingletonFactory, Error, canonical_error_strings, \
    has_errors, ERROR, FATAL, set_preset_value, get_preset_value, NEVER_MATCH_PATTERN, \
    gen_find_include_func, preprocess_includes, make_preprocessor, chain_preprocessors, \
    RootNode, Path, expand_table, pick_from_path


#######################################################################
#
# PREPROCESSOR SECTION - Can be edited. Changes will be preserved.
#
#######################################################################



RE_INCLUDE = NEVER_MATCH_PATTERN
# To capture includes, replace the NEVER_MATCH_PATTERN 
# by a pattern with group "name" here, e.g. r'\input{(?P<name>.*)}'


def principiaTokenizer(original_text) -> Tuple[str, List[Error]]:
    # Here, a function body can be filled in that adds preprocessor tokens
    # to the source code and returns the modified source.
    return original_text, []


def preprocessor_factory() -> PreprocessorFunc:
    # below, the second parameter must always be the same as principiaGrammar.COMMENT__!
    find_next_include = gen_find_include_func(RE_INCLUDE, ';.*?(?:\\n|$)')
    include_prep = partial(preprocess_includes, find_next_include=find_next_include)
    tokenizing_prep = make_preprocessor(principiaTokenizer)
    return chain_preprocessors(include_prep, tokenizing_prep)


get_preprocessor = ThreadLocalSingletonFactory(preprocessor_factory)


def preprocess_principia(source):
    return get_preprocessor()(source)


#######################################################################
#
# PARSER SECTION - Don't edit! CHANGES WILL BE OVERWRITTEN!
#
#######################################################################

class principiaGrammar(Grammar):
    r"""Parser for a principia source file.
    """
    formula = Forward()
    formula0 = Forward()
    formula1 = Forward()
    formula2 = Forward()
    formula3 = Forward()
    source_hash__ = "1182b2b0eeaa380627c496572098c505"
    disposable__ = re.compile('_EOF$|_cdot$|_element$|_affirmation$|_dots$|_assertion_sign$|_nat_number$|_not$|_lB$|_rB$|_exists_sign$|_individual$|_assertion$')
    static_analysis_pending__ = []  # type: List[bool]
    parser_initialization__ = ["upon instantiation"]
    COMMENT__ = r';.*?(?:\n|$)'
    comment_rx__ = re.compile(COMMENT__)
    WHITESPACE__ = r'[ \t]*(?:\n[ \t]*)?(?!\n)'
    WSP_RE__ = mixin_comment(whitespace=WHITESPACE__, comment=COMMENT__)
    wsp__ = Whitespace(WSP_RE__)
    dwsp__ = Drop(Whitespace(WSP_RE__))
    _EOF = Drop(NegativeLookahead(RegExp('.')))
    _reverse_logical_connector = RegExp('[⊢∨⊃≡=]|-[|]|>-|<->')
    _logical_connector = RegExp('[⊢∨⊃≡=]|[|]-|->|<->')
    _rB = Drop(Text(")"))
    _lB = Drop(Text("("))
    _a4 = Series(Text("::"), NegativeLookahead(_logical_connector))
    _a3 = Series(Alternative(Text(".:"), Text(":.")), NegativeLookahead(_logical_connector))
    _a2 = Series(Text(":"), NegativeLookahead(_logical_connector))
    _a1 = Series(Text("."), NegativeLookahead(_logical_connector))
    _and = Alternative(_a4, _a3, _a2, _a1)
    _not = Drop(Alternative(Text("∼"), Text("~")))
    _assertion_sign = Drop(Alternative(Text("⊢"), Text("|-")))
    _unique_sign = Text("E")
    _exists_sign = Drop(Alternative(Text("∃"), Text("€")))
    _nat_number = RegExp('[1-9]\\d*')
    _cdot = Drop(Alternative(RegExp('[·⋅]'), Drop(Series(Text("."), Drop(Lookahead(_nat_number))))))
    _d4 = Alternative(Series(Text("::"), Lookahead(_logical_connector)), Series(Lookbehind(_reverse_logical_connector), Text("::")))
    _d3 = Alternative(Series(Alternative(Text(":."), Text(".:")), Lookahead(_logical_connector)), Series(Lookbehind(_reverse_logical_connector), Alternative(Text(":."), Text(".:"))))
    _d2 = Alternative(Series(Text(":"), Lookahead(_logical_connector)), Series(Lookbehind(_reverse_logical_connector), Text(":")))
    _d1 = Alternative(Series(Text("."), Lookahead(_logical_connector)), Series(Lookbehind(_reverse_logical_connector), Text(".")))
    _dots = Alternative(_d4, _d3, _d2, _d1)
    equals = Text("=")
    ifonlyif = Alternative(Text("≡"), Text("<=>"))
    ifthen = Alternative(Text("⊃"), Text("=>"))
    Or = Alternative(Text("∨"), Text("v"))
    relation = RegExp('[QRST]')
    function_name = RegExp('[fghϕψχ]')
    constant = RegExp('[abcde]')
    circumflected = Alternative(RegExp('[x̂ŷẑ]'), RegExp('^[xyz]'))
    variable = RegExp('[xyz]')
    proposition = RegExp('[pqrstu]')
    number = Series(RegExp('0*'), _nat_number)
    chapter = Synonym(_nat_number)
    _individual = Alternative(variable, constant)
    function = Series(function_name, Alternative(_individual, circumflected))
    restricted_var = Series(circumflected, function)
    predication = Alternative(Series(relation, _lB, _individual, ZeroOrMore(Series(Series(Drop(Text(",")), dwsp__), _individual)), _rB), Series(_individual, relation, _individual))
    group = Alternative(Series(Text("("), formula, Text(")")), Series(Text("{"), formula, Text("}")))
    exists = Series(_lB, _exists_sign, variable, _rB, _a1, formula0)
    for_all = Series(_lB, variable, _rB, _a1, formula0)
    _affirmation = Alternative(for_all, exists, group, predication, proposition, function, variable, restricted_var, constant)
    Not = Series(_not, _affirmation)
    _element = Alternative(Not, _affirmation)
    and1 = Alternative(Series(formula0, _a1, formula0), formula0, _element)
    and2 = Alternative(Series(formula1, _a2, formula1), formula1, _element)
    and3 = Alternative(Series(formula2, _a3, formula2), formula2, _element)
    and4 = Alternative(Series(formula3, _a4, formula3), formula3, _element)
    And = Alternative(and4, and3, and2, and1)
    subscript = Series(variable, Series(Drop(Text(" ")), dwsp__))
    operator = Alternative(Or, Series(ifthen, Option(subscript)), Series(ifonlyif, Option(subscript)), equals)
    axiom = Series(_assertion_sign, Option(_dots), formula, dwsp__, Series(Drop(Text("Pp")), dwsp__))
    definition = Series(formula, dwsp__, Series(Drop(Text("Df")), dwsp__))
    theorem = Series(_assertion_sign, Option(_dots), formula)
    numbering = Series(Alternative(Series(Drop(Text("*")), dwsp__), Series(Drop(Text("∗")), dwsp__)), chapter, _cdot, number, dwsp__)
    formula4 = Alternative(Series(and4, _d4, operator, ZeroOrMore(Series(_d4, and4, _d4, operator)), Alternative(Series(_d4, and4), Series(_d3, and3), Series(_d2, and2), Series(_d1, and1), formula0, _element)), Series(Alternative(Series(and4, _d4), Series(and3, _d3), Series(and2, _d2), Series(and1, _d1), formula0, _element), operator, _d4, and4, ZeroOrMore(Series(_d4, operator, _d4, and4))))
    _assertion = Alternative(definition, axiom, theorem)
    statement = Series(numbering, _assertion)
    formula0.set(Series(_element, ZeroOrMore(Series(operator, _element))))
    formula1.set(Alternative(Series(and1, _d1, operator, ZeroOrMore(Series(_d1, and1, _d1, operator)), Alternative(Series(_d1, and1), formula0, _element)), Series(Alternative(Series(and1, _d1), formula0, _element), operator, _d1, and1, ZeroOrMore(Series(_d1, operator, _d1, and1)))))
    formula2.set(Alternative(Series(and2, _d2, operator, ZeroOrMore(Series(_d2, and2, _d2, operator)), Alternative(Series(_d2, and2), Series(_d1, and1), formula0, _element)), Series(Alternative(Series(and2, _d2), Series(and1, _d1), formula0, _element), operator, _d2, and2, ZeroOrMore(Series(_d2, operator, _d2, and2)))))
    formula3.set(Alternative(Series(and3, _d3, operator, ZeroOrMore(Series(_d3, and3, _d3, operator)), Alternative(Series(_d3, and3), Series(_d2, and2), Series(_d1, and1), formula0, _element)), Series(Alternative(Series(and3, _d3), Series(and2, _d2), Series(and1, _d1), formula0, _element), operator, _d3, and3, ZeroOrMore(Series(_d3, operator, _d3, and3)))))
    formula.set(Alternative(formula4, formula3, formula2, formula1, formula0))
    principia = Series(dwsp__, ZeroOrMore(statement), _EOF)
    root__ = TreeReduction(principia, CombinedParser.MERGE_LEAVES)
    

_raw_grammar = ThreadLocalSingletonFactory(principiaGrammar)

def get_grammar() -> principiaGrammar:
    grammar = _raw_grammar()
    if get_config_value('resume_notices'):
        resume_notices_on(grammar)
    elif get_config_value('history_tracking'):
        set_tracer(grammar, trace_history)
    try:
        if not grammar.__class__.python_src__:
            grammar.__class__.python_src__ = get_grammar.python_src__
    except AttributeError:
        pass
    return grammar
    
def parse_principia(document, start_parser = "root_parser__", *, complete_match=True):
    return get_grammar()(document, start_parser, complete_match=complete_match)


#######################################################################
#
# AST SECTION - Can be edited. Changes will be preserved.
#
#######################################################################


def save_dots_in_operators_attributes_and_remove(path: Path):
    node = path[-1]
    parent = path[-2]
    i = parent.index(node)
    if parent[i - 1].name == 'operator':
        operand = parent[i - 1]
        operand.attr['right'] = node.content
    elif parent[i + 1].name == 'operator':
        operand = parent[i + 1]
        operand.attr['left'] = node.content
    else:
        assert parent.name in ('axiom', 'theorem')
        parent.attr['left'] = '⊢' + node.content
    del parent[node]


def save_and_dots_in_left_operand_and_remove(path: Path):
    node = path[-1]
    parent = path[-2]
    i = parent.index(node)
    parent[i - 1].attr['right'] = node.content
    del parent[node]


def save_and_delete_groups_brackets(path: Path):
    node = path[-1]
    if node[0].content == "(":
        node.attr['left'] = "("
        node.attr['right'] = ")"
    else:
        assert node[0].content == "{"
        node.attr['left'] = "{"
        node.attr['right'] = "}"
    node.result = node.children[1:-1]


def process_subscripts(path: Path):
    node = path[-1]
    parent = path[-2] if len(path) >= 2 else None
    variables = []
    for operator in node.select('operator'):
        if 'subscript' in operator:
            variable = operator['subscript']['variable']
            variables.append(variable)
            del operator['subscript']
            operator.attr['subscript'] = variable.content
    if variables:
        if parent and parent.name == 'for_all':
            parent_result = []
            subscripted = parent.get_attr('subscripted', '').split(',')
            for child in parent:
                if child.name == 'variable':
                    if not any(v.content == child.content for v in variables):
                        variables.append(child)
                        subscripted.append(child.content)
                else:
                    parent_result.append(child)
            parent.result = tuple(variables) + tuple(parent.result)
            parent.attr['subscripted'] = ','.join(subscripted)
        else:
            node.result = tuple(variables) + (Node('formula', node.result).with_pos(node.pos),)
            node.name = 'for_all'
            node.attr['subscripted'] = ','.join(v.content for v in variables)


principia_AST_transformation_table = {
    # AST Transformations for the principia-grammar
    # "<": [],  # called for each node before calling its specific rules
    # "*": [],  # fallback for nodes that do not appear in this table
    # ">": [],   # called for each node after calling its specific rules
    "principia": [],
    "numbering": [],
    "assertion": [],
    "definition": [],
    "axiom": [],
    "theorem": [],
    "formula, formula4, formula3, formula2, formula1, formula0":
        [change_name('formula'), process_subscripts, replace_by_single_child],
    "And, and4, and3, and2, and1": [change_name('And'), replace_by_single_child],
    "_element": [],
    "negation": [],
    "element": [],
    "for_all": [],
    "exists": [],
    "group": [save_and_delete_groups_brackets],
    "predication": [],
    "function": [],
    "restricted_var": [],
    "individual": [replace_by_single_child],
    "chapter": [],
    "number": [],
    "proposition": [],
    "variable": [],
    "circumflected": [],
    "constant": [],
    "function_name": [],
    "relation": [],
    "_dots": [],
    "_d1, _d2, _d3, _d4": [save_dots_in_operators_attributes_and_remove],
    "_nat_number": [],
    "_cdot": [],
    "_exists_sign": [],
    "_unique_sign": [],
    "_assertion_sign": [],
    "_or": [],
    "_ifthen": [],
    "_not": [],
    "_ifonlyif": [],
    "_and": [],
    "_a1, _a2, _a3, _a4": [save_and_dots_in_left_operand_and_remove],
    "_logical_sign": [],
    "_reverse_logical_sign": [],
    "_EOF": [],
}



def _run_principia_AST_transformation(root: RootNode) -> RootNode:
    root = traverse(root, transformation_table=principia_AST_transformation_table.copy())
    root.stage = 'ast'
    return root
    

def principiaTransformer() -> TransformerCallable:
    """Creates a transformation function that does not share state with other
    threads or processes."""
    return _run_principia_AST_transformation
    # return partial(traverse, transformation_table=principia_AST_transformation_table.copy())


get_transformer = ThreadLocalSingletonFactory(principiaTransformer)


def transform_principia(cst):
    return get_transformer()(cst)


#######################################################################
#
# COMPILER SECTION - Can be edited. Changes will be preserved.
#
#######################################################################


Precedence_Table = expand_table({
    'Not, for_all, exists': 4,
    'And, Or': 3,
    'ifthen': 2,
    'ifonlyif, equals': 1
})


class principiaCompiler(Compiler):
    """Compiler for the abstract-syntax-tree of a principia source file.
    """

    def __init__(self):
        super(principiaCompiler, self).__init__()
        self.forbid_returning_None = True  # set to False if any compilation-method is allowed to return None

    def reset(self):
        super().reset()
        # initialize your variables here, not in the constructor!

    def prepare(self, root: RootNode) -> None:
        assert root.stage == 'ast', root.stage

    def finalize(self, result: Any) -> Any:
        if isinstance(self.tree, RootNode):
            root = cast(RootNode, self.tree)
            root.stage = "LST"  # logical syntax tree
        return result

    def remove_attributes(self, node):
        node = self.fallback_compiler(node)
        node.attr = {}
        return node

    def brackets_unary(self, node):
        # assert len(node.children) == 1, node.as_sxpr()
        argument = node.result[-1]
        arg_precedence = Precedence_Table.get(argument.name, 10)
        if arg_precedence < Precedence_Table[node.name]:
            argument.attr['left'] = '('
            argument.attr['right'] = ')'

    def brackets_binary(self, node):
        assert len(node.children) == 2, node.as_sxpr()
        left, right = node.result
        left_precedence = Precedence_Table.get(left.name, 10)
        node_precedence = Precedence_Table[node.name]
        right_precedence = Precedence_Table.get(right.name, 10)
        if left_precedence < node_precedence:
            left.attr['left'] = '('
            left.attr['right'] = ')'
        if right_precedence <= node_precedence:
            right.attr['left'] = '('
            right.attr['right'] = ')'

    def on_principia(self, node):
        return self.fallback_compiler(node)

    def on_definition(self, node):
        assert len(node.children) == 1
        node = self.fallback_compiler(node)
        assert len(node[0].children) == 2
        node[0].attr['subscript'] = 'df'
        return node

    def on_axiom(self, node):
        assert len(node.children) == 1
        return self.remove_attributes(node)

    def on_theorem(self, node):
        assert len(node.children) ==  1
        return self.remove_attributes(node)

    def on_formula(self, node):
        node = self.fallback_compiler(node)

        # structural pre-conditions
        assert len(node.children) >= 3
        assert len(node.children) % 2 == 1
        assert all(item.name == 'operator' for item in node.children[1::2])

        # convert formula to a binary tree
        left, operator, right = node[0:3]
        while len(node.children) > 3:
            left = Node(operator[0].name, (left, right)).with_pos(left.pos)
            node.result = (left, *node.result[3:])
            operator, right = node[1:3]
        node.name = operator[0].name
        node.result = (left, right)
        self.brackets_binary(node)
        return node

    def on_And(self, node):
        node = self.fallback_compiler(node)
        assert len(node.children) >= 2
        left, right = node[0:2]
        while len(node.children) > 2:
            left = Node('And', (left, right)).with_pos(left.pos)
            node.result = (left, *node[2:])
            right = node[1]
        self.brackets_binary(node)
        return node

    def on_group(self, node):
        assert len(node.children) == 1
        node = self.fallback_compiler(node)
        node.name = node[0].name
        if pick_from_path(self.path, "definition") is None:
            node.attr = {}
        node.attr.update(node[0].attr)
        node.result = node[0].result
        return node

    def on_Not(self, node):
        node = self.fallback_compiler(node)
        self.brackets_unary(node)
        return node

    def on_for_all(self, node):
        node = self.remove_attributes(node)
        self.brackets_unary(node)
        return node

    def on_exists(self, node):
        node = self.remove_attributes(node)
        self.brackets_unary(node)
        return node

    def on_proposition(self, node):
        return self.remove_attributes(node)

    def on_variable(self, node):
        return self.remove_attributes(node)


get_compiler = ThreadLocalSingletonFactory(principiaCompiler)


def compile_principia(ast):
    return get_compiler()(ast)


LST_junction = ('ast', get_compiler, 'LST')


#######################################################################
#
# END OF DHPARSER-SECTIONS
#
#######################################################################


#######################################################################
#
# Modern Notation
#
######################################################################


Symbols = {
    'for_all': '∀',
    'exists': '∃',
    'equals': '=',
    'ifonlyif': '≡',
    'ifthen': '⊃',
    'Or': '∨',
    'And': '&',
    'Not': '∼',
}


modern_notation_actions = expand_table({
    'principia': lambda path, *args: '\n'.join(args),
    'statement': lambda path, numbering, assertion: f"{numbering}    {assertion}",
    'numbering': lambda path, chapter, number: f"{chapter}.{number}",
    'number, chapter, definition': lambda path, content: content,
    'axiom, theorem': lambda path, formula: formula,
    'for_all, exists': lambda path, *args: \
        f"{Symbols[path[-1].name]}{','.join(args[:-1]) + (' ' if args[:-1] else '')}{args[-1]}",
    'Not': lambda path, arg: f"{Symbols[path[-1].name]}{arg}",
    'ifthen, Or, And': lambda path, left, right: f"{path[-1].get_attr('left', '')}{left}" \
        f" {Symbols[path[-1].name]} {right}{path[-1].get_attr('right', '')}",
    'equals, ifonlyif': lambda path, left, right: \
        f"{path[-1].get_attr('left', '')}{left}" \
        f"{' ' if path[-1].has_attr('subscript') else ''}" \
        f" {Symbols[path[-1].name]}{path[-1].get_attr('subscript', '')} " \
        f"{' ' if path[-1].has_attr('subscript') else ''}" \
        f"{right}{path[-1].get_attr('right', '')}",
    'function': lambda path, *args: ''.join(args),
    '*': lambda path, args:  path[-1].content
    })



def get_modern_notation():  return modern_notation


def modern_notation(lst: RootNode) -> str:
    global modern_notation_actions
    assert lst.stage == 'LST'
    result = lst.evaluate(modern_notation_actions, path=[lst])
    lst.stage = 'modern'
    return result


modern_junction = ('LST', get_modern_notation, 'modern')


#######################################################################
#
# Principia TeX
#
######################################################################

pm_tex = {
    '⊢': r'\vdash ',
    '.': r'\ldot ',
    ':': r'\colon ',
    '.:': r'\ldot\colon ',
    ':.': r'\colon\ldot ',
    '::': r'\colon\colon ',
    '⊃': r'{\supset}',
    '∨': r'\vee ',
    '∼': r'\osim ',
    '(': '(',
    ')': ')',
    '{': '\{',
    '}': '\}',
    '=': '{=}',
    '≡': '{\equiv}',
    '': ''
}

tex = pm_tex


def subscript(node)->str:
    sc = node.get_attr('subscript', '')
    return f"_{{{sc} }}" if sc else ''


principia_tex_actions = expand_table({
    'principia': lambda path, *args: '\\[\n' + '\n\n'.join(args) + '\n\\]',
    'statement': lambda path, numbering, assertion: f"{numbering}    {assertion}",
    'numbering': lambda path, chapter, number: f"\\tag*{{∗{number}⋅{chapter}}}",
    'number, chapter': lambda path, content: content,
    'axiom': lambda path, formula: f"{tex['⊢']} {tex[':']}  {formula} \\quad Pp",
    'definition':  lambda path, formula: f"{tex['⊢']} {formula} \\quad Df",
    'theorem': lambda path, formula: f"{{\\vdash}} {tex[':']}  {formula}",
    'formula, function': lambda path, *args: ''.join(args),
    'operator, proposition': lambda path, arg:
        f"{tex[path[-1].get_attr('left', '')]}{arg}{subscript(path[-1])}"\
        f"{tex[path[-1].get_attr('right', '')]}",
    'Or, ifthen, equals, ifonlyif': lambda path, arg: tex[arg],
    'And': lambda path, *args: ''.join(args),
    'Not': lambda path, arg: tex['∼'] + arg,
    'group, variable, function_name': lambda path, arg:
        f"{tex[path[-1].get_attr('left', '')]}{arg}{tex[path[-1].get_attr('right', '')]}",
    'for_all': lambda path, variable, expression:
        f"{expression}" if path[-1].has_attr('subscripted') else f"({variable[0]}){variable[1:]}{expression}",
    'exists': lambda path, variable, expression: f"(\exists {variable[0]}){variable[1:]}{expression}",
})


def get_principia_tex():  return principia_tex


def principia_tex(lst: RootNode) -> str:
    global principia_tex_actions
    assert lst.stage == 'ast'
    result = lst.evaluate(copy.deepcopy(principia_tex_actions), path=[lst])
    lst.stage = 'pm.tex'
    return result


principia_tex_junction = ('ast', get_principia_tex, 'pm.tex')


#######################################################################
#
# Moden TeX
#
######################################################################


modern_tex_actions = expand_table({
    'principia': lambda path, *args: '\\[\n' + '\n\n'.join(args) + '\n\\]',
    'statement': lambda path, numbering, assertion: f"{numbering}    {assertion}",
    'numbering': lambda path, chapter, number: f"\\tag*{{∗{number}⋅{chapter}}}",
    'number, chapter': lambda path, content: content,
    'axiom': lambda path, formula: f"{tex['⊢']} {tex[':']}  {formula} \\quad Pp",
    'definition':  lambda path, formula: f"{tex['⊢']} {formula} \\quad Df",
    'theorem': lambda path, formula: f"{{\\vdash}} {tex[':']}  {formula}",
    'formula, function': lambda path, *args: ''.join(args),
    'operator, proposition': lambda path, arg:
        f"{tex[path[-1].get_attr('left', '')]}{arg}{subscript(path[-1])}"\
        f"{tex[path[-1].get_attr('right', '')]}",
    'Or, ifthen, equals, ifonlyif': lambda path, arg: tex[arg],
    'And': lambda path, *args: ''.join(args),
    'Not': lambda path, arg: tex['∼'] + arg,
    'group, variable, function_name': lambda path, arg:
        f"{tex[path[-1].get_attr('left', '')]}{arg}{tex[path[-1].get_attr('right', '')]}",
    'for_all': lambda path, variable, expression:
        f"{expression}" if path[-1].has_attr('subscripted') else f"({variable[0]}){variable[1:]}{expression}",
    'exists': lambda path, variable, expression: f"(\exists {variable[0]}){variable[1:]}{expression}",
})


def get_modern_tex():  return modern_tex


def modern_tex(lst: RootNode) -> str:
    global principia_tex_actions
    assert lst.stage == 'ast'
    result = lst.evaluate(copy.deepcopy(principia_tex_actions), path=[lst])
    lst.stage = 'pm.tex'
    return result


modern_tex_junction = ('lst', get_principia_tex, 'modern.tex')


#######################################################################


RESULT_FILE_EXTENSION = ".sxpr"  # Change this according to your needs!


def compile_src(source: str) -> Tuple[Any, List[Error]]:
    """Compiles ``source`` and returns (result, errors)."""
    result_tuple = compile_source(source, get_preprocessor(), get_grammar(), get_transformer(),
                                  get_compiler())
    return result_tuple[:2]  # drop the AST at the end of the result tuple


def serialize_result(result: Any) -> Union[str, bytes]:
    """Serialization of result. REWRITE THIS, IF YOUR COMPILATION RESULT
    IS NOT A TREE OF NODES.
    """
    if isinstance(result, Node):
        return result.serialize(how='default' if RESULT_FILE_EXTENSION != '.xml' else 'xml')
    elif isinstance(result, str):
        return result
    else:
        return repr(result)


def process_file(source: str, out_dir: str = '') -> str:
    """Compiles the source and writes the serialized results back to disk,
    unless any fatal errors have occurred. Error and Warning messages are
    written to a file with the same name as `result_filename` with an
    appended "_ERRORS.txt" or "_WARNINGS.txt" in place of the name's
    extension. Returns the name of the error-messages file or an empty
    string, if no errors or warnings occurred.
    """
    def gen_dest_name(name):
        return os.path.join(out_dir, os.path.splitext(os.path.basename(name))[0] \
                                     + RESULT_FILE_EXTENSION)

    source_filename = source if is_filename(source) else ''
    result_filename = gen_dest_name(source_filename)
    result, errors = compile_src(source)
    if not has_errors(errors, FATAL):
        if os.path.abspath(source_filename) != os.path.abspath(result_filename):
            with open(result_filename, 'w', encoding='utf-8') as f:
                f.write(serialize_result(result))
        else:
            errors.append(Error('Source and destination have the same name "%s"!'
                                % result_filename, 0, FATAL))
    if errors:
        err_ext = '_ERRORS.txt' if has_errors(errors, ERROR) else '_WARNINGS.txt'
        err_filename = os.path.splitext(result_filename)[0] + err_ext
        with open(err_filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(canonical_error_strings(errors)))
        return err_filename
    return ''


def batch_process(file_names: List[str], out_dir: str,
                  *, submit_func: Callable = None,
                  log_func: Callable = None) -> List[str]:
    """Compiles all files listed in filenames and writes the results and/or
    error messages to the directory `our_dir`. Returns a list of error
    messages files.
    """
    error_list =  []

    def run_batch(submit_func: Callable):
        nonlocal error_list
        err_futures = []
        for name in file_names:
            err_futures.append(submit_func(process_file, name, out_dir))
        for file_name, err_future in zip(file_names, err_futures):
            error_filename = err_future.result()
            if log_func:
                log_func('Compiling "%s"' % file_name)
            if error_filename:
                error_list.append(error_filename)

    if submit_func is None:
        import concurrent.futures
        from DHParser.toolkit import instantiate_executor
        with instantiate_executor(get_config_value('batch_processing_parallelization'),
                                  concurrent.futures.ProcessPoolExecutor) as pool:
            run_batch(pool.submit)
    else:
        run_batch(submit_func)
    return error_list


def main():
    # recompile grammar if needed
    script_path = os.path.abspath(__file__)
    if script_path.endswith('Parser.py'):
        grammar_path = script_path.replace('Parser.py', '.ebnf')
    else:
        grammar_path = os.path.splitext(script_path)[0] + '.ebnf'
    parser_update = False

    def notify():
        global parser_update
        parser_update = True
        print('recompiling ' + grammar_path)

    if os.path.exists(grammar_path) and os.path.isfile(grammar_path):
        if not recompile_grammar(grammar_path, script_path, force=False, notify=notify):
            error_file = os.path.basename(__file__)\
                .replace('Parser.py', '_ebnf_MESSAGES.txt')
            with open(error_file, 'r', encoding="utf-8") as f:
                print(f.read())
            sys.exit(1)
        elif parser_update:
            print(os.path.basename(__file__) + ' has changed. '
                  'Please run again in order to apply updated compiler')
            sys.exit(0)
    else:
        print('Could not check whether grammar requires recompiling, '
              'because grammar was not found at: ' + grammar_path)

    from argparse import ArgumentParser
    parser = ArgumentParser(description="Parses a principia-file and shows its syntax-tree.")
    parser.add_argument('files', nargs='+')
    parser.add_argument('-d', '--debug', action='store_const', const='debug',
                        help='Store debug information in LOGS subdirectory')
    parser.add_argument('-o', '--out', nargs=1, default=['out'],
                        help='Output directory for batch processing')
    parser.add_argument('-v', '--verbose', action='store_const', const='verbose',
                        help='Verbose output')
    parser.add_argument('--singlethread', action='store_const', const='singlethread',
                        help='Run batch jobs in a single thread (recommended only for debugging)')
    outformat = parser.add_mutually_exclusive_group()
    outformat.add_argument('-x', '--xml', action='store_const', const='xml', 
                           help='Format result as XML')
    outformat.add_argument('-s', '--sxpr', action='store_const', const='sxpr',
                           help='Format result as S-expression')
    outformat.add_argument('-t', '--tree', action='store_const', const='tree',
                           help='Format result as indented tree')
    outformat.add_argument('-j', '--json', action='store_const', const='json',
                           help='Format result as JSON')

    args = parser.parse_args()
    file_names, out, log_dir = args.files, args.out[0], ''

    # if not os.path.exists(file_name):
    #     print('File "%s" not found!' % file_name)
    #     sys.exit(1)
    # if not os.path.isfile(file_name):
    #     print('"%s" is not a file!' % file_name)
    #     sys.exit(1)

    if args.debug is not None:
        log_dir = 'LOGS'
        access_presets()
        set_preset_value('history_tracking', True)
        set_preset_value('resume_notices', True)
        set_preset_value('log_syntax_trees', frozenset(['cst', 'ast']))  # don't use a set literal, here!
        finalize_presets()
    start_logging(log_dir)

    if args.singlethread:
        set_config_value('batch_processing_parallelization', False)

    if args.xml:
        RESULT_FILE_EXTENSION = '.xml'

    def echo(message: str):
        if args.verbose:
            print(message)

    batch_processing = True
    if len(file_names) == 1:
        if os.path.isdir(file_names[0]):
            dir_name = file_names[0]
            echo('Processing all files in directory: ' + dir_name)
            file_names = [os.path.join(dir_name, fn) for fn in os.listdir(dir_name)
                          if os.path.isfile(os.path.join(dir_name, fn))]
        elif not ('-o' in sys.argv or '--out' in sys.argv):
            batch_processing = False

    if batch_processing:
        if not os.path.exists(out):
            os.mkdir(out)
        elif not os.path.isdir(out):
            print('Output directory "%s" exists and is not a directory!' % out)
            sys.exit(1)
        error_files = batch_process(file_names, out, log_func=print if args.verbose else None)
        if error_files:
            category = "ERRORS" if any(f.endswith('_ERRORS.txt') for f in error_files) \
                else "warnings"
            print("There have been %s! Please check files:" % category)
            print('\n'.join(error_files))
            if category == "ERRORS":
                sys.exit(1)
    else:
        result, errors = compile_src(file_names[0])

        if errors:
            for err_str in canonical_error_strings(errors):
                print(err_str)
            if has_errors(errors, ERROR):
                sys.exit(1)

        if args.xml:  outfmt = 'xml'
        elif args.sxpr:  outfmt = 'sxpr'
        elif args.tree:  outfmt = 'tree'
        elif args.json:  outfmt = 'json'
        else:  outfmt = 'default'
        print(result.serialize(how=outfmt) if isinstance(result, Node) else result)


if __name__ == "__main__":
    main()
