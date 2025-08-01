class ClaudeCodeAutomation < Formula
  desc "Claude Code rate limit 회피를 위한 자동 세션 시작 도구"
  homepage "https://github.com/weakness/claude-code-automation"
  url "https://github.com/weakness/claude-code-automation/archive/v0.1.0.tar.gz"
  sha256 "YOUR_SHA256_HERE"
  license "MIT"

  depends_on "python@3.11"

  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/claude-code-automation", "--version"
  end
end