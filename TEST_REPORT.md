# ClimateProof validation

Validated locally on **24 October 2026** with Python **3.12.14**, Streamlit **1.66.1**, pandas **2.3.3**, and NumPy **2.3.5** on Windows.

## Automated results

`python -m unittest -v`: **18 tests passed** (16 core tests and 2 Streamlit AppTest tests).

Core coverage: synthetic sample totals; inclusive bounds; invalid bounds; original-byte hashes; invalid fingerprints; invalid and numeric timestamps; mixed ISO timestamps and time-zone offsets; infinite/non-numeric readings; malformed/empty/oversized files; ragged CSV rows; duplicate/empty headers; quoted fields and UTF-8 BOM; preservation of original cell text and colliding source columns; small samples; zero MAD; and extreme finite values without numerical overflow.

UI coverage: sample loading, the expected metrics, matching and mismatching fingerprints, overlapping bounds/outlier flags without double-counting, invalid bounds, and upload mode waiting safely for a file.

`python -m pip check`: **No broken requirements found.**

`git diff --check`: **Passed.**

## Browser and server checks

The browser walkthrough verified sample loading, CSV upload, expected metrics, optional bounds, and SHA-256 match/mismatch feedback. The synthetic sample produced **9 records**, **4 records to review**, and **55.6% without detected flags**.

After the final configuration change, the local server returned **HTTP 200 / ok** from `/_stcore/health`. Effective Streamlit configuration was verified as `server.maxUploadSize = 10` MB and `browser.gatherUsageStats = false`.

A GitHub Actions workflow is included for Python 3.12. This report documents local results; it does not claim that a remote workflow or public deployment has run successfully.

## Scope and limits

These checks establish the listed software behaviours, not scientific validity, sensor authenticity, climate impact, production readiness, or hackathon acceptance. The data is synthetic. SHA-256 compares file bytes against a supplied trusted baseline; the prototype does not use blockchain anchoring or an AI model. MAD-based flags are exploratory and may miss anomalies or flag valid extreme events. A row without a detected flag is not proof of an accurate measurement.
