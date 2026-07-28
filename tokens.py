# tokens.py
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_STRING = 'STRING'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'

TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_MOD = 'MOD'
TT_EQUALS = 'EQUALS'
TT_EQ = 'EQ'
TT_NE = 'NE'
TT_LT = 'LT'
TT_GT = 'GT'
TT_LTE = 'LTE'
TT_GTE = 'GTE'

TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_LBRACKET = 'LBRACKET'
TT_RBRACKET = 'RBRACKET'
TT_COMMA = 'COMMA'
TT_COLON = 'COLON'
TT_DOT = 'DOT'

TT_NEWLINE = 'NEWLINE'
TT_INDENT = 'INDENT'
TT_DEDENT = 'DEDENT'
TT_EOF = 'EOF'


class Token:
    def __init__(self, type_, value=None, start_pos=None, end_pos=None):
        self.type = type_
        self.value = value
        self.start_pos = start_pos
        self.end_pos = end_pos

    def matches(self, type_, value=None):
        """Check if token matches given type and optionally value"""
        if value is not None:
            return self.type == type_ and self.value == value
        return self.type == type_

    def __repr__(self):
        if self.value is not None:
            if self.start_pos:
                return f'Token({self.type}, {repr(self.value)}, line {self.start_pos.line+1}, col {self.start_pos.column+1})'
            return f'Token({self.type}, {repr(self.value)})'
        else:
            if self.start_pos:
                return f'Token({self.type}, line {self.start_pos.line+1}, col {self.start_pos.column+1})'
            return f'Token({self.type})'

    def str(self):
        return self.__repr__()