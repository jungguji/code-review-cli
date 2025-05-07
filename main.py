from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
import subprocess
import os

# LLM 초기화 (예: Ollama 모델 사용)
llm = OllamaLLM(base_url='http://localhost:11434', model="qwen2.5-coder:3b")

# 현재 스크립트 위치를 기준으로 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
prompt_dir = os.path.join(current_dir, "prompt")  # prompt 폴더 경로

def load_prompt_template(file_name):
    """
    외부 파일에서 프롬프트 템플릿을 불러옵니다.
    """
    file_path = os.path.join(prompt_dir, file_name)  # prompt 폴더 안의 파일을 참조
    try:
        with open(file_path, 'r', encoding='utf-8') as file:  # UTF-8 인코딩 명시
            prompt_template = file.read()
        return prompt_template
    except FileNotFoundError:
        print(f"{file_path} 파일을 찾을 수 없습니다.")
        return None

def get_git_diff(branch_name):
    """
    입력된 브랜치와의 git diff 결과를 반환합니다.
    """
    try:
        result = subprocess.run(
            ["git", "diff", branch_name, "--unified=0"],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'  # UTF-8 인코딩 명시
        )
        return result.stdout
    except subprocess.CalledProcessError:
        print(f"브랜치 '{branch_name}'와의 차이를 가져오는 중 오류가 발생했습니다.")
        return None

def execute_agent(agent_name, prompt_text, diff_text):
    """
    각 에이전트가 자신의 역할을 수행하고 결과를 반환합니다.
    """
    print(f"\n===== {agent_name} 에이전트 실행 중 =====\n")

    # PromptTemplate과 LLM 연결
    prompt = PromptTemplate(input_variables=["diff_text"], template=prompt_text)
    
    chain = prompt | llm

    # 체인 실행
    response = chain.invoke({"diff_text": diff_text})
    print(response)
    print(f"\n===== {agent_name} 에이전트 실행 완료 =====\n")

    return response

def main():
    # 사용자에게 브랜치명 입력받기
    branch_name = input("비교할 브랜치명을 입력하세요: ")
    
    diff_text = get_git_diff(branch_name)
    if diff_text is None:
        print("git diff 결과를 가져오지 못했습니다.")
        return

    # 에이전트별 프롬프트 파일과 이름 설정
    agent_configs = [
        {"name": "Pre-condition Check Agent", "file_path": "pre-condition-checks.txt"},
        {"name": "Runtime Error Check Agent", "file_path": "runtime-error-checks.txt"},
        {"name": "Optimization Agent", "file_path": "optimization.txt"},
        {"name": "Security Issue Agent", "file_path": "security-issue.txt"}
    ]

    # 각 에이전트의 결과를 저장할 딕셔너리
    agent_results = {}

    # 각 에이전트를 실행하여 결과를 수집
    for config in agent_configs:
        prompt_text = load_prompt_template(config["file_path"])
        if prompt_text:
            # execute_agent 호출 시 diff_text를 전달하여 템플릿에서 동적으로 치환되도록 설정
            agent_results[config["name"]] = execute_agent(config["name"], prompt_text, diff_text)

    # 최종 리뷰 프롬프트를 외부 파일에서 불러오기

    # PromptTemplate 생성 및 템플릿 치환
    review_prompt_template = PromptTemplate(
        input_variables=["pre_condition", "runtime_error", "optimization", "security_issue", "diff_text"],
        template=load_prompt_template("code-review.txt")
    )

    # review_prompt_template을 사용하여 최종 리뷰 프롬프트 생성
    review_prompt = review_prompt_template.format(
        pre_condition=agent_results.get("Pre-condition Check Agent", "No data"),
        runtime_error=agent_results.get("Runtime Error Check Agent", "No data"),
        optimization=agent_results.get("Optimization Agent", "No data"),
        security_issue=agent_results.get("Security Issue Agent", "No data"),
        diff_text = diff_text
    )

    # Code-Review Agent 실행
    print("\n===== Code-Review Agent 실행 중 =====\n")
    code_review_response = llm.invoke(review_prompt)
    print("\n===== 최종 코드 리뷰 결과 =====\n")
    print(code_review_response)

if __name__ == "__main__":
    main()