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
        app.number_input[0].set_value(100.0).run()
        self.assertIn('minimum', app.error[0].value)
