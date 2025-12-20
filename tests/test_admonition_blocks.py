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

import html

@settings(deadline=5000)
@given(st.sampled_from(["note", "warning", "tip", "info"]), st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pd', 'Zs'))))
def test_property_admonition_rendering(type, content):
    """
    Property 6: Admonition Block Rendering
    Validates that admonition blocks render with appropriate visual styling classes.
    """
    with temp_dir_context() as base_dir:
        docs_dir = os.path.join(base_dir, 'docs')
        os.makedirs(docs_dir)
        with open(os.path.join(docs_dir, 'index.md'), 'w') as f:
            f.write(f"!!! {type}\n    {content}")
            
        with open(os.path.join(base_dir, 'mkdocs.yml'), 'w') as f:
            f.write("site_name: Test\ntheme: material\nmarkdown_extensions:\n  - admonition\n  - pymdownx.details\n  - pymdownx.superfences\n")
            
        cfg = load_config(config_file=os.path.join(base_dir, 'mkdocs.yml'))
        cfg['site_dir'] = os.path.join(base_dir, 'site')
        build(cfg)
        
        output_path = os.path.join(cfg['site_dir'], 'index.html')
        with open(output_path, 'r') as f:
            html_content = f.read()
            # MkDocs Admonition extension uses 'admonition' class and type name as class
            assert 'admonition' in html_content
            assert type in html_content
            # Check for escaped content, stripped to avoid whitespace issues
            assert html.escape(content.strip()) in html_content
