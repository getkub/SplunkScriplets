Here’s a clean, professional README you can drop into your repo:

---

# 📦 Content Compiler Pipeline

This project provides a lightweight, extensible pipeline to **compile Markdown content into structured outputs** (e.g., combined documents or JSON payloads) using a configurable YAML-driven approach.

It is designed to run both:

* **Locally** (via shell script)
* **In CI/CD pipelines** (e.g., Azure DevOps)

---

# 🚀 Overview

The system consists of:

### 1. Bash Launcher

`compile_content.sh`

* Entry point for execution
* Detects Python availability
* Runs Python compiler if available
* Falls back to Bash implementation if needed

### 2. Python Compiler

`compile_content.py`

* Core logic
* Reads configuration (`build.yml`)
* Supports multiple compilation modes:

  * `list` → concatenates Markdown files
  * `json` → builds structured JSON output

### 3. Config File

`config/build.yml`

* Defines what to compile
* Declarative and flexible
* No code changes needed to add new outputs

---

# 📂 Example Project Structure

```text
repo/
├── content/
│   ├── common/
│   │   ├── intro.md
│   │   ├── guidelines.md
│   │   └── format.md
│   ├── items/
│   │   ├── item1.md
│   │   ├── item2.md
│   │   └── item3.md
│   └── compiled/
│
├── config/
│   ├── build.yml
│   └── metadata.csv
│
├── .pipeline/
│   └── scripts/
│       ├── compile_content.sh
│       ├── compile_content.py
│       └── compile_content_fallback.sh
```

---

# ⚙️ Configuration (`build.yml`)

Defines compilation targets.

## Example:

```yaml
targets:
  - name: system_docs
    mode: list
    output: content/compiled/system_output.md
    files:
      - content/common/intro.md
      - content/common/guidelines.md
      - content/common/format.md

  - name: structured_items
    mode: json
    output: content/compiled/items.json
    root_key: items
    key_field: key
    value_field: value
    key_mode: stem
    files:
      - content/items/*.md
```

---

# 🧠 How It Works

### Step-by-step:

1. Pipeline or user runs:

```bash
bash .pipeline/scripts/compile_content.sh config/build.yml
```

2. Script:

   * Locates Python compiler
   * Executes compilation logic

3. Compiler:

   * Loads `build.yml`
   * Iterates through `targets`
   * Resolves Markdown files (supports glob patterns)
   * Generates output:

     * Concatenated `.md`
     * Structured `.json`

4. Output is written to:

```
content/compiled/
```

---

# 📄 Supported Modes

## 1. `list` mode

Concatenates Markdown files into a single document.

### Output:

```md
<file1 content>

<file2 content>

<file3 content>
```

---

## 2. `json` mode

Creates structured JSON objects from Markdown files.

### Output:

```json
{
  "items": [
    {
      "key": "item1",
      "value": "Markdown content..."
    }
  ]
}
```

---

# 🔄 CI/CD Integration

This project is designed for **automatic compilation on commit**.

---

# 🔁 Example Workflow (Self Commit to Branch)

### Scenario:

You modify a Markdown file → pipeline compiles → commits result back to same branch.

---

## 1. Developer Flow

```bash
git checkout -b feature/update-content

# Edit markdown files
vim content/items/item1.md

git add .
git commit -m "update: item1 content"
git push origin feature/update-content
```

---

## 2. Pipeline Execution

Pipeline runs automatically and:

### ✔ Compiles content

```bash
bash .pipeline/scripts/compile_content.sh config/build.yml
```

### ✔ Detects changes

```bash
git diff
```

### ✔ Commits generated output

```bash
git add -A
git commit -m "chore: auto-build content [skip ci]"
git push origin feature/update-content
```

---

## 3. Safeguards

The pipeline **will NOT push changes when:**

* Build is triggered by a Pull Request
* Running on protected branches:

  * `main`
  * `release/*`
  * `pipeline/*`

---

# ✅ Benefits

* No manual compilation required
* Ensures generated artifacts are always up-to-date
* Works across multiple content types
* Easy to extend via config
* Safe CI/CD integration with branch protections

---

# 🧪 Local Usage

Run manually:

```bash
bash .pipeline/scripts/compile_content.sh config/build.yml
```

---

# ⚠️ Notes

* Python 3 is recommended
* If Python is unavailable, fallback script is used
* Markdown files must exist (missing files will fail the build)

---

# 🔧 Extending

You can easily:

* Add new targets in `build.yml`
* Introduce new output formats
* Integrate metadata enrichment (CSV-driven)
* Plug into other CI systems (GitHub Actions, GitLab CI)

---

# 📌 Summary

This setup provides a **simple, reliable content compilation pipeline** that:

* Converts Markdown → structured outputs
* Runs automatically in CI/CD
* Keeps generated artifacts version-controlled

---

If you want, I can next:

* Add **metadata CSV enrichment back into the README**
* Or show a **GitHub Actions equivalent pipeline**
