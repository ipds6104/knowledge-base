"""kb/markdown_io.py — Baca/tulis file Markdown dengan YAML frontmatter.

Zero external dependency — parser YAML murni Python untuk kebutuhan
frontmatter sederhana (key-value + list of dicts).
"""

from pathlib import Path


# ─── YAML Parser ──────────────────────────────────────────────────────────────

def parse_yaml(yaml_str: str) -> dict:
    """Parse YAML frontmatter sederhana menjadi dict Python."""
    metadata = {}
    lines = yaml_str.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            i += 1
            continue

        # List key (e.g. "deadlines:")
        if stripped.endswith(':'):
            key = stripped[:-1].strip()
            i += 1
            list_items = []
            while i < len(lines) and (
                lines[i].startswith(' ') or lines[i].startswith('\t') or not lines[i].strip()
            ):
                l = lines[i]
                if not l.strip():
                    i += 1
                    continue
                cleaned = l.strip()
                if cleaned.startswith('-'):
                    item = {}
                    val = cleaned[1:].strip()
                    if ':' in val:
                        k, v = val.split(':', 1)
                        item[k.strip()] = v.strip().strip('"\'')
                    i += 1
                    while (
                        i < len(lines)
                        and lines[i].startswith(' ')
                        and not lines[i].strip().startswith('-')
                    ):
                        sub_line = lines[i].strip()
                        if sub_line and ':' in sub_line:
                            k, v = sub_line.split(':', 1)
                            item[k.strip()] = v.strip().strip('"\'')
                        i += 1
                    list_items.append(item)
                    continue
                else:
                    i += 1
            metadata[key] = list_items
            continue

        # Standard key-value
        if ':' in line:
            key, val = line.split(':', 1)
            metadata[key.strip()] = val.strip().strip('"\'')
        i += 1
    return metadata


def dump_yaml(metadata: dict) -> str:
    """Serialize dict Python ke string YAML frontmatter."""
    lines = []
    for k, v in metadata.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                if isinstance(item, dict):
                    keys = list(item.keys())
                    if keys:
                        first_key = keys[0]
                        lines.append(f'  - {first_key}: "{item[first_key]}"')
                        for sub_k in keys[1:]:
                            lines.append(f'    {sub_k}: "{item[sub_k]}"')
                else:
                    lines.append(f'  - "{item}"')
        else:
            lines.append(f'{k}: "{v}"')
    return "\n".join(lines)


# ─── File I/O ─────────────────────────────────────────────────────────────────

def read_markdown_file(file_path) -> tuple[dict, str]:
    """Baca file Markdown, pisahkan YAML frontmatter dan body.

    Returns:
        (metadata_dict, body_str) — metadata kosong jika tidak ada frontmatter.
    """
    path = Path(file_path)
    if not path.exists():
        return {}, ""

    content = path.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return {}, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content

    metadata = parse_yaml(parts[1])
    body = parts[2].lstrip()
    return metadata, body


def write_markdown_file(file_path, metadata: dict, body: str) -> None:
    """Tulis file Markdown dengan YAML frontmatter."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    yaml_str = dump_yaml(metadata)
    full_content = f"---\n{yaml_str}\n---\n{body}"
    path.write_text(full_content, encoding='utf-8')
