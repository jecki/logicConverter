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
from typing import Tuple, List, Set, Union, Any, Optional, Callable, cast

try:
    scriptdir = os.path.dirname(os.path.realpath(__file__))
except NameError:
    scriptdir = ''
if scriptdir and scriptdir not in sys.path: sys.path.append(scriptdir)

try:
    from DHParser import versionnumber
except (ImportError, ModuleNotFoundError):
    i = scriptdir.rfind("/DHParser/")
    if i >= 0:
        dhparserdir = scriptdir[:i + 10]  # 10 = len("/DHParser/")
        if dhparserdir not in sys.path:  sys.path.insert(0, dhparserdir)

from DHParser.compile import Compiler, compile_source, Junction, full_compile
from DHParser.configuration import set_config_value, add_config_values, get_config_value, \
    access_thread_locals, access_presets, finalize_presets, set_preset_value, \
    get_preset_value, read_local_config, CONFIG_PRESET, NEVER_MATCH_PATTERN, ALLOWED_PRESET_VALUES
from DHParser import dsl
from DHParser.dsl import recompile_grammar
from DHParser.ebnf import grammar_changed
from DHParser.error import ErrorCode, Error, canonical_error_strings, has_errors, NOTICE, \
    WARNING, ERROR, FATAL
from DHParser.log import start_logging, suspend_logging, resume_logging
from DHParser.nodetree import Node, WHITESPACE_PTYPE, TOKEN_PTYPE, RootNode, Path, ZOMBIE_TAG, \
    pick_from_path
from DHParser.parse import Grammar, PreprocessorToken, Whitespace, Drop, DropFrom, AnyChar, Parser, \
    Lookbehind, Lookahead, Alternative, Pop, Text, Synonym, Counted, Interleave, INFINITE, ERR, \
    Option, NegativeLookbehind, OneOrMore, RegExp, SmartRE, Retrieve, Series, Capture, TreeReduction, \
    ZeroOrMore, Forward, NegativeLookahead, Required, CombinedParser, Custom, IgnoreCase, \
    LateBindingUnary, mixin_comment, last_value, matching_bracket, optional_last_value, \
    PARSER_PLACEHOLDER, RX_NEVER_MATCH, UninitializedError
from DHParser.pipeline import end_points, full_pipeline, create_parser_junction, \
    create_preprocess_junction, create_junction, PseudoJunction, PipelineResult
from DHParser.preprocess import nil_preprocessor, PreprocessorFunc, PreprocessorResult, \
    gen_find_include_func, preprocess_includes, make_preprocessor, chain_preprocessors
from DHParser.stringview import StringView
from DHParser.toolkit import is_filename, load_if_file, cpu_count, \
    ThreadLocalSingletonFactory, expand_table, static, CancelQuery, re
from DHParser.trace import set_tracer, resume_notices_on, trace_history
from DHParser.transform import is_empty, remove_if, TransformationDict, TransformerFunc, \
    transformation_factory, remove_children_if, move_fringes, normalize_whitespace, \
    is_anonymous, name_matches, reduce_single_child, replace_by_single_child, replace_or_reduce, \
    remove_whitespace, replace_by_children, remove_empty, remove_tokens, flatten, all_of, \
    any_of, transformer, merge_adjacent, collapse, collapse_children_if, transform_result, \
    remove_children, remove_content, remove_brackets, change_name, remove_anonymous_tokens, \
    keep_children, is_one_of, not_one_of, content_matches, apply_if, peek, \
    remove_anonymous_empty, keep_nodes, traverse_locally, strip, lstrip, rstrip, \
    replace_content_with, forbid, assert_content, remove_infix_operator, add_error, error_on, \
    left_associative, lean_left, node_maker, has_descendant, neg, has_ancestor, insert, \
    positions_of, replace_child_names, add_attributes, delimit_children, merge_connected, \
    has_attr, has_parent, has_children, has_child, apply_unless, apply_ifelse, traverse
from DHParser import parse as parse_namespace__

import DHParser.versionnumber
if DHParser.versionnumber.__version_info__ < (1, 9, 3):
    print(f'DHParser version {DHParser.versionnumber.__version__} is lower than the DHParser '
          f'version 1.9.3, {os.path.basename(__file__)} has first been generated with. '
          f'Please install a more recent version of DHParser to avoid unexpected errors!')

if sys.version_info >= (3, 14, 0):
    CONFIG_PRESET['multicore_pool'] = 'InterpreterPool'
read_local_config(os.path.join(scriptdir, 'principiaConfig.ini'))


#######################################################################
#
# PREPROCESSOR SECTION - Can be edited. Changes will be preserved.
#
#######################################################################



# To capture includes, replace the NEVER_MATCH_PATTERN
# by a pattern with group "name" here, e.g. r'\input{(?P<name>.*)}'
RE_INCLUDE = NEVER_MATCH_PATTERN
RE_COMMENT = ';.*?(?:\\n|$)'  # THIS MUST ALWAYS BE THE SAME AS principiaGrammar.COMMENT__ !!!


def principiaTokenizer(original_text) -> Tuple[str, List[Error]]:
    # Here, a function body can be filled in that adds preprocessor tokens
    # to the source code and returns the modified source.
    return original_text, []

preprocessing: PseudoJunction = create_preprocess_junction(
    principiaTokenizer, RE_INCLUDE, RE_COMMENT)

get_preprocessor = preprocessing.factory


def preprocess_principia(source):
    return get_preprocessor()(source)


#######################################################################
#
# PARSER SECTION - Don't edit! CHANGES WILL BE OVERWRITTEN!
#
#######################################################################

class principiaGrammar(Grammar):
    r"""Parser for a principia document.

    Instantiate this class and then call the instance with the source
    code as the single argument in order to use the parser, e.g.:
        parser = principia()
        syntax_tree = parser(source_code)
    """
    and1 = Forward()
    formula = Forward()
    formula0 = Forward()
    formula1 = Forward()
    formula2 = Forward()
    formula3 = Forward()
    source_hash__ = "c0fd99e9a5e72e0d97cdd7b8fe8d95f8"
    early_tree_reduction__ = CombinedParser.MERGE_LEAVES
    disposable__ = re.compile('(?:_nat_number$|_element$|_EOF$|_dots$|_affirmation$|_individual$|_exists_sign$|_assertion_sign$|_lB$|_rB$|_assertion$|_not$|_cdot$|_LF$)')
    static_analysis_pending__ = []  # type: List[bool]
    parser_initialization__ = ["upon instantiation"]
    COMMENT__ = r';.*?(?:\n|$)'
    comment_rx__ = re.compile(COMMENT__)
    WHITESPACE__ = r'[\t ]*'
    WSP_RE__ = mixin_comment(whitespace=WHITESPACE__, comment=COMMENT__)
    wsp__ = Whitespace(WSP_RE__)
    dwsp__ = Drop(Whitespace(WSP_RE__))
    _EOF = Drop(NegativeLookahead(RegExp('.')))
    _LF = Drop(RegExp('[ \\t\\r]*\\n\\s*'))
    _reverse_logical_connector = RegExp('[⊢∨⊃≡=]|-[|]|>=|<=>')
    _logical_connector = RegExp('[⊢∨⊃≡=]|[|]-|=>|<=>')
    _rB = Drop(Series(Text(")"), dwsp__))
    _lB = Drop(Series(Text("("), dwsp__))
    _a4 = Series(Text("::"), dwsp__, NegativeLookahead(_logical_connector))
    _a3 = Series(Alternative(Text(".:"), Text(":.")), dwsp__, NegativeLookahead(_logical_connector))
    _a2 = Series(Text(":"), dwsp__, NegativeLookahead(_logical_connector))
    _a1 = Series(Text("."), dwsp__, NegativeLookahead(_logical_connector))
    _not = Drop(Series(Alternative(Text("∼"), Text("~")), dwsp__))
    _assertion_sign = Drop(Series(Alternative(Text("⊢"), Text("|-")), dwsp__))
    _exists_sign = Drop(Alternative(Text("∃"), Text("€")))
    _nat_number = RegExp('[1-9]\\d*')
    _cdot = Drop(Alternative(RegExp('[·⋅]'), Series(Text("."), Lookahead(_nat_number))))
    _d4 = Alternative(Series(Text("::"), dwsp__, Lookahead(_logical_connector)), Series(Lookbehind(_reverse_logical_connector), Text("::"), dwsp__))
    _d3 = Alternative(Series(Alternative(Text(":."), Text(".:")), dwsp__, Lookahead(_logical_connector)), Series(Lookbehind(_reverse_logical_connector), Alternative(Text(":."), Text(".:")), dwsp__))
    _d2 = Alternative(Series(Text(":"), dwsp__, Lookahead(_logical_connector)), Series(Lookbehind(_reverse_logical_connector), Text(":"), dwsp__))
    _d1 = Alternative(Series(Text("."), dwsp__, Lookahead(_logical_connector)), Series(Lookbehind(_reverse_logical_connector), Text("."), dwsp__))
    _dots = Alternative(_d4, _d3, _d2, _d1)
    equals = Series(Text("="), dwsp__)
    ifonlyif = Series(Alternative(Text("≡"), Text("<=>")), dwsp__)
    ifthen = Series(Alternative(Text("⊃"), Text("=>")), dwsp__)
    Or = Series(Alternative(Text("∨"), Text("v")), dwsp__)
    relation = RegExp('[QRSTPG][a-z]?')
    function_name = RegExp('[fghϕψχ]')
    number = Synonym(_nat_number)
    constant = RegExp('[abcde]')
    circumflected = Alternative(RegExp('[x̂ŷẑ]'), RegExp('^[xyz]'))
    variable = RegExp('[xyz]')
    proposition = RegExp('[pqrstu]')
    counter = Series(RegExp('0*'), _nat_number)
    chapter = Synonym(_nat_number)
    _individual = Alternative(variable, constant, number)
    function = Series(function_name, Alternative(_individual, circumflected))
    restricted_var = Series(circumflected, function)
    predication = Alternative(Series(relation, _lB, _individual, ZeroOrMore(Series(Series(Drop(Text(",")), dwsp__), _individual)), _rB), Series(_individual, relation, _individual))
    group = Alternative(Series(Text("("), dwsp__, formula, Text(")"), dwsp__), Series(Text("{"), dwsp__, formula, Text("}"), dwsp__))
    exists = Series(_lB, _exists_sign, variable, _rB, _a1, and1)
    for_all = Series(_lB, variable, _rB, _a1, formula0)
    _affirmation = Alternative(for_all, exists, group, predication, proposition, function, variable, restricted_var, constant, number)
    Not = Series(_not, _affirmation)
    _element = Alternative(Not, _affirmation)
    axiom = Series(_assertion_sign, Option(_dots), formula, dwsp__, Series(Drop(Text("Pp")), dwsp__))
    and2 = Alternative(Series(formula1, _a2, formula1), formula1, _element)
    and3 = Alternative(Series(formula2, _a3, formula2), formula2, _element)
    and4 = Alternative(Series(formula3, _a4, formula3), formula3, _element)
    subscript = Series(variable, Series(Drop(Text(" ")), dwsp__))
    operator = Alternative(Or, Series(ifthen, Option(subscript)), Series(ifonlyif, Option(subscript)), equals)
    definition = Series(formula, dwsp__, Series(Drop(Text("Df")), dwsp__))
    theorem = Series(_assertion_sign, Option(_dots), formula)
    numbering = Series(Alternative(Series(Drop(Text("*")), dwsp__), Series(Drop(Text("∗")), dwsp__)), chapter, _cdot, counter, dwsp__)
    sloppy = Series(Option(numbering), Option(_assertion_sign), Option(_dots), formula, Option(Series(dwsp__, Alternative(Series(Drop(Text("Df")), dwsp__), Series(Drop(Text("Pp")), dwsp__)))))
    formula4 = Alternative(Series(and4, _d4, operator, ZeroOrMore(Series(_d4, and4, _d4, operator)), Alternative(Series(_d4, and4), Series(_d3, and3), Series(_d2, and2), Series(_d1, and1), formula0, _element)), Series(Alternative(Series(and4, _d4), Series(and3, _d3), Series(and2, _d2), Series(and1, _d1), formula0, _element), operator, _d4, and4, ZeroOrMore(Series(_d4, operator, _d4, and4))), and4)
    _assertion = Alternative(definition, axiom, theorem)
    statement = Series(numbering, _assertion)
    and1.set(Alternative(Series(formula0, _a1, formula0), formula0, _element))
    formula0.set(Series(_element, ZeroOrMore(Series(operator, _element))))
    formula1.set(Alternative(Series(and1, _d1, operator, ZeroOrMore(Series(_d1, and1, _d1, operator)), Alternative(Series(_d1, and1), formula0, _element)), Series(Alternative(Series(and1, _d1), formula0, _element), operator, _d1, and1, ZeroOrMore(Series(_d1, operator, _d1, and1))), and1))
    formula2.set(Alternative(Series(and2, _d2, operator, ZeroOrMore(Series(_d2, and2, _d2, operator)), Alternative(Series(_d2, and2), Series(_d1, and1), formula0, _element)), Series(Alternative(Series(and2, _d2), Series(and1, _d1), formula0, _element), operator, _d2, and2, ZeroOrMore(Series(_d2, operator, _d2, and2))), and2))
    formula3.set(Alternative(Series(and3, _d3, operator, ZeroOrMore(Series(_d3, and3, _d3, operator)), Alternative(Series(_d3, and3), Series(_d2, and2), Series(_d1, and1), formula0, _element)), Series(Alternative(Series(and3, _d3), Series(and2, _d2), Series(and1, _d1), formula0, _element), operator, _d3, and3, ZeroOrMore(Series(_d3, operator, _d3, and3))), and3))
    formula.set(Alternative(formula4, formula3, formula2, formula1, formula0))
    principia = Series(dwsp__, ZeroOrMore(Series(Alternative(statement, sloppy), ZeroOrMore(_LF))), _EOF)
    root__ = principia
    
parsing: PseudoJunction = create_parser_junction(principiaGrammar)
get_grammar = parsing.factory  # for backwards compatibility, only

try:
    assert RE_INCLUDE == NEVER_MATCH_PATTERN or \
        RE_COMMENT in (principiaGrammar.COMMENT__, NEVER_MATCH_PATTERN), \
        "Please adjust the pre-processor-variable RE_COMMENT in file principiaParser.py so that " \
        "it either is the NEVER_MATCH_PATTERN or has the same value as the COMMENT__-attribute " \
        "of the grammar class principiaGrammar! " \
        'Currently, RE_COMMENT reads "%s" while COMMENT__ is "%s". ' \
        % (RE_COMMENT, principiaGrammar.COMMENT__) + \
        "\n\nIf RE_COMMENT == NEVER_MATCH_PATTERN then includes will deliberately be " \
        "processed, otherwise RE_COMMENT==principiaGrammar.COMMENT__ allows the " \
        "preprocessor to ignore comments."
except (AttributeError, NameError):
    pass


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
    "definition": [],
    "axiom": [],
    "theorem": [],
    "formula, formula4, formula3, formula2, formula1, formula0":
        [change_name('formula'), process_subscripts, replace_by_single_child],
    # "And": [replace_by_single_child],
    "and4, and3, and2, and1": [change_name('And'), replace_by_single_child],
    "_element": [],
    "for_all": [],
    "exists": [],
    "group": [save_and_delete_groups_brackets],
    "predication": [],
    "function": [],
    "restricted_var": [],
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
    # "_unique_sign": [],
    "_assertion_sign": [],
    "_not": [],
    # "_and": [],
    "_a1, _a2, _a3, _a4": [save_and_dots_in_left_operand_and_remove],
    "_EOF": [],
}



def principiaTransformer() -> TransformerFunc:
    return static(partial(
        transformer, 
        transformation_table=principia_AST_transformation_table.copy(),
        src_stage='CST', 
        dst_stage='AST'))

ASTTransformation: Junction = Junction(
    'CST', ThreadLocalSingletonFactory(principiaTransformer), 'AST')
get_transformer = ASTTransformation.factory  # for backwards compatibility, only


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
        assert root.stage == 'AST', root.stage

    def finalize(self, result: Any) -> Any:
        if isinstance(self.tree, RootNode):
            root = cast(RootNode, self.tree)
            root.stage = 'LST'  # logical syntax tree
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


    # def on__a1(self, node):
    #     return node

    # def on__a2(self, node):
    #     return node

    # def on__a3(self, node):
    #     return node

    # def on__a4(self, node):
    #     return node

    # def on__lB(self, node):
    #     return node

    # def on__rB(self, node):
    #     return node

    # def on__logical_connector(self, node):
    #     return node

    # def on__reverse_logical_connector(self, node):
    #     return node

    # def on__LF(self, node):
    #     return node

    # def on__EOF(self, node):
    #     return node



compiling: Junction = create_junction(
    principiaCompiler, "AST", "LST")
get_compiler = compiling.factory  # for backwards compatibility, only


def compile_principia(ast):
    return get_compiler()(ast)


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
    'predication':
        lambda path, *args: f"{args[0]}({','.join(args[1:])})"
                if len(args[0]) > 1 or any(arg.isnumeric() for arg in args[1:])
                else f"{args[0]}{','.join(args[1:])}",
    '*': lambda path, *args:  path[-1].content
    })


def get_modern_notation():  return modern_notation


def modern_notation(lst: RootNode) -> str:
    global modern_notation_actions
    assert lst.stage == 'LST'
    result = lst.evaluate(modern_notation_actions, path=[lst])
    lst.stage = 'modern'
    return result


modern_junction = Junction('LST', get_modern_notation, 'modern')


#######################################################################
#
# Principia TeX
#
######################################################################

tex = {
    '⊢': r'\vdash ',
    '|-': r'\vdash ',
    '⋅': r'\cdot ',
    '.': r'.',  # r'\ldot ',
    ':': r':',  # r'\colon ',
    '.:': r'.:',  # r'\ldot\colon ',
    ':.': r':.',  # r'\colon\ldot ',
    '::': r'::',  # r'\colon\colon ',
    '⊃': r'{\supset}',
    '=>': r'{\supset}',
    '∨': r' \vee ',
    '&': r'\:\&\: ',  # r'\wedge ',
    '∼': r'{\sim}',  # r'\neg',
    '∀': r'\forall ',
    '∃': r'\exists ',
    '(': '(',
    ')': ')',
    '{': r'\{',
    '}': r'\}',
    '=': '{=}',
    '≡': r'{\equiv}',
    '<=>': r'{\equiv}',
    '': ''
}

def subscript(node)->str:
    sc = node.get_attr('subscript', '')
    return f"_{{{sc} }}" if sc else ''


principia_tex_actions = expand_table({
    'principia': lambda path, *args: '\\[ ' + '\n\n'.join(args) + ' \\]',
    'statement': lambda path, numbering, assertion: f"{numbering}    {assertion}",
    'numbering': lambda path, chapter, number: f"\\tag*{{∗{chapter}⋅{number}}}",
    'number, chapter': lambda path, content: content,
    'axiom': lambda path, formula: f"{tex['⊢']} {tex[':']}  {formula} \\quad Pp",
    'definition':  lambda path, formula: f"{tex['⊢']} {formula} \\quad Df",
    'theorem': lambda path, formula: f"{formula}",
    'formula, function': lambda path, *args: ''.join(args),
    'predication':
        lambda path, *args: f"{args[0]}({','.join(args[1:])})"
        if len(args[0]) > 1 or any(arg.isnumeric() for arg in args[1:])
        else f"{args[0]}{','.join(args[1:])}",
    'operator, proposition': lambda path, arg:
        f"{tex[path[-1].get_attr('left', '')]}{arg}{subscript(path[-1])}"
        f"{tex[path[-1].get_attr('right', '')]}",
    'Or, ifthen, equals, ifonlyif': lambda path, arg: tex[arg],
    'And': lambda path, *args: ''.join(args),
    'Not': lambda path, arg: tex['∼'] + arg,
    'group, variable, function_name': lambda path, arg:
        f"{tex[path[-1].get_attr('left', '')]}{arg}{tex[path[-1].get_attr('right', '')]}",
    'for_all': lambda path, variable, expression:
        f"{expression}" if path[-1].has_attr('subscripted') else f"({variable[0]}){variable[1:]}{expression}",
    'exists': lambda path, variable, expression: fr"(\exists {variable[0]}){variable[1:]}{expression}",
    '*': lambda path, *args:  path[-1].content
})


def get_principia_tex():  return principia_tex


def principia_tex(ast: RootNode) -> str:
    global principia_tex_actions
    assert ast.stage == 'AST'
    result = ast.evaluate(copy.deepcopy(principia_tex_actions), path=[ast])
    ast.stage = 'pm.tex'
    return result


principia_tex_junction = Junction('AST', get_principia_tex, 'pm.tex')


#######################################################################
#
# Moden TeX
#
######################################################################


quad = r' \quad '
medmuskip = r' \: '
thickmuskip = r' \; '


modern_tex_actions = expand_table({
    'principia': lambda path, *args: '\\[ ' + '\n\n'.join(args) + ' \\]',
    'statement': lambda path, numbering, assertion: f"{numbering}    {assertion}",
    'numbering': lambda path, chapter, number: f"\\tag*{{{chapter}.{number}}}",
    'number, chapter, definition': lambda path, content: content,
    'axiom, theorem': lambda path, formula: f"{formula}",
    'for_all': lambda path, variable, expression:
        fr"\forall {variable}\;{expression}",
    'exists': lambda path, variable, expression:
        fr"\exists {variable}\;{expression}",
    'Not': lambda path, arg: tex['∼'] + arg,
    'ifthen, Or, And': lambda path, left, right: f"{path[-1].get_attr('left', '')}{left}"
        f" {tex[Symbols[path[-1].name]]}{right}{path[-1].get_attr('right', '')}",
    'equals, ifonlyif': lambda path, left, right:
        f"{path[-1].get_attr('left', '')}{left}"
        f"{thickmuskip if path[-1].has_attr('subscript') else ' '}"
        f"{Symbols[path[-1].name]}_{{{path[-1].get_attr('subscript', '')}}}"
        f"{thickmuskip if path[-1].has_attr('subscript') else ' '}"
        f"{right}{path[-1].get_attr('right', '')}",
    'function': lambda path, *args: ''.join(args),
    'predication': lambda path, *args: f"{args[0]}({','.join(args[1:])})"
        if len(args[0]) > 1 or any(arg.isnumeric() for arg in args[1:])
        else f"{args[0]}{','.join(args[1:])}",
    '*': lambda path, *args:  path[-1].content
    })

def get_modern_tex():  return modern_tex


def modern_tex(lst: RootNode) -> str:
    global modern_tex_actions
    assert lst.stage == 'LST'
    result = lst.evaluate(copy.deepcopy(modern_tex_actions), path=[lst])
    lst.stage = 'modern.tex'
    return result


modern_tex_junction = Junction('LST', get_modern_tex, 'modern.tex')


#######################################################################

# Add your own stages to the junctions and target-lists, below
# (See DHParser.compile for a description of junctions)

# ADD YOUR OWN POST-PROCESSING-JUNCTIONS HERE:
junctions = set([ASTTransformation, compiling, modern_junction,
                 principia_tex_junction, modern_tex_junction])

# put your targets of interest, here. A target is the name of result (or stage)
# of any transformation, compilation or postprocessing step after parsing.
# Serializations of the stages listed here will be written to disk when
# calling process_file() or batch_process() and also appear in test-reports.
targets = end_points(junctions)
# alternative: targets = set([compiling.dst])

# provide a set of those stages for which you would like to see the output
# in the test-report files, here. (AST is always included)
test_targets = set(j.dst for j in junctions)
# alternative: test_targets = targets

# add one or more serializations for those targets that are node-trees
serializations = expand_table(dict([('*', [get_config_value('default_serialization')])]))


#######################################################################
#
# Main program
#
#######################################################################

def pipeline(source: str,
             target: Union[str, Set[str]] = "",
             start_parser: Union[str,Set[str]] = "root_parser__",
             *, cancel_query: Optional[CancelQuery] = None) -> PipelineResult:
    """Runs the source code through the processing pipeline. If
    the parameter target is not the empty string, only the stages required
    for the given target will be passed. See :py:func:`compile_src` for the
    explanation of the other parameters.
    """
    global targets
    if target:
        target_set = {target} if isinstance(target, str) else target
    else:
        target_set = targets
    return full_pipeline(
        source, preprocessing.factory, parsing.factory, junctions, target_set,
        start_parser, cancel_query = cancel_query)


def compile_src(source: str,
                target: str = "",
                start_parser: str = "root_parser__",
                *, cancel_query: Optional[CancelQuery] = None) -> Tuple[Any, List[Error]]:
    """Compiles the source to a single target and returns the result of the compilation
    as well as a (possibly empty) list or errors or warnings that have occurred in the
    process.

    :param source: Either a file name or a source text. Anything that is not a valid
        file name is assumed to be a source text. Add a byte-order mark ("\ufeff")
        at the beginning of short, i.e. one-line source texts, to avoid these being
        misinterpreted as filenames.
    :param target: the name of the target stage up to which the processing pipeline
        will be proceeded
    :param start_parser: the parser with which the parsing shall start. The default
        is the root-parser, but if only snippets of a full document shall be processed,
        it makes sense to pick another parser, here.

    :returns: a tuple (data, list of errors) of the data in the format of the
        target-stage selected by parameter "target" and of the potentially
        empty list of errors.
    """
    full_compilation_result = pipeline(source, target, start_parser)
    return full_compilation_result[target]


def compile_snippet(source_code: str,
                    target: str = "",
                    start_parser: str = "root_parser__",
                    *, cancel_query: Optional[CancelQuery] = None) -> Tuple[Any, List[Error]]:
    """Compiles a piece of source_code. In contrast to :py:func:`compile_src` the
    parameter source_code is always understood as a piece of source-code and never
    as a filename, not even if it is a one-liner that could also be a file-name.
    """
    if source_code[0:1] not in ('\ufeff', '\ufffe') and \
            source_code[0:3] not in ('\xef\xbb\xbf', '\x00\x00\ufeff', '\x00\x00\ufffe'):
        source_code = '\ufeff' + source_code  # add a byteorder-mark for disambiguation
    return compile_src(source_code, target, start_parser, cancel_query = cancel_query)


def process_file(source: str, out_dir: str = '', target_set: Set[str]=frozenset(),
                 *, cancel_query: CancelQuery = None) -> str:
    """Compiles the source and writes the serialized results back to disk,
    unless any fatal errors have occurred. Error and Warning messages are
    written to a file with the same name as `result_filename` with an
    appended "_ERRORS.txt" or "_WARNINGS.txt" in place of the name's
    extension. Returns the name of the error-messages file or an empty
    string if no errors or warnings occurred.
    """
    global serializations, targets
    if not target_set:
        target_set = targets
    elif not target_set <= targets:
        raise AssertionError('Unknown compilation target(s): ' +
                             ', '.join(t for t in target_set - targets))
    # serializations = get_config_value('principia_serializations', serializations)
    return dsl.process_file(source, out_dir, preprocessing.factory, parsing.factory,
                            junctions, target_set, serializations, cancel_query)


def process_file_wrapper(args: Tuple[str, str, CancelQuery]) -> str:
    return process_file(args[0], args[1], cancel_query=args[2])


def batch_process(file_names: List[str], out_dir: str,
                  *, submit_func: Optional[Callable] = None,
                  log_func: Optional[Callable] = None,
                  cancel_func: Optional[Callable] = None) -> List[str]:
    """Compiles all files listed in file_names and writes the results and/or
    error messages to the directory `our_dir`. Returns a list of error
    messages files.
    """
    from principiaParser import process_file_wrapper
    return dsl.batch_process(file_names, out_dir, process_file_wrapper,
        submit_func=submit_func, log_func=log_func, cancel_func=cancel_func)


def main(called_from_app=False) -> bool:
    global targets, test_targets, serializations, junctions
    # recompile grammar if needed
    scriptpath = os.path.abspath(os.path.realpath(__file__))
    if scriptpath.endswith('Parser.py'):
        grammar_path = scriptpath.replace('Parser.py', '.ebnf')
    else:
        grammar_path = os.path.splitext(scriptpath)[0] + '.ebnf'
    parser_update = False

    def notify():
        nonlocal parser_update
        parser_update = True
        print('recompiling ' + grammar_path)

    if os.path.exists(grammar_path) and os.path.isfile(grammar_path):
        if not recompile_grammar(grammar_path, scriptpath, force=False, notify=notify):
            error_file = os.path.basename(__file__)\
                .replace('Parser.py', '_ebnf_MESSAGES.txt')
            with open(error_file, 'r', encoding="utf-8") as f:
                print(f.read())
            sys.exit(1)
        elif parser_update:
            if '--dontrerun' in sys.argv:
                print(os.path.basename(__file__) + ' has changed. '
                      'Please run again in order to apply updated compiler')
                sys.exit(0)
            else:
                import platform, subprocess
                call = [sys.executable, __file__, '--dontrerun'] + sys.argv[1:]
                result = subprocess.run(call, capture_output=True)
                print(result.stdout.decode('utf-8'))
                sys.exit(result.returncode)
    else:
        print('Could not check whether grammar requires recompiling, '
              'because grammar was not found at: ' + grammar_path)

    from argparse import ArgumentParser
    parser = ArgumentParser(description="Parses a principia-file and shows its syntax-tree.")
    parser.add_argument('files', nargs='*' if called_from_app else '+')
    parser.add_argument('-d', '--debug', action='store_const', const='debug',
                        help='Write debug information to LOGS subdirectory')
    parser.add_argument('-o', '--out', nargs=1, default=['out'],
                        help='Output directory for batch processing')
    parser.add_argument('-v', '--verbose', action='store_const', const='verbose',
                        help='Verbose output')
    parser.add_argument('-f', '--force', action='store_const', const='force',
                        help='Write output file even if errors have occurred')
    parser.add_argument('--singlethread', action='store_const', const='singlethread',
                        help='Run batch jobs in a single thread (recommended only for debugging)')
    parser.add_argument('--dontrerun', action='store_const', const='dontrerun',
                        help='Do not automatically run again if the grammar has been recompiled.')
    parser.add_argument('-s', '--serialize', nargs=1, default=[],
                        help="Choose serialization format for tree structured data. Available: "
                             + ', '.join(ALLOWED_PRESET_VALUES['default_serialization']))
    parser.add_argument('-t', '--target', nargs='+', default=[],
                        help='Pick compilation target(s). Available targets: '
                             '%s; default: %s' % (', '.join(test_targets), ', '.join(targets)))

    args = parser.parse_args()
    file_names, out, log_dir = args.files, args.out[0], ''

    read_local_config(os.path.join(scriptdir, 'principiaConfig.ini'))

    if args.serialize:
        if (args.serialize[0].lower() not in
                [sf.lower() for sf in ALLOWED_PRESET_VALUES['default_serialization']]):
            print('Unknown serialization format: ' + args.serialize[0] +
                  '! Available formats for tree-structures: '
                  + ', '.join(ALLOWED_PRESET_VALUES['default_serialization']))
            sys.exit(1)
        serializations['*'] = args.serialize
        access_presets()
        set_preset_value('principia_serializations', serializations, allow_new_key=True)
        finalize_presets()

    if args.debug is not None:
        log_dir = 'LOGS'
        access_presets()
        set_preset_value('history_tracking', True)
        set_preset_value('resume_notices', True)
        set_preset_value('log_syntax_trees', frozenset(['CST', 'AST']))  # don't use a set literal, here!
        start_logging(log_dir)
        finalize_presets()

    if args.singlethread:
        set_config_value('batch_processing_parallelization', False)

    if args.target:
        chosen = set(args.target)
        unknown = chosen - test_targets
        if unknown:
            print('Unknown targets: ' + ', '.join(unknown) + ' chosen!' +
                  '\nAvailable targets: ' + ', '.join(test_targets))
            sys.exit(1)
        targets = chosen

    def echo(message: str):
        if args.verbose:
            print(message)

    if called_from_app and not file_names:  return False

    batch_processing = True
    if len(file_names) == 1:
        if os.path.isdir(file_names[0]):
            dir_name = file_names[0]
            echo('Processing all files in directory: ' + dir_name)
            file_names = [os.path.join(dir_name, fn) for fn in os.listdir(dir_name)
                          if fn[0:1] != '.' and os.path.isfile(os.path.join(dir_name, fn))]
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
        if len(targets) == 1:
            result, errors = compile_src(file_names[0], target=next(iter(targets)))
        else:
            result, errors = compile_src(file_names[0])  # keep default_target

        if not errors or (not has_errors(errors, ERROR)) \
                or (not has_errors(errors, FATAL) and args.force):
            print(result.serialize(serializations['*'][0])
                  if isinstance(result, Node) else result)
            if errors:  print('\n---')

        for err_str in canonical_error_strings(errors):
            print(err_str)
        if has_errors(errors, ERROR):  sys.exit(1)

    return True


if __name__ == "__main__":
    main()
