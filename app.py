import json
from pathlib import Path
import streamlit as st
from quality import analyse, compare_digest, read_csv

st.set_page_config(page_title='ClimateProof', page_icon='🌍', layout='wide')
st.title('🌍 ClimateProof')
st.caption('Review environmental observations and compare file fingerprints.')
mode = st.radio('Data source', ['Sample dataset', 'Upload CSV'], horizontal=True)
if mode == 'Sample dataset':
    raw = Path(__file__).with_name('sample_data.csv').read_bytes()
    file_name = 'sample_data.csv'
    st.info('Synthetic temperature readings for demonstration; not real monitoring data.')
else:
    upload = st.file_uploader('Upload CSV (up to 10 MB)', type=['csv'])
    if upload is None:
        st.stop()
    raw, file_name = upload.getvalue(), upload.name
try:
    frame = read_csv(raw)
except ValueError as exc:
    st.error(str(exc))
    st.stop()
c1, c2 = st.columns(2)
time_col = c1.selectbox('Timestamp column', frame.columns, index=next((i for i, c in enumerate(frame.columns) if c.lower() in ('timestamp', 'time', 'date')), 0))
measurement_columns = [c for c in frame.columns if c != time_col]
value_col = c2.selectbox('Measurement column', measurement_columns, index=next((i for i, c in enumerate(measurement_columns) if c.lower() in ('value', 'measurement', 'reading')), 0))
st.caption('Use ISO 8601 timestamps. Values without an offset are interpreted as UTC. Analyse one sensor and one unit per file.')
with st.expander('Physical plausibility range'):
    use_bounds = st.checkbox('Check a range appropriate to this sensor and unit')
    low = st.number_input('Minimum', value=0.0)
    high = st.number_input('Maximum', value=40.0)
try:
    output, report, chart = analyse(raw, time_col, value_col, (low, high) if use_bounds else None, file_name)
except ValueError as exc:
    st.error(str(exc))
    st.stop()
m1, m2, m3 = st.columns(3)
m1.metric('Records', report['rows'])
m2.metric('Records to review', report['flagged_rows'])
m3.metric('Without detected flags', f"{100 * (1 - report['flagged_rows'] / report['rows']):.1f}%")
st.caption('A flag calls for review; absence of flags does not establish measurement accuracy.')
if report['outlier_status'] != 'applied':
    st.warning('Statistical outlier check ' + report['outlier_status'] + '. Other checks still run.')
st.subheader('Observations over time')
if len(chart):
    st.line_chart(chart.set_index('timestamp')['value'])
else:
    st.warning('No finite readings with valid timestamps to plot.')
st.subheader('Review the records')
st.dataframe(output, width='stretch')
st.download_button('Download reviewed CSV', output.to_csv(index=False).encode('utf-8'), 'climateproof_flagged.csv', 'text/csv')
st.subheader('File integrity')
st.code(report['sha256'], language=None)
expected = st.text_input('Earlier trusted SHA-256 fingerprint (optional)', max_chars=64)
if expected:
    try:
        if compare_digest(raw, expected):
            st.success('Match: these bytes match the supplied fingerprint.')
        else:
            st.error('Mismatch: these bytes do not match the supplied fingerprint.')
    except ValueError as exc:
        st.error(str(exc))
st.caption('A match does not prove sensor authenticity. This prototype does not anchor data on a blockchain.')
st.download_button('Download JSON report', json.dumps(report, indent=2, allow_nan=False).encode('utf-8'), 'climateproof_report.json', 'application/json')
