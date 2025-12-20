import os
import shutil
import tempfile
from contextlib import contextmanager
from hypothesis import given, strategies as st, settings
from mkdocs.config import load_config
from mkdocs.commands.build import build

@contextmanager
def temp_dir_context():
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)

@settings(deadline=2000)
@given(st.just("CC BY-SA 4.0"))
def test_property_license_display(license_text):
    """
    Property 11.3: License Display
    Validates that license information is prominent in global navigation or footer.
    """
    with temp_dir_context() as base_dir:
        docs_dir = os.path.join(base_dir, 'docs')
        os.makedirs(docs_dir)
        with open(os.path.join(docs_dir, 'index.md'), 'w') as f:
            f.write("# Home")
            
        with open(os.path.join(base_dir, 'mkdocs.yml'), 'w') as f:
            f.write(f"site_name: Test\ncopyright: 'Licensed under {license_text}'\n")
            
        cfg = load_config(config_file=os.path.join(base_dir, 'mkdocs.yml'))
        cfg['site_dir'] = os.path.join(base_dir, 'site')
        build(cfg)
        
        output_path = os.path.join(cfg['site_dir'], 'index.html')
        with open(output_path, 'r') as f:
            html = f.read()
            assert license_text in html
