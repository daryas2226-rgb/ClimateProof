"""Deterministic checks; no network, AI, or claims of sensor authenticity."""
import hashlib
import io
import math
import re
from datetime import datetime, timezone
import numpy as np
import pandas as pd

def read_csv(raw):
    if len(raw) > 10 * 1024 * 1024:
        raise ValueError('Please use a CSV smaller than 10 MB.')
    try:
        frame = pd.read_csv(io.BytesIO(raw))
    except (ValueError, pd.errors.ParserError, UnicodeError) as exc:
        raise ValueError('Could not read CSV. Use a UTF-8 comma-separated file.') from exc
    if frame.empty:
        raise ValueError('The CSV has no data rows.')
    if len(frame.columns) < 2:
        raise ValueError('Provide separate timestamp and measurement columns.')
    return frame

def compare_digest(raw, expected):
    expected = expected.strip().lower()
    if not re.fullmatch(r'[0-9a-f]{64}', expected):
        raise ValueError('A SHA-256 fingerprint must contain exactly 64 hexadecimal characters.')
    return hashlib.sha256(raw).hexdigest() == expected

def analyse(raw, time_col, value_col, bounds=None, name='observations.csv'):
    frame = read_csv(raw)
    if time_col == value_col or time_col not in frame or value_col not in frame:
        raise ValueError('Select separate timestamp and measurement columns.')
    if bounds is not None:
        low, high = bounds
        if not math.isfinite(low) or not math.isfinite(high) or low > high:
            raise ValueError('Bounds must be finite, with minimum no greater than maximum.')
    source_time = frame[time_col].astype('string').str.strip()
    numeric_time = source_time.str.fullmatch(r'[+-]?\d+(\.\d+)?').fillna(False)
    times = pd.to_datetime(source_time.mask(numeric_time), format='mixed', errors='coerce', utc=True)
    values = pd.to_numeric(frame[value_col], errors='coerce')
    finite = pd.Series(np.isfinite(values), index=frame.index).fillna(False)
    clean = values.where(finite)
    valid = clean.dropna()
    median = valid.median() if len(valid) else None
    mad = (valid - median).abs().median() if len(valid) else None
    outliers = pd.Series(False, index=frame.index)
    if len(valid) >= 5 and mad is not None and mad > 0:
        outliers = (0.6745 * (clean - median).abs() / mad > 3.5).fillna(False)
        outlier_status = 'applied'
    else:
        outlier_status = 'skipped: fewer than 5 finite readings or zero MAD'
    flags = pd.DataFrame({
        'invalid_timestamp': times.isna(),
        'invalid_measurement': ~finite,
        'duplicate_timestamp': times.duplicated(keep=False) & times.notna(),
        'outside_user_bounds': ((clean < bounds[0]) | (clean > bounds[1])).fillna(False) if bounds else False,
        'statistical_outlier': outliers,
    })
    any_flag = flags.any(axis=1)
    output = frame.copy()
    flag_columns = {}
    for key, series in [*flags.items(), ('any_flag', any_flag)]:
        col = 'qc_' + key
        while col in output.columns:
            col = '_' + col
        output[col] = series.to_numpy()
        flag_columns[key] = col
    report = {
        'schema_version': 2,
        'file_name': name,
        'sha256': hashlib.sha256(raw).hexdigest(),
        'generated_at_utc': datetime.now(timezone.utc).isoformat(),
        'rows': len(frame),
        'flagged_rows': int(any_flag.sum()),
        'counts': {c: int(flags[c].sum()) for c in flags},
        'selected_columns': {'timestamp': time_col, 'measurement': value_col},
        'export_flag_columns': flag_columns,
        'physical_bounds': {'min': bounds[0], 'max': bounds[1]} if bounds else None,
        'timestamp_policy': 'Text timestamps parsed independently; missing offsets assumed UTC. Numeric epochs unsupported. Use ISO 8601 to avoid ambiguity.',
        'outlier_method': 'Absolute modified z-score > 3.5, minimum 5 finite readings; skipped if MAD=0.',
        'outlier_status': outlier_status,
        'note': 'Flags require review. No flags does not prove accuracy. SHA-256 checks byte integrity against a trusted baseline, not authenticity or blockchain anchoring.',
    }
    chart = pd.DataFrame({'timestamp': times, 'value': clean}).dropna().sort_values('timestamp')
    return output, report, chart
