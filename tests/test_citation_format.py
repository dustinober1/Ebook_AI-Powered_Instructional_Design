import pytest
from hypothesis import given, strategies as st
import sys
import os

# Add scripts to path so we can import format_apa7
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))
from generate_bib import format_apa7

@given(st.fixed_dictionaries({
    'authors': st.lists(st.text(min_size=1), min_size=1, max_size=5),
    'title': st.text(min_size=1),
    'year': st.integers(min_value=1900, max_value=2100),
    'publication': st.text(),
    'url': st.text()
}))
def test_property_citation_format_compliance(entry):
    """
    Property 3: Citation Format Compliance
    Validates that various inputs generate a string with expected APA components.
    """
    result = format_apa7(entry)
    
    # Check for core components
    assert str(entry['year']) in result
    assert entry['title'] in result
    
    # Check author formatting (presence of & if multiple)
    if len(entry['authors']) > 1:
        assert "&" in result
    
    # Check for italics (markdown asterisk) around title
    assert f"*{entry['title']}*" in result
