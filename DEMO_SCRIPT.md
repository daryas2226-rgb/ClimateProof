# ClimateProof demo narration

English narration synthesized offline with Microsoft Zira. Visuals show the actual running Streamlit app and explanatory cards. No paid services or artificial sensor footage.

## ClimateProof

ClimateProof is a working prototype for reviewing environmental observation files before they are shared or used in analysis. It combines transparent quality checks with a SHA two fifty-six file fingerprint, in a small Streamlit application.

## A practical trust problem

A sensor spreadsheet may contain missing readings, repeated timestamps, or unusual values. Those problems need to be visible before anyone treats the data as evidence. A separate question is whether the file has changed since it was checked.

## Start with a CSV

Here is the running application. We can choose the built-in sample dataset or upload a CSV containing timestamps and measurements. For this demonstration, we use the included sample file. These are synthetic temperature readings, not a claim of field deployment.

## Choose the fields

After loading the file, the interface lets us select which columns represent time and the measured value. This makes the workflow usable with different column names. Timestamps are parsed into UTC, and readings are checked for valid numeric values.

## See the quality summary

The summary shows the number of records, the number of flagged records, and the percentage that passed these checks. That percentage describes this file under the selected rules. It is not a certification of measurement accuracy or environmental impact.

## Inspect the time series

The time-series chart makes it easy to see the unusually high sample reading alongside the surrounding observations. A visual spike is a reason to investigate. It could be a sensor issue, a data-entry issue, or a real event that should be retained.

## Trace every flag

The quality table preserves the original data and adds separate flags, so a reviewer can see why each row needs attention. The checks include invalid timestamps, missing or non-numeric readings, and duplicate timestamps. Every occurrence of a duplicated timestamp is marked.

## Explain the anomaly rule

Statistical outliers use a modified z-score based on the median absolute deviation, with a threshold of three point five. This is an explicit statistical rule, not a trained artificial intelligence model. The check is skipped when there are fewer than five finite readings, or the median absolute deviation is zero.

## Add domain knowledge

A reviewer can also enable a lower and upper plausibility bound. Those limits must make sense for the measurement type and unit. They are user-defined assumptions, and the report records them so someone else can understand the result.

## Export the review

The flagged CSV export keeps the source columns together with the check results. This supports a practical review process: inspect the suspect records, discuss them with the data owner, and document any corrections instead of silently removing unusual observations.

## Fingerprint the original file

The integrity section displays the SHA two fifty-six fingerprint of the exact original file bytes. We can enter an earlier trusted fingerprint here to check for a match or mismatch. Even a formatting change can produce a different fingerprint because the bytes are different.

## Keep an auditable report

The downloadable JSON report brings together the file name, fingerprint, record counts, flag counts, analysis method, and selected bounds. Its UTC generation time says when this report was created. It is not a trusted external timestamp or proof of when a sensor reading occurred.

## Clear limits

The prototype makes checks inspectable and produces a reproducible file fingerprint. It does not authenticate sensors, prove that measurements are true, or anchor records to a blockchain. Those limitations are stated in the application and documentation.

## Review. Explain. Preserve.

ClimateProof is built with Python, pandas, and Streamlit, and can run locally with no paid service. The repository includes the code, sample data, and setup instructions, so reviewers can reproduce the workflow themselves. Thank you for watching.

