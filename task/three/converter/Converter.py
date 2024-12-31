import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
import re


class KoreanMathConverter:
    def __init__(self):
        self.symbol_map = {
            # Basic operators
            'TIMES': r'\times',
            'over': r'\frac',
            'LEFT': r'\left',
            'RIGHT': r'\right',

            # Mathematical functions
            'P': r'\mathrm{P}',
            'C': r'\mathrm{C}',
            'lim': r'\lim',
            'sum': r'\sum',
            'int': r'\int',

            # Special symbols
            'SMALLINTER': r'\cap',
            '^{C}': r'^{\complement}',
            'infty': r'\infty',
            'sqrt': r'\sqrt',

            # Probability notation
            'cap': r'\cap',
            'cup': r'\cup',

            # Common subscripts
            '_n': r'_{n}',
            '_1': r'_{1}',
            '_2': r'_{2}'
        }

        # Inverse mapping for LaTeX to Korean conversion
        self.latex_to_korean_map = {v: k for k, v in self.symbol_map.items()}

    def parse_hwpx(self, file_path: str) -> List[str]:
        """Parse mathematical expressions from HWPX file."""
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract math zones from HWPX
        math_expressions = []
        for math_elem in root.findall(".//math"):
            expr = self._clean_math_text(math_elem.text)
            math_expressions.append(expr)

        return math_expressions

    def parse_hml(self, file_path: str) -> List[str]:
        """Parse mathematical expressions from HML file."""
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract math zones from HML
        math_expressions = []
        for math_elem in root.findall(".//hmath"):
            expr = self._clean_math_text(math_elem.text)
            math_expressions.append(expr)

        return math_expressions

    def _clean_math_text(self, text: str) -> str:
        """Clean and normalize mathematical text."""
        if not text:
            return ""

        # Remove unnecessary whitespace
        text = re.sub(r'\s+', ' ', text.strip())

        # Normalize brackets
        text = text.replace('（', '(').replace('）', ')')

        return text

    def korean_to_latex(self, expression: str) -> str:
        """Convert Korean mathematical expression to LaTeX."""
        # Parse the expression into tokens
        tokens = self._tokenize_expression(expression)
        latex_tokens = []

        i = 0
        while i < len(tokens):
            token = tokens[i]

            # Handle fractions
            if token == 'over':
                numerator = latex_tokens.pop()
                i += 1
                denominator = tokens[i]
                latex_tokens.append(f'\\frac{{{numerator}}}{{{denominator}}}')

            # Handle special functions
            elif token in self.symbol_map:
                latex_tokens.append(self.symbol_map[token])

            # Handle subscripts and superscripts
            elif token.startswith('_') or token.startswith('^'):
                prev_token = latex_tokens[-1] if latex_tokens else ''
                latex_tokens[-1] = f'{prev_token}{token}'

            # Handle regular tokens
            else:
                latex_tokens.append(token)

            i += 1

        return ''.join(latex_tokens)

    def latex_to_korean(self, latex: str) -> str:
        """Convert LaTeX expression to Korean mathematical expression."""
        korean_expr = latex

        # Replace LaTeX commands with Korean equivalents
        for latex_symbol, korean_symbol in self.latex_to_korean_map.items():
            korean_expr = korean_expr.replace(latex_symbol, korean_symbol)

        # Handle special cases
        korean_expr = self._handle_special_cases_latex_to_korean(korean_expr)

        return korean_expr

    def _tokenize_expression(self, expression: str) -> List[str]:
        """Tokenize mathematical expression."""
        tokens = []
        current_token = ''
        paren_count = 0

        for char in expression:
            if char == ' ' and paren_count == 0:
                if current_token:
                    tokens.append(current_token)
                    current_token = ''
            else:
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                current_token += char

        if current_token:
            tokens.append(current_token)

        return tokens

    def _handle_special_cases_latex_to_korean(self, expr: str) -> str:
        """Handle special cases when converting from LaTeX to Korean."""
        # Handle fraction special cases
        expr = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'\1 over \2', expr)

        # Handle probability notation
        expr = re.sub(r'\\mathrm\{P\}', 'P', expr)
        expr = re.sub(r'\\mathrm\{C\}', 'C', expr)

        return expr


def test_converter():
    """Test the converter with examples from the exam papers."""
    converter = KoreanMathConverter()

    # Test case 1: Complex fraction with combinations
    korean_expr1 = "rm {{1} over {3} TIMES {1} over {3}} over {{1} over {3} TIMES {1} over {3} + LEFT ( {2} over {3} TIMES _2C_1 TIMES _1C_1 RIGHT )}"
    latex1 = converter.korean_to_latex(korean_expr1)
    print(f"Test 1:\nInput: {korean_expr1}\nLaTeX: {latex1}\n")

    # Test case 2: Probability expression with complement
    korean_expr2 = "rm P LEFT ( A SMALLINTER B ^{C} RIGHT )"
    latex2 = converter.korean_to_latex(korean_expr2)
    print(f"Test 2:\nInput: {korean_expr2}\nLaTeX: {latex2}\n")


if __name__ == "__main__":
    test_converter()