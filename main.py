#!/usr/bin/env python3

from lark import *
from lark import exceptions
from lark.tree import pydot__tree_to_png
import sys
from aux import *
from visitors import PatternProg,exportlist,patternlist

grammar= 'grammar_r.lark'


try:
    test_parser = Lark(open(grammar),parser="lalr").parse
except exceptions.LarkError as e:
    print(f"Parsing error: {e}")
    if hasattr(e, 'line') and hasattr(e, 'column'):
            print(f"Error occurred at line {e.line}, column {e.column}")
    exit(1)  # Exit with status 1 on failure

source=sys.argv[1]

with open(source) as f:
    prog = f.read() 

#pydot__tree_to_png(test_parser(prog), "out/treetest_r.png",rankdir="TB") #o site não funciona com isto

PatternProg().visit_topdown(test_parser(prog))

for export in exportlist:
    export_ly(export,patternlist) #um ficheiro lilypond por export
    export_sh(export,patternlist)