# LaunchAgent 설정 가이드

macOS에서 cron 대신 LaunchAgent를 사용하면 키체인 접근 문제를 해결할 수 있습니다.

## 설정 방법

1. plist 파일 수정:
   - 원하는 시간으로 `StartCalendarInterval` 섹션 수정
   - 필요시 `ProgramArguments`의 경로를 시스템에 맞게 수정

2. LaunchAgent 설치:
```bash
cp com.claude-code-automation.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.claude-code-automation.plist
```

3. 상태 확인:
```bash
launchctl list | grep claude-code-automation
```

4. 로그 확인:
```bash
# stdout 로그
tail -f ~/Library/Logs/claude-code-automation.out.log

# stderr 로그
tail -f ~/Library/Logs/claude-code-automation.err.log
```

## 관리 명령어

```bash
# 중지
launchctl unload ~/Library/LaunchAgents/com.claude-code-automation.plist

# 시작
launchctl load ~/Library/LaunchAgents/com.claude-code-automation.plist

# 제거
launchctl unload ~/Library/LaunchAgents/com.claude-code-automation.plist
rm ~/Library/LaunchAgents/com.claude-code-automation.plist
```

## 스케줄 변경

`com.claude-code-automation.plist` 파일의 `StartCalendarInterval` 섹션을 수정하여 원하는 시간에 실행되도록 설정할 수 있습니다.

### 단일 시간 설정:
```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>9</integer>
    <key>Minute</key>
    <integer>30</integer>
</dict>
```

### 여러 시간 설정:
```xml
<key>StartCalendarInterval</key>
<array>
    <dict>
        <key>Hour</key>
        <integer>6</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <dict>
        <key>Hour</key>
        <integer>12</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <dict>
        <key>Hour</key>
        <integer>18</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</array>
```

변경 후에는 반드시 unload/load를 다시 해야 합니다.

## LaunchAgent vs cron

- **LaunchAgent**: 사용자 세션에서 실행되어 키체인 접근 가능
- **cron**: 시스템 데몬으로 실행되어 키체인 접근 불가

Claude Code는 키체인에 인증 정보를 저장하므로, macOS에서는 LaunchAgent 사용을 권장합니다.