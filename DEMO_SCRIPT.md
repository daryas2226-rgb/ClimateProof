# ClimateProof — 3:35 screen-demo script
Use the real running app. Sample values are explicitly synthetic. Do not show personal files, account details, or a fabricated deployment.

**0:00–0:25 · Problem.** “Before environmental data supports a decision, someone has to review it. Missing readings, repeated timestamps and unusual values can be hidden in a simple spreadsheet. ClimateProof is a transparent review prototype for the Climate Data and Environmental Monitoring track.”

**0:25–0:55 · Input.** Show the sample mode and its synthetic-data label. “This example is synthetic temperature data. The app starts with a sample, or the user uploads one sensor's CSV and selects timestamp and measurement columns. Timestamps without an offset are assumed to be UTC.”

**0:55–1:35 · Review.** Show metrics, chart and table. “There are nine records. Four need review: an extreme reading, two records sharing a timestamp, and a missing value. We count flagged records once, even when a row has several flags. A flag is a reason to investigate, not proof that a sensor is faulty.”

**1:35–2:05 · Bounds.** Open physical range, enable 0–40. “A reviewer who knows the measurement and unit can set physical bounds. The extreme value is now also outside those bounds. The total remains four, because we do not double-count it. Statistical flags use median absolute deviation; the test is skipped for small or constant samples.”

**2:05–2:35 · Exports.** Download CSV and JSON. Show the JSON in an editor. “The export retains source columns and adds named review flags. The report records selected columns, thresholds, counts, timestamp assumptions and the original file's fingerprint.”

**2:35–3:05 · Integrity.** Paste the visible digest, show match; change a character, show mismatch. “This compares the file bytes with a fingerprint from an earlier trusted record. It detects a difference from that baseline. It does not authenticate the sensor, and no blockchain anchoring is implemented.”

**3:05–3:35 · Evidence and next test.** Show repository and actual passing tests. “The public Python source includes regression tests for invalid values, time formats, duplicate records and fingerprint changes. This is a working proof of concept, not a validated monitoring deployment. The next step is to evaluate it with a real environmental team and labelled sensor data.”

Target 3:35, verify the recorded duration is between 3 and 5 minutes. Keep all limitations audible or visible. Upload only the actual completed recording; do not use the old OpportunityProof or SignalForge video.
