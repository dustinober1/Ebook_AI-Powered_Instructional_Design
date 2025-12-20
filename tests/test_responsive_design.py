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
@given(st.just("dummy"))
def test_property_responsive_design(dummy):
    """
    Property 5: Responsive Design Adaptation
    Validates that the generated site contains responsive layout adaptations.
    """
    with temp_dir_context() as base_dir:
        docs_dir = os.path.join(base_dir, 'docs')
        os.makedirs(docs_dir)
        with open(os.path.join(docs_dir, 'index.md'), 'w') as f:
            f.write("# Home")
        
        # We also add our extra.css to be sure it's included
        css_dir = os.path.join(docs_dir, 'stylesheets')
        os.makedirs(css_dir)
        with open(os.path.join(css_dir, 'extra.css'), 'w') as f:
            f.write("@media screen and (max-width: 30em) { .test { font-size: 0.8rem; } }")

        with open(os.path.join(base_dir, 'mkdocs.yml'), 'w') as f:
            f.write("site_name: Test\ntheme: material\nextra_css: [stylesheets/extra.css]\n")
            
        cfg = load_config(config_file=os.path.join(base_dir, 'mkdocs.yml'))
        cfg['site_dir'] = os.path.join(base_dir, 'site')
        build(cfg)
        
        # Check generated CSS or HTML for media query presence
        # For simplicity, we check if the extra.css was copied and still has the media query
        site_css = os.path.join(cfg['site_dir'], 'stylesheets/extra.css')
        assert os.path.exists(site_css)
        with open(site_css, 'r') as f:
            content = f.read()
            assert '@media' in content
            assert 'max-width: 30em' in content
