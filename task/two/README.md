## two - README.md

## 고급 수식 처리:
- 극한(limit) 표현식
- 제곱근(sqrt) 표현식
- 수열(sequence) 표기법
- 조각함수(piecewise function) 처리


## 개선된 파싱 기능:
- 중첩된 수식 구조 처리
- 복잡한 함수 표현식 지원
- 수학 기호와 특수 문자 확장

## 특수 기능
- 수열 표기법 자동 변환
- 함수 표현식 자동 변환
- 복잡한 수식 구조 보존


## 유연한 확장성
- 새로운 수학 기호 쉽게 추가 가능
- 다양한 수식 패턴 처리 가능
- 시험지의 수식들을 다음과 같이 변환 가능


```
# 첫 번째 문제의 수식
korean = "sqrt{5}*2^3"
latex = r"\sqrt{5} \times 2^3"

# 두 번째 문제의 함수 극한
korean = "lim_{h->0} (f(2+h)-f(2))/h"
latex = r"\lim_{h \to 0} \frac{f(2+h)-f(2)}{h}"
```

### extract_sequence 에러 처리
- _extract_sequence 메서드를 추가하여 중첩된 괄호를 올바르게 처리
- parse_mathematical_components 메서드를 개선하여 수식 구성 요소를 정확하게 분리
- 각각의 수학 표현식 처리를 위한 전용 메서드 추가 (_handle_sqrt, _handle_limit, _handle_fraction)
- 기본 수학 기호 매핑 테이블 개선