"""Shared artifact locations for enclosure tools; no geometry changes."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent
PATHS=json.loads(Path(__file__).with_name('artifact_paths.json').read_text())
def asset(root,name):
    """Resolve an artifact under the enclosure root; preserve archive roots."""
    root=Path(root)
    return root / PATHS.get(str(name),str(name)) if root.resolve()==ROOT else root/name
