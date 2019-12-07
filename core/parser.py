class TypedToken:
    symbols = {
        '(': 'LPA', ')': 'RPA', '.': 'DOT', '|': 'ALTER',
        '?': 'QUES', '+': 'PLUS', '*': 'STAR',
    }
    TYPE_CHAR = 'CHAR'

    def __init__(self, _type, _prop):
        self._type = _type
        self._prop = _prop
        pass

    @property
    def type(self):
        return self._type

    @property
    def prop(self):
        return self._prop

    def __repr__(self):
        return "(%s, '%s')" % (self._type, self._prop)


class RegexLexer:
    @staticmethod
    def get_tokens(pattern):
        tokens = []
        for c in pattern:
            tokens.append(TypedToken(
                TypedToken.symbols.get(c, TypedToken.TYPE_CHAR),
                c
            ))
        return tokens


class RegexParser:
    """
    简单的Regex语法，使用固定写法的递归下降法实现

    regex = regex $
    regex    = term [|] regex    {push '|'}
             | term
             |                   empty?
    term     = factor term       chain {add \x08}
             | factor
    factor   = unit [*]       star {push '*'}
             | unit [+]       plus {push '+'}
             | unit [?]       optional {push '?'}
             | unit
    unit     = ( regex )
             | char              literal {push char}
    """

    def __init__(self):
        pass
