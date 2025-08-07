class ClaudeCodeAutomation < Formula
  desc "Automated session manager for Claude Code to bypass rate limits"
  homepage "https://github.com/yourusername/claude-code-automation"
  url "https://github.com/yourusername/claude-code-automation/archive/v0.1.0.tar.gz"
  sha256 "YOUR_SHA256_HERE"
  license "MIT"

  depends_on "python@3.11"

  def install
    virtualenv_install_with_resources
  end

  def post_install
    (var/"log/claude-code-automation").mkpath
  end

  service do
    run [opt_bin/"claude-code-automation", "daemon"]
    keep_alive true
    log_path var/"log/claude-code-automation/service.log"
    error_log_path var/"log/claude-code-automation/error.log"
  end

  test do
    system "#{bin}/claude-code-automation", "--version"
  end
end