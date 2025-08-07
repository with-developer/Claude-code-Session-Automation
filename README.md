# Claude Code Session Automation

Claude Code rate limit 회피를 위한 자동 세션 시작 도구

## 설치

### 소스에서 설치
```bash
git clone https://github.com/yourusername/claude-code-automation.git
cd claude-code-automation
pip install -e .
```

## 사용법

### 빠른 시작 (macOS)

현재 CLI 명령어에 문제가 있어 Python 스크립트를 직접 실행해야 합니다:

```bash
# 기본 설정으로 설치 (5시간 간격: 5시, 10시, 15시, 20시)
python setup-launchagent.py

# 특정 시간 설정 (HH:MM 또는 HHMM 형식)
python setup-launchagent.py 09:00 14:00 19:00
python setup-launchagent.py 0900 1400 1900

# 하나의 시간만 설정
python setup-launchagent.py 14:30
```

### 서비스 관리
```bash
# 서비스 상태 확인
launchctl list | grep claude-code-automation

# 로그 확인
tail -f ~/Library/Logs/claude-code-automation.out.log

# 서비스 제거
launchctl unload ~/Library/LaunchAgents/com.claude-code-automation.plist
rm ~/Library/LaunchAgents/com.claude-code-automation.plist
```

### 수동 실행
```bash
# 즉시 세션 시작
claude-code-automation start
```

## 동작 원리

- macOS: LaunchAgent를 통해 지정된 시간에 자동 실행
- 전용 세션 디렉터리(`~/.config/claude-code-automation/session`)에서 Claude Code를 시작합니다
- 초기 메시지를 보내 세션을 활성화합니다
- 실패 시 재시도 로직이 작동합니다
- 키체인 인증을 자동으로 처리합니다

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
- `claude` 명령어가 시스템에 설치되어 있어야 함
- macOS 또는 Linux

## 주의사항

- Claude Code 세션은 5시간 동안 유지됩니다.
- 세션이 시작될 때 Claude Code가 프롬프트를 표시할 수 있습니다.
- 스케줄 시간은 24시간 형식(HH:MM)으로 입력해야 합니다.
- **macOS 사용자**: cron 대신 LaunchAgent 사용을 권장합니다. 자세한 내용은 [LAUNCHD_SETUP.md](LAUNCHD_SETUP.md)를 참조하세요.

## 라이선스

MIT License