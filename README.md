# Claude Code Session Automation

Claude Code rate limit 회피를 위한 자동 세션 시작 도구

## 설치

### Homebrew를 통한 설치 (권장)
```bash
brew tap weakness/tap
brew install claude-code-automation
```

### 소스에서 설치
```bash
git clone https://github.com/weakness/claude-code-automation.git
cd claude-code-automation
pip install -e .
```

## 사용법

### 스케줄 설정
```bash
# 매일 오전 6시에 세션 시작하도록 설정
claude-code-automation schedule 06:00

# 여러 시간 설정
claude-code-automation schedule 06:00 11:00 16:00

# 24시간 형식 사용 (예: 오후 2시 30분)
claude-code-automation schedule 14:30
```

### 수동 실행
```bash
claude-code-automation start
```

### 스케줄 관리
```bash
# 현재 스케줄 확인
claude-code-automation list

# 모든 스케줄 삭제
claude-code-automation clear
```

## 동작 원리

- 지정된 시간에 cron을 통해 `claude-code-automation start` 명령이 실행됩니다
- 전용 세션 디렉터리(`~/.config/claude-code-automation/session`)에서 Claude Code를 시작합니다
- 초기 메시지를 보내 세션을 활성화합니다
- 실패 시 재시도 로직이 작동합니다

## 로그 확인

로그는 다음 위치에 저장됩니다:
```
~/.config/claude-code-automation/logs/claude-code-automation.log
```

## 설정 파일

설정은 다음 위치에 저장됩니다:
```
~/.config/claude-code-automation/config.json
```

## 요구사항

- Python 3.8+
- `claude-code` 명령어가 시스템에 설치되어 있어야 함
- macOS 또는 Linux (cron 지원 필요)

## 라이선스

MIT License