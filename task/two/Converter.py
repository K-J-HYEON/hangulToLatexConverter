import re
from typing import List, Dict, Tuple


class AdvancedMathConverter:
    def __init__(self):
        self.math_symbols = {
            'sqrt': r'\sqrt',
            'lim': r'\lim',
            'frac': r'\frac',
            '->': r'\to',
            '^': r'^',
            '{': r'{',
            '}': r'}'
        }

    def _extract_sequence(self, text: str, start_pos: int) -> Tuple[str, int]:
        """수학 표현식에서 시퀀스를 추출하는 메서드"""
        brackets = {'{': '}', '(': ')', '[': ']'}
        stack = []
        sequence = ""
        i = start_pos

        while i < len(text):
            char = text[i]
            if char in brackets.keys():
                stack.append(char)
            elif char in brackets.values():
                if not stack:
                    break
                if char == brackets[stack[-1]]:
                    stack.pop()
                    if not stack:  # 모든 괄호가 닫힘
                        sequence += char
                        i += 1
                        break
            sequence += char
            i += 1

        return sequence, i

    def parse_mathematical_components(self, expression: str) -> List[str]:
        """수학 표현식을 구성 요소로 분해"""
        components = []
        i = 0
        current_component = ""

        while i < len(expression):
            if expression[i] in ['{', '(', '[']:
                seq, new_i = self._extract_sequence(expression, i)
                components.append(seq)
                i = new_i
            else:
                current_component += expression[i]
                i += 1

            if current_component.strip():
                components.append(current_component.strip())
                current_component = ""

        return components

    def korean_to_latex(self, expression: str) -> str:
        """한글 수식을 LaTeX로 변환"""
        components = self.parse_mathematical_components(expression)
        latex = ""

        for component in components:
            # 기본 수학 기호 변환
            for k, v in self.math_symbols.items():
                component = component.replace(k, v)

            # 특수 케이스 처리
            if component.startswith('sqrt'):
                component = self._handle_sqrt(component)
            elif component.startswith('lim'):
                component = self._handle_limit(component)
            elif component.startswith('frac'):
                component = self._handle_fraction(component)

            latex += component

        return latex

    def _handle_sqrt(self, component: str) -> str:
        """루트 표현식 처리"""
        return component.replace('sqrt', r'\sqrt')

    def _handle_limit(self, component: str) -> str:
        """극한 표현식 처리"""
        return component.replace('lim', r'\lim')

    def _handle_fraction(self, component: str) -> str:
        """분수 표현식 처리"""
        return component.replace('frac', r'\frac')


def test_converter():
    """변환기 테스트"""
    converter = AdvancedMathConverter()

    test_cases = [
        ("sqrt{5}*2^3", r"\sqrt{5}*2^3"),
        ("lim_{h->0} frac{f(2+h)-f(2)}{h}", r"\lim_{h\to 0} \frac{f(2+h)-f(2)}{h}")
    ]

    print("Testing Korean to LaTeX conversion:")
    for expr, expected in test_cases:
        print(f"\nInput: {expr}")
        latex = converter.korean_to_latex(expr)
        print(f"LaTeX: {latex}")
        print(f"Correct: {'Yes' if latex == expected else 'No'}")


if __name__ == "__main__":
    test_converter()