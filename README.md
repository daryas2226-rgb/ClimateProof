# ClimateProof 🌍

ClimateProof is a small, transparent Streamlit application for inspecting environmental sensor CSVs and producing reproducible SHA-256 file fingerprints.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Upload `sample_data.csv` or a CSV with a timestamp column and a numeric reading column. Select the appropriate columns in the interface. Set plausible minimum and maximum readings only when the measurement type and unit justify them.

## Features
- Missing timestamps and missing/non-numeric readings
- Duplicate timestamps (all repeated occurrences are marked)
- Optional user-specified plausibility bounds
- Statistical anomaly detection using modified z-score / median absolute deviation (MAD); intentionally avoids false positives when MAD=0
- Time-series chart and row-level flags
- CSV export and JSON quality report
- SHA-256 fingerprint of the **original uploaded bytes**

## Limitations
- This is a prototype; it does not verify the provenance or calibration of sensors.
- A hash demonstrates file integrity only when compared to a previously trusted digest; it is not blockchain anchoring.
- MAD-based outlier detection is exploratory and may miss anomalies or flag valid extreme events.
- Timestamps are normalized to UTC. It does not infer missing expected sampling intervals.
- No claims are made about verified emissions reductions or deployment to municipalities.

## Demo plan (3–5 minutes)
1. Explain environmental data quality challenges.
2. Start Streamlit and upload `sample_data.csv`.
3. Show flagged missing readings, repeated timestamps and the extreme value.
4. Set appropriate bounds, inspect chart, export CSV and JSON.
5. Show SHA-256 and explain integrity-versus-authenticity limitation.
