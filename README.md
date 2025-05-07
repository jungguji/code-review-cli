# AI 기반 자동 코드 리뷰어

**AI 기반 자동 코드 리뷰어**는 `git diff`를 활용하여 코드 변경 사항을 분석하고, 다양한 관점에서 자동화된 코드 리뷰를 제공하여 개발 생산성 향상과 코드 품질 개선을 목표로 하는 도구입니다.

## ✨ 주요 기능

-   **Git Diff 기반 분석**: `git diff` 명령어를 통해 두 브랜치 또는 커밋 간의 코드 변경 사항을 추출하여 분석합니다.
-   **다각도 코드 검토**: LLM (Large Language Model)을 활용하여 다음과 같은 주요 항목에 대해 심층적인 코드 리뷰를 수행합니다.
    -   **사전 조건 검사 (Pre-condition Check)**: 함수 및 메서드가 올바르게 동작하기 위해 필요한 변수의 초기 상태, 값의 범위 등을 확인합니다.
    -   **런타임 오류 가능성 검토 (Runtime Error Check)**: 실행 중 발생할 수 있는 잠재적 오류(Null 참조, 타입 불일치, 배열 범위 초과 등)를 예측하고 검토합니다.
    -   **최적화 방안 제시 (Optimization Check)**: 코드의 효율성(실행 속도, 메모리 사용량)을 분석하고 개선 가능한 부분을 제안합니다.
    -   **보안 취약점 점검 (Security Issue Check)**: 일반적인 보안 취약점(SQL Injection, XSS, 데이터 노출 등)이 코드에 포함되어 있는지 검사합니다.
-   **종합 리뷰 제공**: 각 항목별 분석 결과를 종합하여 코드 변경사항에 대한 최종적이고 포괄적인 리뷰를 생성합니다.

## 🚀 시작하기

### 사전 준비물

-   **Ollama**: 로컬 환경에서 LLM을 실행하기 위한 플랫폼입니다.
    -   [Ollama 공식 웹사이트](https://ollama.com/)에서 설치 가이드를 참고하세요.
    -   **macOS (Homebrew 사용 시)**:
        ```bash
        # Homebrew 저장소 업데이트
        brew update
        # Ollama tap 저장소 추가 (기본 저장소에 없을 경우)
        brew tap ollama/tap
        # Ollama 설치
        brew install ollama
        # 설치 확인
        ollama --version
        ```
-   **LLM 모델**: Ollama를 통해 실행할 LLM 모델이 필요합니다.
    -   본 프로젝트는 기본적으로 [qwen2.5-coder](https://ollama.com/library/qwen2.5-coder) 모델을 사용하도록 설정되어 있습니다. ([모델 상세 정보](https://qwenlm.github.io/blog/qwen2.5-coder/))
    -   다른 모델을 사용하고자 할 경우, `main.py` 파일 내의 모델 설정을 변경할 수 있습니다.
    -   모델 설치 (예: qwen2.5-coder):
        ```bash
        ollama run qwen2.5-coder
        ```
-   **Python**: Python 3.x 버전이 필요합니다.
    -   프로젝트에 필요한 라이브러리는 `requirements.txt` 파일에 명시되어 있습니다.
-   **Langchain**: LLM과의 상호작용을 위한 프레임워크입니다. (`requirements.txt`를 통해 설치됩니다.)

### 설치 및 실행

1.  이 저장소를 클론합니다:
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```
2.  필요한 Python 라이브러리를 `requirements.txt`를 사용하여 설치합니다:
    ```bash
    pip install -r requirements.txt
    ```
3.  Ollama 서버가 실행 중인지 확인합니다.
4.  애플리케이션을 실행합니다:
    ```bash
    python main.py
    ```
    실행 후, 비교할 브랜치명을 입력하라는 메시지가 나타납니다.

## 🛠️ 사용 방법

스크립트를 실행하면 비교 대상 브랜치명을 입력하라는 프롬프트가 표시됩니다. 브랜치명을 입력하면, 현재 브랜치와 입력한 브랜치 간의 `git diff` 결과를 바탕으로 코드 리뷰가 진행됩니다. 각 에이전트(Pre-condition, Runtime Error, Optimization, Security, Code-Review)가 순차적으로 실행되며, 최종적으로 종합된 코드 리뷰 결과가 터미널에 출력됩니다.

## ⚠️ 한계점 및 고려사항

-   **프롬프트 엔지니어링 의존성**: LLM의 응답 품질은 프롬프트의 구성에 크게 영향을 받습니다. 프롬프트 수정 및 개선을 통해 결과의 정확도를 높일 수 있습니다.
-   **Diff 크기의 영향**: 비교하는 코드 변경 사항의 양이 많을수록 LLM의 분석 정확도가 저하될 수 있습니다.
    -   작은 단위로 자주 커밋하고 Pull Request를 생성하는 개발 문화/정책이 도움이 될 수 있습니다.
-   **브랜치 간 누적 차이**: `git diff`는 두 브랜치 간의 전체 차이를 비교합니다. 따라서 특정 PR의 변경 사항이 적더라도, 베이스 브랜치와 피처 브랜치 간에 누적된 변경 사항이 많으면 분석의 초점이 분산될 수 있습니다.
    -   예: `develop` 브랜치에만 존재하는 개발용 코드가 있고, `master`에서 분기한 `feature` 브랜치와 `develop` 브랜치를 비교할 경우, 의도치 않은 많은 차이점이 분석 대상에 포함될 수 있습니다.
-   **로컬 모델의 성능 제약**: 로컬 환경에서 사용하기 위해 경량화된 LLM 모델을 사용할 경우, 더 크고 강력한 상용 모델에 비해 분석의 깊이나 정확성에 한계가 있을 수 있습니다.
    -   보안 및 비용 문제가 해결된다면, 고성능 API 기반 모델을 활용하는 것을 고려할 수 있습니다.

## 📚 참고 자료

-   [시간은 금이다: LLM을 이용한 AI 코드 리뷰 도입기 (YouTube)](https://www.youtube.com/watch?v=7cwFhX14nkg)
-   [[우아한테크세미나] 생성AI로 똑똑하게 일하는 법 (YouTube)](https://www.youtube.com/watch?v=v2icwh-nyl4)