import pathlib

ROOT = pathlib.Path("./data").resolve()


def _safe(path: str) -> pathlib.Path:
    p = (ROOT / path).resolve()
    if not p.is_relative_to(ROOT):
        raise ValueError("path outside workspace")
    return p


def read_file(path: str) -> str:
    """Read a text file and return its contents."""
    return _safe(path).read_text()[:20000]


def write_file(path: str, content: str) -> str:
    """Write content to a file, creating it if needed."""
    p = _safe(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    return f"wrote {len(content)} chars to {path}"
