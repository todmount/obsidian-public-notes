from pathlib import Path
import html
import markdown


NOTES_DIR = Path("notes")
SITE_DIR = Path("site")


CSS = """
body {
    max-width: 900px;
    margin: 40px auto;
    padding: 0 20px;
    font-family: system-ui, sans-serif;
    line-height: 1.6;
    color: #24292f;
    background: #ffffff;
}

h1, h2, h3, h4 {
    line-height: 1.25;
}

pre {
    padding: 16px;
    overflow-x: auto;
    border-radius: 8px;
    background: #f6f8fa;
}

code {
    font-family: monospace;
}

img {
    max-width: 100%;
}

a {
    color: #0969da;
}

table {
    border-collapse: collapse;
    width: 100%;
}

th, td {
    border: 1px solid #d0d7de;
    padding: 6px 10px;
}

blockquote {
    border-left: 4px solid #d0d7de;
    margin-left: 0;
    padding-left: 16px;
    color: #57606a;
}
"""


def render_page(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{html.escape(title)}</title>
    <link rel="stylesheet" href="/obsidian-public-notes/style.css">
</head>
<body>
{body}
</body>
</html>
"""


def main():
    SITE_DIR.mkdir(exist_ok=True)

    (SITE_DIR / "style.css").write_text(CSS, encoding="utf-8")

    for source in NOTES_DIR.rglob("*.md"):
        relative = source.relative_to(NOTES_DIR)
        destination = SITE_DIR / relative.with_suffix(".html")

        destination.parent.mkdir(parents=True, exist_ok=True)

        text = source.read_text(encoding="utf-8")

        body = markdown.markdown(
            text,
            extensions=[
                "extra",
                "fenced_code",
                "tables",
            ],
        )

        page = render_page(source.stem, body)

        destination.write_text(page, encoding="utf-8")

    print("Site generated successfully.")


if __name__ == "__main__":
    main()
