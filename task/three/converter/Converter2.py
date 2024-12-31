import xml.etree.ElementTree as ET
import re
from typing import Dict, List, Tuple


class MathConverter:
    def __init__(self):
        # 기본 수식 기호 매핑
        self.symbol_map = {
            '×': r'\times',
            '÷': r'\div',
            '∩': r'\cap',
            '∪': r'\cup',
            '⊂': r'\subset',
            '⊃': r'\supset',
            '∈': r'\in',
            '∉': r'\notin',
            '≠': r'\neq',
            '≤': r'\leq',
            '≥': r'\geq',
            '±': r'\pm',
            '∓': r'\mp',
            '∞': r'\infty',
            '∴': r'\therefore',
            '∵': r'\because',
        }

        # 특수 수식 구조 패턴
        self.patterns = {
            'fraction': r'(\d+)\s*\/\s*(\d+)',
            'superscript': r'(\w+)\^(\w+)',
            'subscript': r'(\w+)_(\w+)',
            'root': r'√\{([^}]+)\}',
            'matrix': r'\[\[(.*?)\]\]',
            'combination': r'_(\d+)C_(\d+)',
            'sum': r'Σ_\{([^}]+)\}\^\{([^}]+)\}',
            'integral': r'∫_\{([^}]+)\}\^\{([^}]+)\}'
        }

    def parse_hangul_xml(self, xml_content: str) -> List[str]:
        """한글 XML에서 수식 추출"""
        try:
            root = ET.fromstring(xml_content)
            math_elements = root.findall(".//math")
            return [elem.text for elem in math_elements if elem.text]
        except ET.ParseError as e:
            print(f"XML 파싱 오류: {e}")
            return []

    def hangul_to_latex(self, math_expr: str) -> str:
        """한글 수식을 LaTeX로 변환"""
        result = math_expr

        # 기본 기호 변환
        for k, v in self.symbol_map.items():
            result = result.replace(k, v)

        # 특수 구조 변환
        result = re.sub(self.patterns['fraction'], r'\\frac{\1}{\2}', result)
        result = re.sub(self.patterns['superscript'], r'{\1}^{\2}', result)
        result = re.sub(self.patterns['subscript'], r'{\1}_{\2}', result)
        result = re.sub(self.patterns['root'], r'\\sqrt{\1}', result)
        result = re.sub(self.patterns['combination'], r'C_{\1}^{\2}', result)

        # 행렬 처리
        def matrix_to_latex(match):
            content = match.group(1)
            rows = content.split(';')
            matrix_content = r' \\ '.join([' & '.join(row.split()) for row in rows])
            return f"\\begin{{pmatrix}}{matrix_content}\\end{{pmatrix}}"

        result = re.sub(self.patterns['matrix'], matrix_to_latex, result)

        return result

    def latex_to_hangul(self, latex_expr: str) -> str:
        """LaTeX를 한글 수식으로 변환"""
        result = latex_expr

        # 역변환 맵 생성
        reverse_map = {v: k for k, v in self.symbol_map.items()}

        # 기본 기호 역변환
        for k, v in reverse_map.items():
            result = result.replace(k, v)

        # 특수 구조 역변환
        result = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'\1/\2', result)
        result = re.sub(r'\{([^}]+)\}\^([^}]+)', r'\1^\2', result)
        result = re.sub(r'\{([^}]+)\}_([^}]+)', r'\1_\2', result)
        result = re.sub(r'\\sqrt\{([^}]+)\}', r'√{\1}', result)

        # 행렬 역변환
        def latex_to_matrix(match):
            content = match.group(1)
            rows = content.split(r'\\')
            matrix_content = ';'.join([row.replace('&', ' ').strip() for row in rows])
            return f"[[{matrix_content}]]"

        result = re.sub(r'\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}', latex_to_matrix, result)

        return result


# 사용 예시
def main():
    converter = MathConverter()

    # 예제 1: 조합과 분수
    hangul_math = "₃C₁ × 1/3"
    latex = converter.hangul_to_latex(hangul_math)
    print(f"한글 수식: {hangul_math}")
    print(f"LaTeX 변환: {latex}")
    print(f"역변환: {converter.latex_to_hangul(latex)}\n")

    # 예제 2: 행렬
    hangul_math = "[[1 2; 3 4]]"
    latex = converter.hangul_to_latex(hangul_math)
    print(f"한글 수식: {hangul_math}")
    print(f"LaTeX 변환: {latex}")
    print(f"역변환: {converter.latex_to_hangul(latex)}")


if __name__ == "__main__":
    main()