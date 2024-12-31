## one - README.md
## 기본 구조:
- MathExpressionConverter 클래스를 통해 변환 로직을 캡슐화
- 한글->LaTeX, LaTeX->한글 양방향 변환 지원
- 수학 기호와 연산자에 대한 매핑 테이블 구현


## 주요 기능 :
- parse_korean_expression(): 한글 수식을 토큰으로 분리
- korean_to_latex(): 한글 수식을 LaTeX로 변환
- latex_to_korean(): LaTeX를 한글 수식으로 변환
- 분수, 특수 함수, 수학 기호 등 처리



## 툭징
- 괄호 처리를 위한 상태 추적
- 분수 표현을 위한 특별 처리
- 테스트 케이스 포함

### 향상될 수 있는 부분들
- XML 파싱 기능 추가
- 더 복잡한 수식 구조 지원
- 에러 처리 강화
- 더 많은 수학 기호 지원