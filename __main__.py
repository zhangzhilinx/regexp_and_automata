#!/usr/bin/env python
from core.parser import RegexLexer

if __name__ == '__main__':
    tokens = RegexLexer.get_tokens("((ab|a)(b(c?)d|c))(d*)")
    pass
