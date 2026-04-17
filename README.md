# approxIPA

Research scaffold for IPA approximation and tonal contrast evaluation.

## Layout

- `src/approxipa/`: Python package for reusable code
- `scripts/`: runnable pipeline scripts
- `evaluation/`: metric and analysis utilities
- `data/`: local datasets, annotations, and outputs
- `tests/`: pytest suite
- `notebooks/`: exploratory notebooks

## Getting Started

1. Create a Python 3.11 environment.
2. Install dependencies with `uv sync` or your preferred toolchain.
3. Run scripts from `scripts/` and keep research artifacts under `data/`.

## Transphone Pipeline

Run the Kikuyu approximation pipeline with:

```bash
python scripts/run_transphone.py
```

The script reads `data/kikuyu_wordlist.txt` and writes `data/ipa_approximations.jsonl`.
