import pytest
import sys
from weasyprint import document
sys.path.insert(0, './flask')

import exports

def test_pdf_export():
    assert isinstance(exports.pdf("a"), document.Document)