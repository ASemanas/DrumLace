#!/usr/bin/env python3

from lark import *
from lark.tree import pydot__tree_to_png
import sys
from aux import *
from visitors import PatternProg,exportlist,patternlist

grammar= 'grammar_r.lark'

test_parser = Lark(open(grammar),parser="lalr").parse


source=sys.argv[1]

with open(source) as f:
    prog = f.read() 


PatternProg().visit_topdown(test_parser(prog))

for export in exportlist:
    export_ly(export,patternlist) #um ficheiro lilypond por export
    export_sh(export,patternlist)