import hashlib
from pathlib import Path
import unittest
from streamlit.testing.v1 import AppTest

class UiTests(unittest.TestCase):
    def test_sample_and_integrity_workflow(self):
        app = AppTest.from_file('app.py').run(timeout=30)
        self.assertFalse(app.exception)
        self.assertEqual([m.value for m in app.metric], ['9', '4', '55.6%'])
        app.text_input[0].set_value(hashlib.sha256(Path('sample_data.csv').read_bytes()).hexdigest()).run()
        self.assertEqual(len(app.success), 1)
        app.text_input[0].set_value('0' * 64).run()
        self.assertIn('Mismatch', app.error[0].value)
        app.checkbox[0].set_value(True).run()
        self.assertEqual([m.value for m in app.metric], ['9', '4', '55.6%'])
        self.assertTrue(any('Outside bounds: 1' in c.value for c in app.caption))
        app.number_input[0].set_value(100.0).run()
        self.assertIn('minimum', app.error[0].value)

    def test_upload_mode_waits_for_file(self):
        app = AppTest.from_file('app.py').run(timeout=30)
        app.radio[0].set_value('Upload CSV').run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.metric), 0)
        self.assertEqual(len(app.get('file_uploader')), 1)
