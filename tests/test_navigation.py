import os
import shutil
import tempfile
import urllib.parse
from contextlib import contextmanager
from hypothesis import given, strategies as st, settings
from mkdocs.config import load_config
from mkdocs.structure.nav import get_navigation
from mkdocs.structure.files import get_files

@contextmanager
def temp_dir_context():
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)

def create_nested_structure(docs_dir, structure):
    for path in structure:
        full_path = os.path.join(docs_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(f"# {path}\nContent")

@settings(deadline=5000) # Site structure tests can be slow
@given(st.lists(
    st.text(min_size=1, max_size=10, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))).map(lambda s: s + "/index.md"),
    min_size=1, max_size=5, unique=True
))
def test_property_navigation_generation(structure):
    """
    Property 1: Content Organization Consistency (Navigation)
    Validates that the navigation hierarchy correctly reflects the directory structure.
    """
    with temp_dir_context() as base_dir:
        docs_dir = os.path.join(base_dir, 'docs')
        os.makedirs(docs_dir)
        
        # Add index.md if not present
        if 'index.md' not in structure:
            structure.append('index.md')
            
        create_nested_structure(docs_dir, structure)
        
        with open(os.path.join(base_dir, 'mkdocs.yml'), 'w') as f:
            f.write("site_name: Test\n")
            
        cfg = load_config(config_file=os.path.join(base_dir, 'mkdocs.yml'))
        files = get_files(cfg)
        nav = get_navigation(files, cfg)
        
        # Verify that all files in structure are in the navigation
        # We check the URLs as they are more predictable than titles
        # index.md -> ./, dir/index.md -> dir/
        nav_urls = []
        def collect_urls(items):
            for item in items:
                if item.is_page:
                    nav_urls.append(urllib.parse.unquote(item.url))
                elif item.is_section:
                    collect_urls(item.children)
        
        collect_urls(nav.items)
        
        for path in structure:
            expected_url = path.replace('index.md', '').replace('.md', '/')
            if expected_url == '':
                expected_url = '' # Home page is often '' or './'
            
            # Normalize for comparison
            found = any(url.rstrip('/') == expected_url.rstrip('/') for url in nav_urls)
            assert found, f"Path {path} (expected URL prefix {expected_url}) not found in nav URLs: {nav_urls}"
