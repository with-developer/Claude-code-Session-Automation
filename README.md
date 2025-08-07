# Claude Code Session Automation

Claude Code rate limit 회피를 위한 자동 세션 시작 도구

[![CI](https://github.com/with-developer/claude-code-automation/workflows/CI/badge.svg)](https://github.com/with-developer/claude-code-automation/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## ✨ 특징

- **통합 CLI 인터페이스**: 간단한 명령어로 Claude Code 세션 스케줄링
- **유연한 시간 형식**: HH:MM 및 HHMM 형식 모두 지원
- **LaunchAgent 통합**: macOS LaunchAgent를 통한 안정적인 백그라운드 스케줄링
- **세션 관리**: 스케줄 생성, 조회, 삭제, 수동 시작 기능
- **키체인 자동 인증**: 사용자 세션 컨텍스트에서 키체인 접근

## 🚀 설치

### 개발버전 설치

```bash
# 저장소 클론
git clone https://github.com/with-developer/claude-code-automation.git
cd claude-code-automation

# 가상환경 생성 및 설치
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Homebrew 설치 (향후 지원 예정)

```bash
# Custom tap 추가 (향후)
brew tap with-developer/claude-code-automation

# 설치 (향후)
brew install claude-code-automation
```

## 📖 사용법

### 기본 명령어

```bash
# 세션 스케줄링 (단일 시간)
claude-code-automation schedule 14:30

# 여러 시간 스케줄링 (HH:MM 형식)
claude-code-automation schedule 14:30 16:00 18:30

# HHMM 형식으로도 가능
claude-code-automation schedule 1430 1600 1830

# 현재 스케줄 확인
claude-code-automation list

# 모든 스케줄 삭제
claude-code-automation clear

# 수동으로 세션 시작
claude-code-automation start

# 현재 상태 확인
claude-code-automation status

# 도움말 보기
claude-code-automation help
```

### 사용 예시

```bash
# 오후 2시 30분에 세션 시작하도록 스케줄링
$ claude-code-automation schedule 14:30
✓ Scheduled sessions at: 14:30
Use 'claude-code-automation list' to view current schedule

# 현재 스케줄 확인
$ claude-code-automation list
Scheduled sessions:
  - 14:30

Service status: ✓ Service is loaded and running

# 여러 시간대 스케줄링
$ claude-code-automation schedule 09:00 14:00 19:00
✓ Scheduled sessions at: 09:00, 14:00, 19:00
```

## 🔧 시스템 요구사항

- **운영체제**: macOS (LaunchAgent 지원)
- **Python**: 3.8 이상
- **Claude Code**: 설치 및 인증 완료
- **권한**: 사용자 홈 디렉토리 쓰기 권한

## ⚙️ 동작 원리

1. **LaunchAgent 스케줄링**: macOS LaunchAgent를 통해 지정된 시간에 자동 실행
2. **전용 세션 디렉토리**: `~/.config/claude-code-automation/session`에서 Claude Code 실행
3. **자동 세션 활성화**: 초기 메시지 전송으로 세션 활성화
4. **키체인 자동 인증**: 사용자 세션 컨텍스트에서 키체인 접근
5. **실패 시 재시도**: 연결 실패 시 자동 재시도 로직

## 📁 파일 구조

```
~/.config/claude-code-automation/
├── session/                    # Claude Code 세션 디렉토리
│   └── .claude_session_marker  # 세션 상태 파일
├── logs/                       # 로그 파일
│   └── claude-code-automation.log
└── config.json                 # 설정 파일

~/Library/LaunchAgents/
└── com.claude-code-automation.plist  # LaunchAgent 설정
```

## 🔍 로그 확인

```bash
# 애플리케이션 로그
tail -f ~/.config/claude-code-automation/logs/claude-code-automation.log

# LaunchAgent 로그
tail -f ~/Library/Logs/claude-code-automation.out.log
tail -f ~/Library/Logs/claude-code-automation.err.log

# 서비스 상태 확인
launchctl list | grep claude-code-automation
```

## 🛠️ 고급 사용법

### LaunchAgent 수동 관리

```bash
# 서비스 상태 확인
launchctl list | grep claude-code-automation

# 서비스 중지
launchctl unload ~/Library/LaunchAgents/com.claude-code-automation.plist

# 서비스 시작
launchctl load ~/Library/LaunchAgents/com.claude-code-automation.plist

# 서비스 완전 제거
claude-code-automation clear
```

## ❓ 문제 해결

### 일반적인 문제

1. **"Invalid API key" 오류**
   - Claude Code가 올바르게 인증되었는지 확인
   - `claude login` 명령으로 재인증

2. **세션이 시작되지 않음**
   - `claude-code-automation status`로 상태 확인
   - 로그 파일에서 오류 메시지 확인

3. **LaunchAgent가 실행되지 않음**
   - `launchctl list | grep claude-code-automation`으로 상태 확인
   - 시스템 시간이 정확한지 확인

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🙏 감사의 말

- Claude Code 팀의 훌륭한 도구에 감사드립니다
- macOS LaunchAgent 시스템의 강력한 스케줄링 기능에 감사드립니다