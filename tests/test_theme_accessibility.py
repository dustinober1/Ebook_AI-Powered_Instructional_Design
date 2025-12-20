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

@settings(deadline=5000)
@given(st.text(min_size=1, max_size=10, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))))
def test_property_theme_accessibility(dummy_content):
    """
    Property 4: Theme Persistence and Accessibility
    Validates semantic HTML5 tags and theme toggle presence.
    """
    with temp_dir_context() as base_dir:
        docs_dir = os.path.join(base_dir, 'docs')
        os.makedirs(docs_dir)
        with open(os.path.join(docs_dir, 'index.md'), 'w') as f:
            f.write(f"# Home\n{dummy_content}")
            
        with open(os.path.join(base_dir, 'mkdocs.yml'), 'w') as f:
            f.write("site_name: Test\ntheme:\n  name: material\n  palette:\n    - scheme: default\n")
            
        cfg = load_config(config_file=os.path.join(base_dir, 'mkdocs.yml'))
        cfg['site_dir'] = os.path.join(base_dir, 'site')
        build(cfg)
        
        output_path = os.path.join(cfg['site_dir'], 'index.html')
        with open(output_path, 'r') as f:
            html = f.read()
            # Check for semantic tags used by Material theme
            assert '<article' in html
            assert '<nav' in html
            # Check for theme toggle infrastructure (usually an input or a specific class)
            # Material theme uses inputs with id starting with __palette for toggles
            assert '__palette' in html or 'data-md-color-scheme' in html
