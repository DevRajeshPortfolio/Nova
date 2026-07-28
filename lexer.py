# lexer.py
# Nova Programming Language - Lexer

from tokens import *
from keywords import KEYWORDS
from errors import *
from position import Position


class Lexer:
    def __init__(self, filename, source):
        self.filename = filename
        self.source = source
        self.pos = Position(-1, 0, -1, filename)
        self.current_char = None
        self.tokens = []
        self.advance()
        
        # Indentation tracking
        self.indent_stack = [0]
        self.pending_indents = 0
        self.in_indent_region = False
    
    def advance(self):
        """Advance to next character"""
        self.pos.advance(self.current_char)
        if self.pos.index < len(self.source):
            self.current_char = self.source[self.pos.index]
        else:
            self.current_char = None
    
    def peek(self, offset=1):
        """Look ahead without advancing"""
        idx = self.pos.index + offset
        if idx < len(self.source):
            return self.source[idx]
        return None
    
    def make_tokens(self):
        """Main tokenization method with indentation support"""
        while self.current_char is not None:
            start = self.pos.copy()
            
            if self.current_char == ' ' or self.current_char == '\t':
                self.handle_whitespace()
            elif self.current_char == '#':
                self.skip_comment()
            elif self.current_char >= '0' and self.current_char <= '9':
                self.make_number()
            elif self.current_char == '"':
                self.make_string()
            elif self.current_char.isalpha() or self.current_char == '_':
                self.make_identifier()
            elif self.current_char == '+':
                self.add_token(TT_PLUS, start)
                self.advance()
            elif self.current_char == '-':
                self.add_token(TT_MINUS, start)
                self.advance()
            elif self.current_char == '*':
                self.add_token(TT_MUL, start)
                self.advance()
            elif self.current_char == '/':
                self.add_token(TT_DIV, start)
                self.advance()
            elif self.current_char == '%':
                self.add_token(TT_MOD, start)
                self.advance()
            elif self.current_char == '=':
                self.make_equals(start)
            elif self.current_char == '!':
                self.make_not_equals(start)
            elif self.current_char == '<':
                self.make_less_than(start)
            elif self.current_char == '>':
                self.make_greater_than(start)
            elif self.current_char == '(':
                self.add_token(TT_LPAREN, start)
                self.advance()
            elif self.current_char == ')':
                self.add_token(TT_RPAREN, start)
                self.advance()
            elif self.current_char == '[':
                self.add_token(TT_LBRACKET, start)
                self.advance()
            elif self.current_char == ']':
                self.add_token(TT_RBRACKET, start)
                self.advance()
            elif self.current_char == ',':
                self.add_token(TT_COMMA, start)
                self.advance()
            elif self.current_char == ':':
                self.add_token(TT_COLON, start)
                self.advance()
            elif self.current_char == '.':
                self.add_token(TT_DOT, start)
                self.advance()
            elif self.current_char == '\n':
                self.handle_newline(start)
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharacterError(
                    f"'{char}' is not a valid character",
                    pos_start,
                    self.pos
                )
        
        self.handle_end_of_file()
        return self.tokens, None
    
    def handle_whitespace(self):
        """Handle spaces and tabs (only used for indentation)"""
        indent_count = 0
        
        while self.current_char is not None and (self.current_char == ' ' or self.current_char == '\t'):
            if self.current_char == ' ':
                indent_count += 1
            else:  # tab
                indent_count += 4
            self.advance()
        
        # Store indentation for later processing
        self.pending_indents = indent_count
        self.in_indent_region = True
    
    def handle_newline(self, start):
        """Handle newline and potential indentation"""
        # First, process any pending indentation from previous line
        if self.in_indent_region:
            current_indent = self.pending_indents
            
            if current_indent > self.indent_stack[-1]:
                # Increased indentation
                self.indent_stack.append(current_indent)
                self.add_token(TT_INDENT, self.pos)
            elif current_indent < self.indent_stack[-1]:
                # Decreased indentation - may need multiple dedents
                while current_indent < self.indent_stack[-1]:
                    self.indent_stack.pop()
                    self.add_token(TT_DEDENT, self.pos)
                
                if current_indent != self.indent_stack[-1]:
                    # Invalid indentation
                    pass
            
            self.in_indent_region = False
        
        # Add the newline token
        self.add_token(TT_NEWLINE, start)
        self.advance()
    
    def handle_end_of_file(self):
        """Handle end of file with dedents"""
        # Add dedents to close all open indents
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            start = self.pos.copy()
            self.add_token(TT_DEDENT, start)
        
        # Add EOF
        start = self.pos.copy()
        self.add_token(TT_EOF, start)
    
    def add_token(self, type_, start_pos, value=None):
        """Add a token to the token list"""
        end = self.pos.copy()
        self.tokens.append(Token(type_, value, start_pos, end))
    
    def make_number(self):
        """Parse integer or float"""
        start = self.pos.copy()
        num_str = ''
        
        while self.current_char is not None and self.current_char >= '0' and self.current_char <= '9':
            num_str += self.current_char
            self.advance()
        
        if self.current_char == '.':
            num_str += self.current_char
            self.advance()
            
            while self.current_char is not None and self.current_char >= '0' and self.current_char <= '9':
                num_str += self.current_char
                self.advance()
            
            self.add_token(TT_FLOAT, start, float(num_str))
        else:
            self.add_token(TT_INT, start, int(num_str))
    
    def make_string(self):
        """Parse string with escape sequences"""
        start = self.pos.copy()
        self.advance()  # Skip opening quote
        string = ''
        escape_char = False
        
        while self.current_char is not None:
            if escape_char:
                if self.current_char == 'n':
                    string += '\n'
                elif self.current_char == 't':
                    string += '\t'
                elif self.current_char == '\\':
                    string += '\\'
                elif self.current_char == '"':
                    string += '"'
                else:
                    string += self.current_char
                escape_char = False
            elif self.current_char == '\\':
                escape_char = True
            elif self.current_char == '"':
                self.advance()  # Skip closing quote
                self.add_token(TT_STRING, start, string)
                return
            else:
                string += self.current_char
            self.advance()
        
        # Unterminated string
        self.add_token(TT_STRING, start, string)
    
    def make_identifier(self):
        """Parse identifier or keyword"""
        start = self.pos.copy()
        id_str = ''
        
        while self.current_char is not None and (self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        
        if id_str in KEYWORDS:
            self.add_token(TT_KEYWORD, start, id_str)
        else:
            self.add_token(TT_IDENTIFIER, start, id_str)
    
    def make_equals(self, start):
        """Parse = or =="""
        self.advance()
        if self.current_char == '=':
            self.advance()
            self.add_token(TT_EQ, start)
        else:
            self.add_token(TT_EQUALS, start)
    
    def make_not_equals(self, start):
        """Parse !="""
        self.advance()
        if self.current_char == '=':
            self.advance()
            self.add_token(TT_NE, start)
        else:
            return [], ExpectedCharacterError(
                "Expected '=' after '!'",
                start,
                self.pos
            )
    
    def make_less_than(self, start):
        """Parse < or <="""
        self.advance()
        if self.current_char == '=':
            self.advance()
            self.add_token(TT_LTE, start)
        else:
            self.add_token(TT_LT, start)
    
    def make_greater_than(self, start):
        """Parse > or >="""
        self.advance()
        if self.current_char == '=':
            self.advance()
            self.add_token(TT_GTE, start)
        else:
            self.add_token(TT_GT, start)
    
    def skip_comment(self):
        """Skip single-line comments"""
        self.advance()
        while self.current_char is not None and self.current_char != '\n':
            self.advance()