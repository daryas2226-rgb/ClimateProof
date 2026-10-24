# ClimateProof
A small environmental-data review tool for **Climate Data & Environmental Monitoring**.
It checks one sensor's timestamped CSV, exports transparent row-level flags, and compares original-file SHA-256 fingerprints. No AI account or paid API is needed.

## Run
Tested on Python 3.12.
```sh
python -m venv .venv
# Activate .venv using your operating system's normal command
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
The bundled synthetic dataset opens immediately. Switch to Upload CSV for your own UTF-8 comma-separated file (up to 10 MB). Use one sensor and one measurement unit per file.

## What works
- Empty/malformed input handling and independent timestamp/measurement selection.
- Missing/invalid timestamps, missing/non-numeric/infinite readings, repeated timestamps.
- Optional physical bounds supplied by the reviewer.
- Modified z-score outliers (absolute score >3.5, at least five finite readings; skipped when MAD=0).
- Chronological chart, CSV export preserving original columns, strict JSON report.
- SHA-256 of original bytes, plus match/mismatch against a supplied earlier trusted digest.

## Reproduce the demo
Open Sample dataset: **9 records, 4 to review, 55.6% without detected flags**.
The extreme reading is flagged once, two rows share a timestamp, and one reading is missing.
Enable bounds 0–40 for this synthetic temperature example. The out-of-bounds flag overlaps the statistical outlier; flagged records are not double-counted.
Copy the shown digest into the comparison field: match. Replace one character: mismatch. Download CSV and JSON.
These are synthetic examples, not measurements from a deployed environmental network.

## Validation
```sh
python -m unittest -v
```
12 core regression tests and a UI interaction test cover the sample, invalid files, non-finite values, mixed timestamp formats and offsets, duplicate timestamps, small/constant samples, bounds, preserved columns, and changed-file fingerprints.
Validated 23 October 2026. Tests establish these behaviours, not scientific accuracy or field performance.

## Limits
- A flag requires review. No flags does not establish data quality or prove a sensor is accurate.
- Timestamps without offsets are assumed UTC; use ISO 8601 to avoid ambiguity. Numeric epochs are unsupported.
- No missing-interval inference, sensor calibration, provenance verification, or signed identity.
- SHA-256 is only a byte-integrity comparison. This prototype does **not** anchor data on a blockchain.
- No claim of measured climate benefit, customers, pilots, or production deployment.
- For confidential data run locally; a remote host would process uploaded files on its server.

## Submission materials
See DEMO_SCRIPT.md for a 3–5 minute walkthrough and the actual working app.
Repository creation and a public project page do not constitute final hackathon submission.
