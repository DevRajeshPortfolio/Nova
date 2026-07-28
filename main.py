# main.py
# Nova Programming Language - Entry Point

from lexer import Lexer
from parser import Parser
from compiler import Compiler
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <source.nova> [command]")
        print("Commands:")
        print("  tokenize  - Show tokens only")
        print("  parse     - Show AST only")
        print("  compile   - Full compilation (default)")
        return
    
    source_file = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else 'compile'
    
    # Read source
    with open(source_file, 'r', encoding='utf-8') as f:
        source = f.read()
    
    # Lex
    lexer = Lexer(source_file, source)
    tokens, error = lexer.make_tokens()
    
    if error:
        print(error.as_string())
        return
    
    if command == 'tokenize':
        # Print tokens
        for token in tokens:
            print(token)
        return
    
    # Parse
    parser = Parser(tokens)
    ast = parser.parse()
    
    if parser.errors:
        for err in parser.errors:
            print(f"Parse Error: {err}")
        return
    
    if command == 'parse':
        # Print AST
        print("AST:")
        for node in ast:
            print(f"  {node.node_type}: {vars(node)}")
        return
    
    # Compile
    compiler = Compiler()
    compiler.compile(source_file)


if __name__ == '__main__':
    main()

