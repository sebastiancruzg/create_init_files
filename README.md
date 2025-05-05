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
git clone https://sebastiancruz10@bitbucket.org/ttndevel/create_init_files.git
python -m run <target_directory> [--exclude <dir1> <dir2> ...]
```

### Example

Project Structure:
.
├── ttn-medical-core/
└── create_init_files/

To run:

```bash
cd create_init_file
python -m run ../ttn-medical-core --exclude templates
```

---

## Test

To run test is necessary to install pytest dependency

```bash
python -m venv .venv
pip install pytest
pytest tests/ -v
```
