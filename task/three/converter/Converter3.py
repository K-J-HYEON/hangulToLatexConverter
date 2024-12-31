import re
from typing import Dict, List, Optional


class MathConverter:
    def __init__(self):
        # 기본 변환 규칙 정의
        self.hangul_to_latex_rules = {
            'TIMES': r'\times',
            'over': r'\frac',
            'LEFT': r'\left',
            'RIGHT': r'\right',
            'SMALLINTER': r'\cap',
            r'\(': '{',
            r'\)': '}',
            'rm': '',
            'C': r'C'
        }

        self.latex_to_hangul_rules = {v: k for k, v in self.hangul_to_latex_rules.items()}

    def parse_hangul_xml(self, xml_content: str) -> List[str]:
        """한글 XML에서 수식 추출"""
        # 정규표현식을 사용하여 수식 부분 추출
        math_patterns = re.findall(r'\[(한글수식)\](.*?)\[/한글수식\]', xml_content, re.DOTALL)
        return [math[1].strip() for math in math_patterns]

    def hangul_to_latex(self, hangul_math: str) -> str:
        """한글 수식을 Latex로 변환"""
        latex = hangul_math

        # 분수 처리
        fraction_pattern = r'(\w+)\s+over\s+(\w+)'
        while re.search(fraction_pattern, latex):
            latex = re.sub(fraction_pattern, r'\\frac{\1}{\2}', latex)

        # 기본 변환 규칙 적용
        for hangul, latex_sym in self.hangul_to_latex_rules.items():
            latex = latex.replace(hangul, latex_sym)

        # 공백 정리
        latex = re.sub(r'\s+', ' ', latex).strip()

        return latex

    def latex_to_hangul(self, latex: str) -> str:
        """Latex를 한글 수식으로 변환"""
        hangul = latex

        # 분수 처리
        frac_pattern = r'\\frac\{(.*?)\}\{(.*?)\}'
        while re.search(frac_pattern, hangul):
            hangul = re.sub(frac_pattern, r'\1 over \2', hangul)

        # 기본 변환 규칙 적용
        for latex_sym, hangul_sym in self.latex_to_hangul_rules.items():
            hangul = hangul.replace(latex_sym, hangul_sym)

        # 공백 정리
        hangul = re.sub(r'\s+', ' ', hangul).strip()

        return hangul

    def validate_conversion(self, original: str, converted: str, reverse_converted: str) -> bool:
        """변환 결과 검증"""
        # 공백과 불필요한 문자 제거 후 비교
        clean = lambda s: re.sub(r'[\s\{\}]', '', s)
        return clean(original) == clean(reverse_converted)


# 사용 예시
def main():
    converter = MathConverter()

    # 예제 1: 첫 번째 수식
    hangul_math1 = "rm {(1) over (3) TIMES (1) over (3)} over {(1) over (3) TIMES ((2) over (3) C_(1) TIMES C_(1)) over (_3C_2)} = (1) over (5)"
    latex1 = converter.hangul_to_latex(hangul_math1)
    hangul_back1 = converter.latex_to_hangul(latex1)

    print("Example 1:")
    print(f"Original: {hangul_math1}")
    print(f"Latex: {latex1}")
    print(f"Back to Hangul: {hangul_back1}")
    print(f"Validation: {converter.validate_conversion(hangul_math1, latex1, hangul_back1)}\n")

    # 예제 2: 두 번째 수식
    hangul_math2 = "rm P LEFT (A SMALLINTER B^C) RIGHT = rm P LEFT (A RIGHT) rm P LEFT (B^C) RIGHT = rm P LEFT (A RIGHT) TIMES (3) over (8) = (1) over (8)"
    latex2 = converter.hangul_to_latex(hangul_math2)
    hangul_back2 = converter.latex_to_hangul(latex2)

    print("Example 2:")
    print(f"Original: {hangul_math2}")
    print(f"Latex: {latex2}")
    print(f"Back to Hangul: {hangul_back2}")
    print(f"Validation: {converter.validate_conversion(hangul_math2, latex2, hangul_back2)}")


if __name__ == "__main__":
    main()