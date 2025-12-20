import os
import shutil
import tempfile
from contextlib import contextmanager
import pytest
from hypothesis import given, strategies as st, settings
from mkdocs.commands.build import build
from mkdocs.config import load_config

@contextmanager
def temp_dir_context():
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)

def create_mock_site(base_dir, pages):
    docs_dir = os.path.join(base_dir, 'docs')
    os.makedirs(docs_dir, exist_ok=True)
    
    # Create mkdocs.yml
    config_path = os.path.join(base_dir, 'mkdocs.yml')
    with open(config_path, 'w') as f:
        f.write("site_name: Test Site\n")
        f.write("theme: material\n")
        f.write("nav:\n")
        for title, filename in pages.items():
            f.write(f"  - {title}: {filename}\n")
    
    # Create pages
    for title, filename in pages.items():
        page_path = os.path.join(docs_dir, filename)
        os.makedirs(os.path.dirname(page_path), exist_ok=True)
        with open(page_path, 'w') as f:
            f.write(f"# {title}\n\nContent for {title}")

@settings(deadline=2000)
@given(st.dictionaries(
    st.text(min_size=1, max_size=10, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
    st.text(min_size=1, max_size=10, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))).map(lambda s: s + ".md"),
    min_size=1, max_size=5
))
def test_property_basic_site_generation(pages):
    """
    Property 1: Content Organization Consistency
    Validates that the site builds correctly for various flat navigation structures.
    """
    with temp_dir_context() as base_dir:
        site_dir = tempfile.mkdtemp(dir=base_dir)
        create_mock_site(site_dir, pages)
        
        # Try to load config and build
        try:
            cfg = load_config(config_file=os.path.join(site_dir, 'mkdocs.yml'))
            cfg['site_dir'] = os.path.join(site_dir, 'site')
            build(cfg)
            
            # Verify generated files exist
            for title, filename in pages.items():
                html_filename = filename.replace('.md', '/index.html')
                if filename == 'index.md':
                    html_filename = 'index.html'
                
                output_path = os.path.join(cfg['site_dir'], html_filename)
                assert os.path.exists(output_path), f"Generated file {output_path} not found"
                
        finally:
            if os.path.exists(site_dir):
                shutil.rmtree(site_dir)
