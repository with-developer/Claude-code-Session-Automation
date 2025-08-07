# LaunchAgent 설정 가이드

macOS에서 cron 대신 LaunchAgent를 사용하면 키체인 접근 문제를 해결할 수 있습니다.

## 설정 방법

1. LaunchAgent 설치:
```bash
cp com.claude-code-automation.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.claude-code-automation.plist
```

2. 상태 확인:
```bash
launchctl list | grep claude-code-automation
```

3. 중지/시작:
```bash
# 중지
launchctl unload ~/Library/LaunchAgents/com.claude-code-automation.plist

# 시작
launchctl load ~/Library/LaunchAgents/com.claude-code-automation.plist
```

4. 제거:
```bash
launchctl unload ~/Library/LaunchAgents/com.claude-code-automation.plist
rm ~/Library/LaunchAgents/com.claude-code-automation.plist
```

## 스케줄 변경

`com.claude-code-automation.plist` 파일의 `StartCalendarInterval` 섹션을 수정하여 원하는 시간에 실행되도록 설정할 수 있습니다.

예시:
```xml
<dict>
    <key>Hour</key>
    <integer>9</integer>
    <key>Minute</key>
    <integer>30</integer>
</dict>
```

변경 후에는 반드시 unload/load를 다시 해야 합니다.