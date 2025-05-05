
# Project Name

A brief description of your project.

---

## Prerequisites

- Python 3.x
- pytest (for testing)

---

## Usage

Run the script with the following command:

```bash
python run.py <target_directory> [--exclude <dir1> <dir2> ...]
```

Example

```bash
1 python run.py ttn-medical-core --exclude templates
```

---

## Test

To run test is necessary to install pytest dependency

```bash
python -m venv .venv
pip install pytest
pytest tests/ -v
```
