# errors.py
class Error:
    def __init__(self, error_name, details, start_pos, end_pos):
        self.error_name = error_name
        self.details = details
        self.start_pos = start_pos
        self.end_pos = end_pos

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f'\nFile {self.start_pos.filename}, line {self.start_pos.line+1}, column {self.start_pos.column+1}'
        return result


class IllegalCharacterError(Error):
    def __init__(self, details, start_pos, end_pos):
        super().__init__('Illegal Character', details, start_pos, end_pos)


class ExpectedCharacterError(Error):
    def __init__(self, details, start_pos, end_pos):
        super().__init__('Expected Character', details, start_pos, end_pos)


class InvalidSyntaxError(Error):
    def __init__(self, details, start_pos, end_pos):
        super().__init__('Invalid Syntax', details, start_pos, end_pos)


class RuntimeError(Error):
    def __init__(self, details, start_pos, end_pos):
        super().__init__('Runtime Error', details, start_pos, end_pos)


class IndentationError(Error):
    def __init__(self, details, start_pos, end_pos):
        super().__init__('Indentation Error', details, start_pos, end_pos)


class UnexpectedTokenError(Error):
    def __init__(self, details, start_pos, end_pos):
        super().__init__('Unexpected Token', details, start_pos, end_pos)