import re
from typing import Dict, List, Optional


class MathExpressionConverter:
    def __init__(self):
        self.korean_to_latex_map = {
            # Basic operators
            'TIMES': r'\times',
            'over': r'\frac',
            'LEFT': r'\left',
            'RIGHT': r'\right',

            # Special symbols
            'SMALLINTER': r'\cap',
            '^{C}': r'^{\complement}',

            # Function names
            'P': r'\mathrm{P}',
            'C': r'\mathrm{C}',
        }

        self.latex_to_korean_map = {v: k for k, v in self.korean_to_latex_map.items()}

    def parse_korean_expression(self, expression: str) -> List[str]:
        """Parse Korean mathematical expression into tokens."""
        # Remove 'rm' prefix if exists
        expression = expression.replace('rm ', '')

        # Split by spaces but keep parentheses together
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

    def korean_to_latex(self, expression: str) -> str:
        """Convert Korean mathematical expression to LaTeX."""
        tokens = self.parse_korean_expression(expression)
        latex_tokens = []

        i = 0
        while i < len(tokens):
            token = tokens[i]

            # Handle fractions
            if token == 'over':
                # Extract numerator and denominator
                numerator = latex_tokens.pop()
                i += 1
                denominator = tokens[i]
                latex_tokens.append(f'\\frac{{{numerator}}}{{{denominator}}}')

            # Handle special functions and symbols
            elif token in self.korean_to_latex_map:
                latex_tokens.append(self.korean_to_latex_map[token])

            # Handle regular tokens
            else:
                latex_tokens.append(token)

            i += 1

        return ''.join(latex_tokens)

    def latex_to_korean(self, expression: str) -> str:
        """Convert LaTeX expression to Korean mathematical expression."""
        # This is a simplified version - would need more complex parsing for complete conversion
        korean_expr = expression

        for latex_symbol, korean_symbol in self.latex_to_korean_map.items():
            korean_expr = korean_expr.replace(latex_symbol, korean_symbol)

        return korean_expr


def test_converter():
    """Test the converter with the provided examples."""
    converter = MathExpressionConverter()

    # Test Case 1
    korean_expr1 = "rm {1} over {3} TIMES {1} over {3}} over {{1} over {3} TIMES {1} over {3} + LEFT ( {2} over {3} TIMES _2C_1 TIMES _1C_1 RIGHT )} = {1} over {5}"
    latex_result1 = converter.korean_to_latex(korean_expr1)
    print("Test Case 1:")
    print(f"Input: {korean_expr1}")
    print(f"Output: {latex_result1}\n")

    # Test Case 2
    korean_expr2 = "rm P LEFT ( A SMALLINTER B ^{C} RIGHT ) = rm P LEFT ( A RIGHT ) rm P LEFT ( B ^{C} RIGHT ) = rm P LEFT ( A RIGHT ) TIMES {3} over {8} = {1} over {8}"
    latex_result2 = converter.korean_to_latex(korean_expr2)
    print("Test Case 2:")
    print(f"Input: {korean_expr2}")
    print(f"Output: {latex_result2}")


if __name__ == "__main__":
    test_converter()