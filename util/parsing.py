from util.colors import syntax

m = '\033[36m'
token_colors = {
  'ENDMARKER': None,
  'NAME': None,
  'NUMBER': syntax.number,
  'STRING': syntax.string,
  'NEWLINE': None,
  'INDENT': None,
  'DEDENT': None,
  'LPAR': None,
  'RPAR': None,
  'LSQB': None,
  'RSQB': None,
  'COLON': syntax.default,
  'COMMA': None,
  'SEMI': None,
  'PLUS': syntax.default,
  'MINUS': syntax.default,
  'STAR': syntax.default,
  'SLASH': syntax.default,
  'VBAR': None,
  'AMPER': None,
  'LESS': None,
  'GREATER': None,
  'EQUAL': None,
  'DOT': None,
  'PERCENT': None,
  'LBRACE': None,
  'RBRACE': None,
  'EQEQUAL': None,
  'NOTEQUAL': None,
  'LESSEQUAL': None,
  'GREATEREQUAL': None,
  'TILDE': None,
  'CIRCUMFLEX': None,
  'LEFTSHIFT': None,
  'RIGHTSHIFT': None,
  'DOUBLESTAR': None,
  'PLUSEQUAL': None,
  'MINEQUAL': None,
  'STAREQUAL': None,
  'SLASHEQUAL': None,
  'PERCENTEQUAL': None,
  'AMPEREQUAL': None,
  'VBAREQUAL': None,
  'CIRCUMFLEXEQUAL': None,
  'LEFTSHIFTEQUAL': None,
  'RIGHTSHIFTEQUAL': None,
  'DOUBLESTAREQUAL': None,
  'DOUBLESLASH': None,
  'DOUBLESLASHEQUAL': None,
  'AT': None,
  'ATEQUAL': None,
  'RARROW': None,
  'ELLIPSIS': None,
  'OP': None,
  'ERRORTOKEN': None,
  'COMMENT': None,
  'NL': None,
  'ENCODING': None,
  'N_TOKENS': None,
  'NT_OFFSET': None
}

symbol_colors = {
  'single_input': None,
  'file_input': None,
  'eval_input': None,
  'decorator': None,
  'decorators': None,
  'decorated': None,
  'async_funcdef': syntax.keyword,
  'funcdef': syntax.keyword,
  'parameters': None,
  'typedargslist': None,
  'tfpdef': syntax.default,
  'varargslist': None,
  'vfpdef': None,
  'stmt': None,
  'simple_stmt': None,
  'small_stmt': None,
  'expr_stmt': None,
  'annassign': None,
  'testlist_star_expr': None,
  'augassign': None,
  'del_stmt': syntax.keyword,
  'pass_stmt': syntax.keyword,
  'flow_stmt': syntax.keyword,
  'break_stmt': syntax.keyword,
  'continue_stmt': syntax.keyword,
  'return_stmt': syntax.keyword,
  'yield_stmt': syntax.keyword,
  'raise_stmt': syntax.keyword,
  'import_stmt': None,
  'import_name': syntax.keyword,
  'import_from': syntax.keyword,
  'import_as_name': None,
  'dotted_as_name': None,
  'import_as_names': None,
  'dotted_as_names': None,
  'dotted_name': None,
  'global_stmt': syntax.keyword,
  'nonlocal_stmt': syntax.keyword,
  'assert_stmt': syntax.keyword,
  'compound_stmt': syntax.keyword,
  'async_stmt': None,
  'if_stmt': syntax.keyword,
  'while_stmt': syntax.keyword,
  'for_stmt': syntax.keyword,
  'try_stmt': syntax.keyword,
  'with_stmt': syntax.keyword,
  'with_item': syntax.keyword,
  'except_clause': syntax.keyword,
  'suite': None,
  'test': None,
  'test_nocond': None,
  'lambdef': None,
  'lambdef_nocond': None,
  'or_test': None,
  'and_test': None,
  'not_test': None,
  'comparison': None,
  'comp_op': None,
  'star_expr': None,
  'expr': None,
  'xor_expr': None,
  'and_expr': None,
  'shift_expr': None,
  'arith_expr': None,
  'term': None,
  'factor': None,
  'power': None,
  'atom_expr': None,
  'atom': None,
  'testlist_comp': None,
  'trailer': None,
  'subscriptlist': None,
  'subscript': None,
  'sliceop': None,
  'exprlist': None,
  'testlist': None,
  'dictorsetmaker': None,
  'classdef': syntax.keyword,
  'arglist': None,
  'argument': None,
  'comp_iter': None,
  'sync_comp_for': None,
  'comp_for': None,
  'comp_if': None,
  'encoding_decl': None,
  'yield_expr': None,
  'yield_arg': None
}
