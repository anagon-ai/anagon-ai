import parser
import re
import symbol
import sys
import token

from util import colors, parsing


def render(source, default_color=colors.reset, debug=False):
  r_whitespace_and_comments = re.compile(r'^\s+(#.+\n)?')

  source = source.lstrip()
  t = parser.suite(source)
  tree = t.tolist()

  prev = None
  pos = 0

  def _render_tree(node):
    nonlocal prev, pos, source

    out = ''
    if type(node) == list:
      for n in node:
        out += _render_tree(n)
    if type(node) == int:
      if token.ISTERMINAL(node):
        name = token.tok_name[node]
        color = parsing.token_colors[name]
      else:
        name = symbol.sym_name[node]
        color = parsing.symbol_colors[name]

      if color:
        out += color

      if debug:
        print((color if color else colors.reset) + '[' + name + ']')
      prev = name

    if prev == 'NAME':
      if node == 'self':
        out += colors.syntax.self
      if node in ['super', 'elif', 'else', 'print']:
        out += colors.syntax.keyword

    if type(node) == str:
      if debug:
        print(node)

      out += node
      pos += len(node)

      whitespace_and_comments = r_whitespace_and_comments.search(source[pos:])

      if whitespace_and_comments:
        if whitespace_and_comments.group(1):
          # syntax highlight comments
          out += colors.syntax.comment

        # add trailing whitespace to output (because parser removes whitespace and comma's)
        out += whitespace_and_comments.group(0)
        pos += len(whitespace_and_comments.group(0))
      out += default_color

    return out

  return default_color + _render_tree(tree)


if __name__ == '__main__':
  source = open(sys.argv[0]).read().strip()
  output = render(source)
  print(output)
