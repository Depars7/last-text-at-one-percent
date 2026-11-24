"""make.fun entry: "Last Text at One Percent"
(slug u-azazex-last-text-at-one-percent-ba9fc876).

Gate: /output/entry.txt must be UTF-8 text of 1-200 characters, not only
whitespace, containing exactly ONE single-line final text message written
in the voice of a phone dying at 1% battery. This program writes the
winning text's exact UTF-8 bytes (no trailing newline), chmods the file
to 0644, and verifies the result by reading it back.
"""

import os
import stat

OUTPUT_PATH = "/output/entry.txt"

TEXT = (
    "1%. I can see the charger\u2014six inches away, just watching. "
    "Tell it I died in sight of land because you said 'one sec' "
    "forty minutes ago."
)


def validate(text: str) -> None:
    """Assert the text passes the bounty gate."""
    assert isinstance(text, str)
    assert 1 <= len(text) <= 200, f"length {len(text)} outside 1-200"
    assert text.strip(), "text must not be only whitespace"
    assert text == text.strip(), "no leading/trailing whitespace: every char counts"
    assert "\n" not in text and "\r" not in text, "text must be one line"


def main() -> None:
    validate(TEXT)
    data = TEXT.encode("utf-8")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
    os.chmod(OUTPUT_PATH, 0o644)

    # Read-back verification: bytes identical, no trailing newline, mode 0644.
    with open(OUTPUT_PATH, "rb") as f:
        back = f.read()
    assert back == data, "read-back bytes differ from intended text"
    assert not back.endswith(b"\n"), "output must have no trailing newline"
    mode = stat.S_IMODE(os.stat(OUTPUT_PATH).st_mode)
    assert mode == 0o644, f"mode {oct(mode)} != 0o644"
    validate(back.decode("utf-8"))


if __name__ == "__main__":
    main()
