
import pytest
from app.services.pdf_handler import fetch_gem_report

def test_fetch_gem_report():
    docs = fetch_gem_report()
    assert len(docs) > 0
