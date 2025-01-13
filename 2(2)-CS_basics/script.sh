#!/bin/bash

# Exit on error
set -e

# Error handling function
error_exit() {
    echo "[ERROR] $1"
    exit 1
}

# Miniconda 설치 및 환경 설정
install_conda() {
    echo "Installing Miniconda..."
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh || error_exit "Failed to download Miniconda."
    bash ~/miniconda.sh -b -p "$HOME/miniconda" || error_exit "Failed to install Miniconda."
    export PATH="$HOME/miniconda/bin:$PATH"
    echo 'export PATH="$HOME/miniconda/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
}

check_conda() {
    if ! command -v conda &> /dev/null; then
        if [ -d "$HOME/miniconda" ]; then
            export PATH="$HOME/miniconda/bin:$PATH"
        else
            install_conda
        fi
    fi
}

initialize_conda() {
    if [ -f "$HOME/miniconda/etc/profile.d/conda.sh" ]; then
        source "$HOME/miniconda/etc/profile.d/conda.sh"
    else
        echo "Conda initialization script not found. Using PATH directly."
    fi
}

# Conda 환경 생성
setup_conda_env() {
    if ! conda env list | grep -q myenv; then
        echo "Creating Conda environment 'myenv'..."
        conda create -y -n myenv python=3.8 || error_exit "Failed to create Conda environment."
    else
        echo "Conda environment 'myenv' already exists."
    fi

    source activate myenv || error_exit "Failed to activate Conda environment."

    # ▼ 만약 오래된 mypy가 깔려있다면 업그레이드(또는 재설치) 권장
    pip install --upgrade mypy || error_exit "Failed to install/upgrade mypy."
}

# 디렉토리 설정
setup_directories() {
    mkdir -p submission input output
}

# ---------------------------------------------------
# 경고(오류) 없이 정상 실행된 스크립트를 저장할 배열
successful_scripts=()

# 파이썬 스크립트 실행
execute_scripts() {
    echo "Running Python scripts..."

    for file in submission/*.py; do
        filename=$(basename "$file" .py)
        input_file="input/${filename}_input"
        output_file="output/${filename}_output"

        echo "[INFO] Executing $filename"
        echo "[INFO] Generating output file: $output_file"
        touch "$output_file"

        # 입력 파일 체크
        if [[ ! -f "$input_file" ]]; then
            echo "[WARNING] Missing input file for $filename. Skipping."
            echo "No input file provided." > "$output_file"
            continue
        fi

        # 파이썬 파일 실행: 성공하면 successful_scripts 에 추가
        if python "$file" < "$input_file" > "$output_file" 2>&1; then
            successful_scripts+=("$file")
        else
            echo "[WARNING] Error occurred during $filename execution. Check $output_file for details."
        fi
    done
}

# ---------------------------------------------------
# mypy 테스트 (경고 없이 성공한 스크립트만 대상)
run_mypy_tests() {
    if [ ${#successful_scripts[@]} -eq 0 ]; then
        echo "[INFO] No successfully executed scripts found. Skipping mypy tests."
        return
    fi

    echo "Running mypy tests…"
    for file in "${successful_scripts[@]}"; do
        filename=$(basename "$file")
        echo "[INFO] Running mypy for $filename..."
        
        mypy "$file"
    done
}

# 메인 실행
main() {
    check_conda
    initialize_conda
    setup_conda_env
    setup_directories

    execute_scripts
    run_mypy_tests

    echo "All tasks completed."
}

main