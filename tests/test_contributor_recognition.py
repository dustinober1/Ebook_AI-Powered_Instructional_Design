import os
import shutil
import tempfile
import frontmatter
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
@given(st.lists(st.text(min_size=1, max_size=20, alphabet=st.sampled_from("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ")), min_size=1, max_size=3))
def test_property_contributor_recognition(authors):
    """
    Property 11.2: Contributor Recognition
    Validates that authors specified in metadata are recognized in output.
    """
    # Filter out empty or whitespace-only names
    authors = [a.strip() for a in authors if a.strip()]
    if not authors:
        return

    with temp_dir_context() as base_dir:
        docs_dir = os.path.join(base_dir, 'docs')
        os.makedirs(docs_dir)
        
        # Create page with authors
        page_content = f"---\ntitle: Test\nauthors: {authors}\n---\nContent"
        with open(os.path.join(docs_dir, 'index.md'), 'w') as f:
            f.write(page_content)
            
        with open(os.path.join(base_dir, 'mkdocs.yml'), 'w') as f:
            f.write("site_name: Test\ntheme: material\n")
            
        cfg = load_config(config_file=os.path.join(base_dir, 'mkdocs.yml'))
        cfg['site_dir'] = os.path.join(base_dir, 'site')
        build(cfg)
        
        # Verify via our audit script
        import sys
        sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))
        from content_audit import run_audit
        audit_md = os.path.join(base_dir, 'maintenance.md')
        run_audit(docs_dir, audit_md)
        
        with open(audit_md, 'r') as f:
            audit_content = f.read()
            for author in authors:
                # We check for author, handling common whitespace replacements if any
                assert author in audit_content or author.replace('\xa0', ' ') in audit_content
