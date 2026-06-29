import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from data import data_fetch


class DataFetchFallbackTest(unittest.TestCase):
    def test_fetch_and_process_data_handles_failed_spacex_api_calls(self):
        with patch.object(data_fetch, "fetch_rockets_data", return_value=None), \
             patch.object(data_fetch, "fetch_launchpads_data", return_value=None), \
             patch.object(data_fetch, "fetch_payloads_data", return_value=None), \
             patch.object(data_fetch, "fetch_cores_data", return_value=None), \
             patch.object(data_fetch, "fetch_initial_spacex_data", return_value=None):
            rockets_df, launchpads_df, payloads_df, cores_df = data_fetch.fetch_and_process_data()

        self.assertEqual(list(rockets_df.columns), data_fetch.ROCKETS_COLUMNS)
        self.assertEqual(list(launchpads_df.columns), data_fetch.LAUNCHPADS_COLUMNS)
        self.assertEqual(list(payloads_df.columns), data_fetch.PAYLOADS_COLUMNS)
        self.assertEqual(list(cores_df.columns), data_fetch.CORES_COLUMNS)

        self.assertTrue(rockets_df.empty)
        self.assertTrue(launchpads_df.empty)
        self.assertTrue(payloads_df.empty)
        self.assertTrue(cores_df.empty)


if __name__ == "__main__":
    unittest.main()
