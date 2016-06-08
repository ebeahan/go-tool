
import os
import pytest
import sys

sys.path.append(os.path.abspath(".."))

from go.go import hostname_resolves

def test_hostname_resolves_successful():
    assert True == hostname_resolves("www.google.com")
