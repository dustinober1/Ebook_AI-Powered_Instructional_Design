import os
import shutil
import tempfile
import json
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

@settings(deadline=10000)
@given(st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pd', 'Zs'))))
def test_property_search_index_integrity(keyword):
    """
    Property 8: Search Functionality and Optimization
    Validates that the search index is generated and contains content keywords.
    """
    with temp_dir_context() as base_dir:
        docs_dir = os.path.join(base_dir, 'docs')
        os.makedirs(docs_dir)
        with open(os.path.join(docs_dir, 'index.md'), 'w') as f:
            f.write(f"# Home\nFind this: {keyword}")
            
        with open(os.path.join(base_dir, 'mkdocs.yml'), 'w') as f:
            f.write("site_name: Test\ntheme: material\nplugins:\n  - search:\n      prebuild_index: true\n")
            
        cfg = load_config(config_file=os.path.join(base_dir, 'mkdocs.yml'))
        cfg['site_dir'] = os.path.join(base_dir, 'site')
        build(cfg)
        
        # Check for search index existence
        index_path = os.path.join(cfg['site_dir'], 'search/search_index.json')
        assert os.path.exists(index_path)
        
        with open(index_path, 'r') as f:
            index_data = json.load(f)
            # Find the entry and check if keyword (or part of it if split) exists
            found = False
            for doc in index_data['docs']:
                if keyword in doc['text']:
                    found = True
                    break
            # Note: separator logic might split keywords, but for simple strings it should work
            if keyword.strip():
                assert found or any(part in str(index_data) for part in keyword.split())

        # Check for UI elements in index.html
        output_path = os.path.join(cfg['site_dir'], 'index.html')
        with open(output_path, 'r') as f:
            html = f.read()
            assert 'role="search"' in html or 'md-search' in html
            assert 'md-search__input' in html
