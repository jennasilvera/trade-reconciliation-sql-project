from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_FILES = [ROOT / "README.md"] + list((ROOT / "docs").glob("*.md"))

LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def is_external_link(target: str) -> bool:
    return (
        target.startswith("http://")
        or target.startswith("https://")
        or target.startswith("#")
        or target.startswith("mailto:")
    )


def strip_anchor(target: str) -> str:
    return target.split("#", 1)[0]


def test_markdown_links_point_to_existing_files():
    broken_links = []

    for markdown_file in MARKDOWN_FILES:
        text = markdown_file.read_text()

        for _, target in LINK_PATTERN.findall(text):
            target = strip_anchor(target.strip())

            if not target or is_external_link(target):
                continue

            resolved_path = (markdown_file.parent / target).resolve()

            if not resolved_path.exists():
                broken_links.append(
                    f"{markdown_file.relative_to(ROOT)} -> {target}"
                )

    assert not broken_links, "Broken Markdown links found:\n" + "\n".join(broken_links)
