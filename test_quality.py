import hashlib
import json
from pathlib import Path
import unittest
from quality import analyse, compare_digest, read_csv

class QualityTests(unittest.TestCase):
    def run_data(self, rows):
        return analyse(('timestamp,value\n' + rows).encode(), 'timestamp', 'value')

    def test_sample_results(self):
        _, report, _ = analyse(Path('sample_data.csv').read_bytes(), 'timestamp', 'value')
        self.assertEqual((report['rows'], report['flagged_rows']), (9, 4))
        self.assertEqual(report['counts']['duplicate_timestamp'], 2)
        self.assertEqual(report['counts']['statistical_outlier'], 1)
        json.dumps(report, allow_nan=False)

    def test_non_finite_values(self):
        _, r, chart = self.run_data('2026-10-20,inf\n2026-10-21,-inf\n2026-10-22,word\n')
        self.assertEqual(r['counts']['invalid_measurement'], 3)
        self.assertEqual(len(chart), 0)

    def test_mixed_iso_formats_and_offsets(self):
        _, r, _ = self.run_data('2026-10-20,1\n2026-10-21T05:00:00+05:00,2\n2026-10-21T00:00:00Z,3\n')
        self.assertEqual(r['counts']['invalid_timestamp'], 0)
        self.assertEqual(r['counts']['duplicate_timestamp'], 2)

    def test_invalid_and_numeric_timestamps(self):
        _, r, _ = self.run_data('bad,1\n,2\n1792483200,3\n')
        self.assertEqual(r['counts']['invalid_timestamp'], 3)

    def test_zero_mad(self):
        _, r, _ = self.run_data('\n'.join(f'2026-10-{i+10},1' for i in range(6)))
        self.assertIn('skipped', r['outlier_status'])

    def test_small_samples(self):
        _, r, _ = self.run_data('2026-10-20,1\n2026-10-21,999\n')
        self.assertIn('skipped', r['outlier_status'])

    def test_bounds_inclusive(self):
        _, r, _ = analyse(b'timestamp,value\n2026-10-20,0\n2026-10-21,40\n2026-10-22,41\n', 'timestamp', 'value', (0, 40))
        self.assertEqual(r['counts']['outside_user_bounds'], 1)

    def test_reject_invalid_bounds(self):
        for bounds in [(10, 0), (0, float('inf'))]:
            with self.assertRaises(ValueError):
                analyse(b'timestamp,value\n2026-10-20,1', 'timestamp', 'value', bounds)

    def test_source_column_preserved(self):
        out, r, _ = analyse(b'timestamp,value,qc_invalid_timestamp\n2026-10-20,1,original', 'timestamp', 'value')
        self.assertEqual(out.iloc[0]['qc_invalid_timestamp'], 'original')
        self.assertEqual(r['export_flag_columns']['invalid_timestamp'], '_qc_invalid_timestamp')

    def test_digest_original_bytes(self):
        raw = b'timestamp,value\n2026-10-20,1\n'
        digest = hashlib.sha256(raw).hexdigest()
        self.assertTrue(compare_digest(raw, digest.upper()))
        self.assertFalse(compare_digest(raw + b'\n', digest))
        self.assertEqual(analyse(raw, 'timestamp', 'value')[1]['sha256'], digest)

    def test_invalid_digest(self):
        with self.assertRaises(ValueError):
            compare_digest(b'example', 'not a hash')

    def test_invalid_files(self):
        for raw in [b'', b'timestamp,value\n', b'one\n1\n', b'\xff\xfe', b'x' * (10*1024*1024 + 1)]:
            with self.assertRaises(ValueError):
                read_csv(raw)

if __name__ == '__main__':
    unittest.main()
