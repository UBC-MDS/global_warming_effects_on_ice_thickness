from pathlib import Path

import pandas as pd
import pytest
from src import import_data as ipd
import os

"""
Run tests from project root dir
>>> pytest
"""

def test_download_data(monkeypatch):
    """Test download_data
    - NOTE this can fail if you download too many times and the gov ratelimits your ip!
    """
    monkeypatch.setattr('builtins.input', lambda _: 'y')

    # remove file before testing
    p = ipd.save_dir_default
    if p.exists():
        p.unlink()
    
    # test from cmd line with default args
    os.system('python -m download')
    assert p.exists(), 'data file failed to download!'

    # test failure with incorrect save_dir
    p_data = ipd.download_data(url=None, save_dir='not_a_dir.csv')
    assert p_data is None

def test_load_data():
    """Test df is loaded from /data/raw"""
    df = ipd.load_data()
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] >= 50000, 'df doesn\'t have enough rows!'

def test__input(monkeypatch):
    """Test custom import_data._input func works
    - use pytest's monkeypatch to modify system 'input' function
    """

    # user says 'y'
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    assert ipd._input(msg='') == True

    # user says 'n'
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    assert ipd._input(msg='') == False

    # user says anything else
    monkeypatch.setattr('builtins.input', lambda _: 'sdfsfsdf')
    assert ipd._input(msg='') == False

