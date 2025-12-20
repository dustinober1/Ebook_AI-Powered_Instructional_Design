import datetime
from hypothesis import given, strategies as st
import sys
import os

# Add scripts to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))
from content_audit import get_status

@given(st.dates())
def test_property_freshness_status(date_val):
    """
    Property 9: Content Freshness Tracking
    Validates that review dates result in correct status labels.
    """
    status = get_status(date_val)
    
    today = datetime.date.today()
    age_days = (today - date_val).days
    
    if age_days < 0: # Future date
        # Our script doesn't explicitly handle future dates, but age_days will be negative
        assert status in ["✅ Fresh", "⚠️ Unknown"]
    elif age_days < 180:
        assert status == "✅ Fresh"
    elif age_days < 365:
        assert status == "🕒 Needs Review"
    else:
        assert status == "🚨 Stale"

def test_status_invalid_inputs():
    assert get_status(None) == "⚠️ Unknown"
    assert get_status("") == "⚠️ Unknown"
    assert get_status("not-a-date") == "❌ Invalid Date"
