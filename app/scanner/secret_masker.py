import re
from typing import Callable, Union

REDACTED = "[REDACTED]"


def _preserve_key(m: re.Match) -> str:
    return m.group(1) + REDACTED


_PATTERNS: list[tuple[re.Pattern, Union[str, Callable[[re.Match], str]]]] = [
    # AWS access key ID: AKIA followed by 16 uppercase alphanumerics
    (re.compile(r"AKIA[0-9A-Z]{16}"), REDACTED),
    # GitHub tokens: ghp_, gho_, ghu_, ghs_, ghr_ prefix
    (re.compile(r"gh[pousr]_[A-Za-z0-9_]{36,}"), REDACTED),
    # GitHub fine-grained PAT
    (re.compile(r"github_pat_[A-Za-z0-9_]{82}"), REDACTED),
    # OpenAI key: sk- followed by exactly 48 alphanumerics
    (re.compile(r"sk-[A-Za-z0-9]{48}"), REDACTED),
    # Anthropic key: sk-ant- prefix
    (re.compile(r"sk-ant-[A-Za-z0-9_\-]{40,}"), REDACTED),
    # Google API key: AIza prefix + 35 chars
    (re.compile(r"AIza[0-9A-Za-z_\-]{35}"), REDACTED),
    # JWT: three base64url segments separated by dots, starting with eyJ
    (
        re.compile(r"eyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+"),
        REDACTED,
    ),
    # .env style secrets: KEYWORD=value — preserve the key name
    (
        re.compile(
            r"(?m)^([ \t]*(?:PASSWORD|SECRET|API_KEY|APIKEY|TOKEN|PASSWD|PRIVATE_KEY|"
            r"AUTH_TOKEN|ACCESS_TOKEN|CREDENTIALS?)\w*\s*=\s*)['\"]?\S{4,}['\"]?",
            re.IGNORECASE,
        ),
        _preserve_key,
    ),
    # Bearer tokens in HTTP headers — preserve "bearer " prefix
    (
        re.compile(r"(?i)(bearer\s+)[A-Za-z0-9_\-\.]{20,}"),
        _preserve_key,
    ),
]


def mask_secrets(content: str) -> str:
    for pattern, replacement in _PATTERNS:
        content = pattern.sub(replacement, content)
    return content
