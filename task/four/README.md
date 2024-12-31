# four
기본 구조
- MathFormulaConverter 클래스를 통해 한글 수식과 LaTeX 수식 간의 변환을 처리
- 각종 수학 기호, 함수, 괄호에 대한 매핑 테이블 포함


주요 기능
- convert_korean_to_latex(): 한글 수식을 LaTeX로 변환
- convert_latex_to_korean(): LaTeX 수식을 한글로 변환
- 전처리 함수들을 통한 입력 정규화


특별 처리
- 분수 표현 변환 (a/b ↔ \frac{a}{b})
- 첨자 처리 (x1 ↔ x_1)
- 제곱 처리 (x^2 ↔ x^{2})
- 괄호 처리 (( ↔ \left()


확장성
- 새로운 수학 기호나 함수를 쉽게 추가할 수 있는 구조
- 매핑 테이블을 통한 유지보수 용이성

## Code 설명
```
def __init__(self):
    # 기본 수학 기호 매핑
    self.korean_to_latex_map = {
        '≤': r'\leq',
        '≥': r'\geq',
        # ... 추가 기호들
    }
```

- 한글과 LaTeX 수학 표기법 간의 변환을 위한 매핑 테이블 생성
- LaTeX 백슬래시를 올바르게 처리하기 위해 raw 문자열 사용
- 일반적인 수학 기호, 연산자, 관계 기호 포함
- 함수 매핑


##
```
self.function_map = {
    'sin': r'\sin',
    'cos': r'\cos',
    # ... 추가 함수들
}
```
- 수학 함수들을 처리
- 함수의 올바른 LaTeX 형식을 보장 (예: 단순 sin이 아닌 \sin 사용)
- 일관된 간격과 형식 유지
- 괄호 매핑


##
```
self.bracket_map = {
    '(': r'\left(',
    ')': r'\right(',
    # ... 추가 괄호들
}
```
- 다양한 유형의 괄호와 괄호쌍 관리
- 적절한 LaTeX 크기 조정을 위해 \left와 \right 사용
- 출력에서 괄호의 균형 보장
- 전처리 메서드


##


```
def preprocess_korean_formula(self, formula: str) -> str:
    # 공백 정리
    formula = re.sub(r'\s+', ' ', formula.strip())
    
    # 분수 처리
    formula = re.sub(r'(\d+)/(\d+)', r'\\frac{\1}{\2}', formula)
    
    return formula
```
- 입력 수식 정리 및 정규화
- 분수와 같은 특수 케이스 처리
- 불필요한 공백 제거
- 패턴 매칭을 위한 정규 표현식 사용
- 핵심 변환 메서드



##
```
def convert_korean_to_latex(self, formula: str) -> str:
    formula = self.preprocess_korean_formula(formula)
    
    # 기호 변환
    for k, v in self.korean_to_latex_map.items():
        formula = formula.replace(k, v)
    
    # 함수 변환
    for k, v in self.function_map.items():
        formula = re.sub(rf'\b{k}\b', v, formula)
    
    # 추가 변환...
    return formula
```
- 주요 기능:
- 수식 구성 요소의 순차적 처리
- 복잡한 치환을 위한 패턴 매칭
- 특수 케이스의 적절한 처리
- 특수 패턴 처리

##
```
# 첨자 처리
formula = re.sub(r'([a-zA-Z])(\d+)', r'\1_{\2}', formula)

# 제곱 처리
formula = re.sub(r'\^(\d+)', r'^{\1}', formula)
```
- 첨자 처리 (예: x1 → x_1)
- 지수 처리 (예: x^2 → x^{2})
- 복잡한 패턴 매칭을 위한 정규 표현식 사용
- 역변환

##

```
def convert_latex_to_korean(self, formula: str) -> str:
    formula = self.preprocess_latex_formula(formula)
    
    # 역매핑 생성
    latex_to_korean_map = {v: k for k, v in self.korean_to_latex_map.items()}
    
    # 한글로 다시 변환
    for k, v in latex_to_korean_map.items():
        formula = formula.replace(k, v)
    
    # 추가 역변환...
    return formula
```
- LaTeX에서 한글 표기법으로의 변환 처리
- 기호와 함수를 위한 역매핑 사용
- 변환 과정에서 수학적 의미 보존

##

```
converter = MathFormulaConverter()

# 한글에서 LaTeX로
korean_formula = "x^2 + 2x + 1 ≤ 0"
latex_result = converter.convert_korean_to_latex(korean_formula)
# 결과: x^{2} + 2x + 1 \leq 0

# LaTeX에서 한글로
korean_result = converter.convert_latex_to_korean(latex_result)
# 결과: x^2 + 2x + 1 ≤ 0
```
- 추가로 고려할 수 있는 기능들:
- 잘못된 입력에 대한 오류 처리
- 더 복잡한 수학 구조 지원
- 행렬 표기법 처리
- 적분과 미분 기호 지원
- 특정 사용 사례를 위한 사용자 정의 기호 매핑