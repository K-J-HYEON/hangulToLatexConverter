import re
from typing import Dict, List, Tuple

class MathFormulaConverter:
    def __init__(self):
        # 기본 수학 기호 매핑
        self.korean_to_latex_map = {
            '≤': r'\leq',
            '≥': r'\geq',
            '×': r'\times',
            '÷': r'\div',
            '±': r'\pm',
            '∓': r'\mp',
            '→': r'\rightarrow',
            '←': r'\leftarrow',
            '↔': r'\leftrightarrow',
            '∴': r'\therefore',
            '∵': r'\because',
            '∞': r'\infty',
            '≠': r'\neq',
            '≈': r'\approx',
            '∀': r'\forall',
            '∃': r'\exists',
            '∄': r'\nexists',
            '∈': r'\in',
            '∉': r'\notin',
            '⊂': r'\subset',
            '⊃': r'\supset',
            '⊆': r'\subseteq',
            '⊇': r'\supseteq',
            '∪': r'\cup',
            '∩': r'\cap',
            '∅': r'\emptyset'
        }

        # 함수 매핑
        self.function_map = {
            'sin': r'\sin',
            'cos': r'\cos',
            'tan': r'\tan',
            'log': r'\log',
            'ln': r'\ln',
            'lim': r'\lim',
            'max': r'\max',
            'min': r'\min'
        }

        # 괄호 매핑
        self.bracket_map = {
            '(': r'\left(',
            ')': r'\right)',
            '[': r'\left[',
            ']': r'\right]',
            '{': r'\left\{',
            '}': r'\right\}'
        }

    def preprocess_korean_formula(self, formula: str) -> str:
        """한글 수식 전처리"""
        # 불필요한 공백 제거
        formula = re.sub(r'\s+', ' ', formula.strip())

        # 분수 표현 정규화
        formula = re.sub(r'(\d+)/(\d+)', r'\\frac{\1}{\2}', formula)

        return formula

    def convert_korean_to_latex(self, formula: str) -> str:
        """한글 수식을 LaTeX로 변환"""
        formula = self.preprocess_korean_formula(formula)

        # 기본 수학 기호 변환
        for k, v in self.korean_to_latex_map.items():
            formula = formula.replace(k, v)

        # 함수 변환
        for k, v in self.function_map.items():
            formula = re.sub(r'\b' + re.escape(k) + r'\b', v, formula)

        # 괄호 변환
        for k, v in self.bracket_map.items():
            formula = formula.replace(k, v)

        # 첨자 처리
        formula = re.sub(r'([a-zA-Z])(\d+)', r'\1_{\2}', formula)

        # 제곱 처리
        formula = re.sub(r'\^(\d+)', r'^{\1}', formula)

        return formula

    def preprocess_latex_formula(self, formula: str) -> str:
        """LaTeX 수식 전처리"""
        # LaTeX 명령어 정규화
        formula = formula.replace('\\left', '').replace('\\right', '')
        formula = re.sub(r'\s+', ' ', formula.strip())
        return formula

    def convert_latex_to_korean(self, formula: str) -> str:
        """LaTeX 수식을 한글로 변환"""
        formula = self.preprocess_latex_formula(formula)

        # LaTeX를 한글로 변환하기 위한 역매핑 생성
        latex_to_korean_map = {v: k for k, v in self.korean_to_latex_map.items()}

        # 기본 수학 기호 변환
        for k, v in latex_to_korean_map.items():
            formula = formula.replace(k, v)

        # 함수 변환
        latex_to_function_map = {v: k for k, v in self.function_map.items()}
        for k, v in latex_to_function_map.items():
            formula = formula.replace(k, v)

        # 분수 변환
        formula = re.sub(r'\\frac\{(\d+)\}\{(\d+)\}', r'\1/\2', formula)

        # 첨자 변환
        formula = re.sub(r'_\{(\d+)\}', r'\1', formula)

        # 제곱 변환
        formula = re.sub(r'\^\{(\d+)\}', r'^{\1}', formula)

        return formula


def test_converter():
    """변환기 테스트 함수"""
    converter = MathFormulaConverter()

    # 테스트 케이스
    test_cases = [
        ("x^2 + 2x + 1 ≤ 0", r"x^{2} + 2x + 1 \leq 0"),
        ("sin(x)/cos(x) = tan(x)", r"\sin\left(x\right)/\cos\left(x\right) = \tan\left(x\right)"),
        ("∀x∈R, |x| ≥ 0", r"\forall x\in\mathbb{R}, |x| \geq 0")
    ]

    print("테스트 시작...")
    for korean, expected_latex in test_cases:
        result = converter.convert_korean_to_latex(korean)
        print(f"\n입력: {korean}")
        print(f"변환 결과: {result}")
        print(f"기대 결과: {expected_latex}")
        print(f"테스트 {'성공' if result == expected_latex else '실패'}")

        # 역변환 테스트
        reverse = converter.convert_latex_to_korean(result)
        print(f"역변환 결과: {reverse}")