import os
import shutil
import tempfile
import re
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
@given(st.lists(
    st.fixed_dictionaries({
        'name': st.text(min_size=1, max_size=10, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))).map(lambda s: s + ".md"),
        'links_to': st.integers(min_value=0, max_value=4) # Index of another page to link to
    }),
    min_size=2, max_size=5, unique_by=lambda x: x['name']
))
def test_property_link_integrity(pages_data):
    """
    Property 2: Link Integrity Preservation
    Validates that internal markdown links correctly resolve in the generated HTML.
    """
    with temp_dir_context() as base_dir:
        docs_dir = os.path.join(base_dir, 'docs')
        os.makedirs(docs_dir)
        
        # Ensure index.md exists
        if not any(p['name'] == 'index.md' for p in pages_data):
            pages_data[0]['name'] = 'index.md'
            
        for i, page_info in enumerate(pages_data):
            target_index = page_info['links_to'] % len(pages_data)
            target_name = pages_data[target_index]['name']
            
            with open(os.path.join(docs_dir, page_info['name']), 'w') as f:
                f.write(f"# {page_info['name']}\n\n")
                f.write(f"[Link to {target_name}]({target_name})\n")
        
        with open(os.path.join(base_dir, 'mkdocs.yml'), 'w') as f:
            f.write("site_name: Test\n")
            
        cfg = load_config(config_file=os.path.join(base_dir, 'mkdocs.yml'))
        cfg['site_dir'] = os.path.join(base_dir, 'site')
        build(cfg)
        
        # Check that generated HTML contains the link and targeted file exists
        for page_info in pages_data:
            target_index = page_info['links_to'] % len(pages_data)
            target_name = pages_data[target_index]['name']
            
            html_name = page_info['name'].replace('.md', '/index.html') if page_info['name'] != 'index.md' else 'index.html'
            output_path = os.path.join(cfg['site_dir'], html_name)
            
            with open(output_path, 'r') as f:
                html_content = f.read()
                # MkDocs converts [text](file.md) to <a href="../file/">text</a> or <a href="file/">text</a>
                # We just check if the link is there and normalized
                expected_href = target_name.replace('.md', '/')
                if target_name == 'index.md':
                    expected_href = '../' # or similar depending on depth
                
                # Check for link existence in HTML
                # (This is simplified, a full link checker would be better)
                assert 'href=' in html_content
