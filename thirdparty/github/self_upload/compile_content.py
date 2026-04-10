#!/usr/bin/env python3
import csv
import json
import pathlib
import sys
from datetime import datetime, timezone
from typing import Any

def ts() -> str:
  return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def log_info(message: str) -> None:
  print(f"[{ts()}] [INFO] {message}")

def log_warn(message: str) -> None:
  print(f"[{ts()}] [WARN] {message}", file=sys.stderr)

def parse_scalar(value: str) -> str:
  value = value.strip()
  if len(value) >= 2 and ((value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'"))):
    return value[1:-1]
  return value

def parse_simple_yaml(yaml_text: str) -> dict[str, Any]:
  lines = yaml_text.splitlines()
  targets = []
  current = None
  in_files = False
  in_targets = False

  for raw in lines:
    raw = raw.rstrip("\r")
    if not raw.strip() or raw.lstrip().startswith("#"):
      continue

    line = raw.split("#", 1)[0].rstrip()
    if not line.strip():
      continue

    indent = len(line) - len(line.lstrip(" "))
    stripped = line.strip()

    if indent == 0 and stripped == "targets:":
      in_targets = True
      in_files = False
      continue

    if not in_targets:
      continue

    if indent == 2 and stripped.startswith("-"):
      if current is not None:
        targets.append(current)
      current = {"files": []}
      in_files = False
      remaining = stripped[1:].strip()
      if remaining and ":" in remaining:
        key, value = remaining.split(":", 1)
        current[key.strip()] = parse_scalar(value)
      continue

    if current is None:
      raise SystemExit("Invalid YAML structure")

    if indent == 4 and stripped == "files:":
      in_files = True
      continue

    if in_files and indent >= 6 and stripped.startswith("-"):
      current["files"].append(parse_scalar(stripped[1:].strip()))
      continue

    if indent == 4 and ":" in stripped:
      in_files = False
      key, value = stripped.split(":", 1)
      current[key.strip()] = parse_scalar(value)
      continue

  if current is not None:
    targets.append(current)

  return {"targets": targets}

def load_config(config_path: pathlib.Path) -> dict[str, Any]:
  text = config_path.read_text(encoding="utf-8")
  try:
    import yaml
    return yaml.safe_load(text)
  except ModuleNotFoundError:
    return parse_simple_yaml(text)

def resolve_markdown_files(root_dir: pathlib.Path, entries: list[str]) -> list[pathlib.Path]:
  files = []
  for entry in entries:
    for match in root_dir.glob(entry):
      if match.is_file() and match.suffix == ".md":
        files.append(match)
  return files

def compile_list(root_dir: pathlib.Path, target: dict[str, Any]) -> None:
  files = resolve_markdown_files(root_dir, target.get("files", []))
  out_path = root_dir / target["output"]
  out_path.parent.mkdir(parents=True, exist_ok=True)
  with out_path.open("w", encoding="utf-8") as out:
    for f in files:
      out.write(f.read_text(encoding="utf-8") + "\n\n")

def compile_json(root_dir: pathlib.Path, target: dict[str, Any]) -> None:
  files = resolve_markdown_files(root_dir, target.get("files", []))
  items = []
  for f in files:
    items.append({
      target.get("key_field", "key"): f.stem,
      target.get("value_field", "value"): f.read_text(encoding="utf-8")
    })
  payload = {target.get("root_key", "items"): items}
  out_path = root_dir / target["output"]
  out_path.parent.mkdir(parents=True, exist_ok=True)
  out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

def main():
  root_dir = pathlib.Path(__file__).resolve().parents[2]
  trigger = sys.argv[1] if len(sys.argv) > 1 else "config/build.yml"
  config = load_config(root_dir / trigger)

  for target in config.get("targets", []):
    mode = target.get("mode")
    if mode == "list":
      compile_list(root_dir, target)
    elif mode == "json":
      compile_json(root_dir, target)

if __name__ == "__main__":
  main()
