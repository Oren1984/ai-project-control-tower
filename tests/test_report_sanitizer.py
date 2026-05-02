from app.reports.report_sanitizer import sanitize_report


def test_masks_aws_key():
    content = "key=AKIAIOSFODNN7EXAMPLE"
    result = sanitize_report(content)
    assert "AKIAIOSFODNN7EXAMPLE" not in result
    assert "[REDACTED]" in result


def test_masks_openai_key():
    content = "sk-" + "A" * 48
    result = sanitize_report(content)
    assert "A" * 48 not in result


def test_masks_env_password():
    content = "PASSWORD=supersecretvalue123"
    result = sanitize_report(content)
    assert "supersecretvalue123" not in result
    assert "PASSWORD=" in result
    assert "[REDACTED]" in result


def test_removes_autofix_header():
    content = "## Auto Fix\nsome instructions here\n\n## Next Section\nstuff"
    result = sanitize_report(content)
    assert "Auto Fix" not in result


def test_removes_diff_block():
    content = "```diff\n- old line\n+ new line\n```"
    result = sanitize_report(content)
    assert "- old line" not in result


def test_removes_patch_block():
    content = "```patch\n--- a/file.py\n+++ b/file.py\n```"
    result = sanitize_report(content)
    assert "+++ b/file.py" not in result


def test_clean_content_unchanged():
    content = "# Audit Report\n\nNo issues found.\n"
    result = sanitize_report(content)
    assert "No issues found." in result
    assert "# Audit Report" in result


def test_no_secrets_in_clean_report():
    content = "This is a finding about security configuration. Recommended: Review access policies."
    result = sanitize_report(content)
    assert "[REDACTED]" not in result
    assert result == content
