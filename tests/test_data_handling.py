import importlib.util
import importlib.machinery
import sys
import types
from datetime import datetime, timedelta
from pathlib import Path

class DummyModule(types.ModuleType):
    def __getattr__(self, name):
        def _(*args, **kwargs):
            return None
        return _

def import_ccb():
    sys.modules['streamlit'] = DummyModule('streamlit')
    dummy_plot = DummyModule('matplotlib.pyplot')
    matplotlib = types.ModuleType('matplotlib')
    matplotlib.pyplot = dummy_plot
    sys.modules['matplotlib'] = matplotlib
    sys.modules['matplotlib.pyplot'] = dummy_plot

    module_name = 'ccb'
    file_path = Path(__file__).resolve().parents[1] / 'ccb.py'
    loader = importlib.machinery.SourceFileLoader(module_name, str(file_path))
    spec = importlib.util.spec_from_loader(module_name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    sys.modules[module_name] = module
    return module


def test_save_and_load(tmp_path):
    ccb = import_ccb()
    tmp_file = tmp_path / 'benefits.json'
    ccb.DATA_FILE = str(tmp_file)

    expected = {
        'Benefit1': {
            'description': 'desc',
            'used': 0.5,
            'reset_interval': 'Monthly',
            'next_reset': '2099-01-01'
        }
    }
    ccb.benefits = expected.copy()
    ccb.save_benefits()

    ccb.benefits = {}
    loaded = ccb.load_benefits()
    assert loaded == expected


def test_check_resets(tmp_path):
    ccb = import_ccb()
    tmp_file = tmp_path / 'benefits.json'
    ccb.DATA_FILE = str(tmp_file)
    past = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    ccb.benefits = {
        'Benefit1': {
            'description': 'desc',
            'used': 1.0,
            'reset_interval': 'Monthly',
            'next_reset': past
        }
    }
    ccb.save_benefits()
    expected_next = ccb.calculate_reset_time('Monthly')
    ccb.check_resets()
    benefit = ccb.benefits['Benefit1']
    assert benefit['used'] == 0.0
    assert benefit['next_reset'] == expected_next
