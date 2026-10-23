import hashlib
import io
import json
from datetime import datetime, timezone

import pandas as pd
import streamlit as st

st.set_page_config(page_title='ClimateProof', page_icon='🌍', layout='wide')
st.title('🌍 ClimateProof')
st.caption('Transparent quality checks and SHA-256 integrity fingerprints for environmental observations')

uploaded = st.file_uploader('Upload a CSV containing timestamp and value columns', type=['csv'])
if uploaded is None:
    st.info('Try the included sample_data.csv to explore the app.')
    st.stop()

raw = uploaded.getvalue()
digest = hashlib.sha256(raw).hexdigest()
try:
    df = pd.read_csv(io.BytesIO(raw))
except Exception as exc:
    st.error(f'Unable to read CSV: {exc}')
    st.stop()

if df.empty:
    st.error('The CSV is empty.')
    st.stop()

c1, c2 = st.columns(2)
with c1:
    time_col = st.selectbox('Timestamp column', df.columns, index=next((i for i, x in enumerate(df.columns) if x.lower() in ('timestamp', 'time', 'date')), 0))
with c2:
    numeric_candidates = [c for c in df.columns if c != time_col]
    if not numeric_candidates:
        st.error('Provide a separate measurement column.')
        st.stop()
    value_col = st.selectbox('Measurement column', numeric_candidates, index=next((i for i, x in enumerate(numeric_candidates) if x.lower() in ('value', 'measurement', 'reading')), 0))

with st.expander('Optional physical plausibility range'):
    use_bounds = st.checkbox('Enable lower/upper bounds (set for your sensor and unit)', value=False)
    low = st.number_input('Minimum', value=0.0)
    high = st.number_input('Maximum', value=100.0)
    if use_bounds and low > high:
        st.error('Minimum must be ≤ maximum.')
        st.stop()

parsed_time = pd.to_datetime(df[time_col], errors='coerce', utc=True)
values = pd.to_numeric(df[value_col], errors='coerce')
missing_timestamp = parsed_time.isna()
missing_value = values.isna()
duplicate_timestamp = parsed_time.duplicated(keep=False) & ~missing_timestamp
implausible = ((values < low) | (values > high)).fillna(False) if use_bounds else pd.Series(False, index=df.index)

# Robust modified Z-score (median absolute deviation); handle zero MAD without false positives.
valid = values.dropna()
median = valid.median() if not valid.empty else float('nan')
mad = (valid - median).abs().median() if not valid.empty else float('nan')
if pd.notna(mad) and mad > 0:
    modified_z = (0.6745 * (values - median) / mad).abs()
    outlier = (modified_z > 3.5).fillna(False)
else:
    outlier = pd.Series(False, index=df.index)

flags = pd.DataFrame({
    'missing_timestamp': missing_timestamp,
    'missing_or_non_numeric_value': missing_value,
    'duplicate_timestamp': duplicate_timestamp,
    'outside_user_bounds': implausible,
    'statistical_outlier': outlier,
})
flagged = flags.any(axis=1)
report = {
    'file_name': uploaded.name,
    'sha256': digest,
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'rows': len(df),
    'flagged_rows': int(flagged.sum()),
    'counts': {col: int(flags[col].sum()) for col in flags.columns},
    'method': 'MAD-based modified z-score > 3.5; outliers skipped when MAD is zero',
    'physical_bounds': {'min': low, 'max': high} if use_bounds else None,
    'note': 'SHA-256 verifies byte integrity only; it does not prove sensor authenticity or measurement accuracy.',
}

m1, m2, m3 = st.columns(3)
m1.metric('Records', len(df))
m2.metric('Flagged records', int(flagged.sum()))
m3.metric('Quality pass rate', f'{(1 - flagged.mean()) * 100:.1f}%')
st.subheader('Time series')
plot_df = pd.DataFrame({'timestamp': parsed_time, 'value': values}).dropna().sort_values('timestamp')
if not plot_df.empty:
    st.line_chart(plot_df.set_index('timestamp')['value'])
else:
    st.warning('No valid timestamp/value pairs to chart.')
st.subheader('Quality flags')
output = pd.concat([df.reset_index(drop=True), flags.reset_index(drop=True)], axis=1)
output['any_flag'] = flagged.to_numpy()
st.dataframe(output, use_container_width=True)
st.download_button('Download flagged CSV', output.to_csv(index=False).encode('utf-8'), 'climateproof_flagged.csv', 'text/csv')
st.subheader('File integrity')
st.code(digest, language=None)
st.caption('Compare this SHA-256 fingerprint with a trusted earlier fingerprint of the same file. It does not authenticate the source.')
st.download_button('Download JSON verification report', json.dumps(report, indent=2).encode('utf-8'), 'climateproof_report.json', 'application/json')
