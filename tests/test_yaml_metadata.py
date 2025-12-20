import os
import shutil
import tempfile
from contextlib import contextmanager
import yaml
from hypothesis import given, strategies as st, settings
from mkdocs.config import load_config
from mkdocs.structure.pages import Page

@contextmanager
def temp_dir_context():
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)

def create_mock_page_with_metadata(docs_dir, filename, metadata):
    page_path = os.path.join(docs_dir, filename)
    os.makedirs(os.path.dirname(page_path), exist_ok=True)
    with open(page_path, 'w') as f:
        f.write("---\n")
        f.write(yaml.dump(metadata))
        f.write("---\n")
        f.write("# Test Title\nContent")

@settings(deadline=2000)
@given(st.fixed_dictionaries({
    'title': st.text(min_size=1),
    'description': st.text(),
    'tags': st.lists(st.text()),
    'difficulty': st.sampled_from(["Beginner", "Intermediate", "Advanced"]),
    'reading_time': st.integers(min_value=1)
}))
def test_property_yaml_front_matter_processing(metadata):
    """
    Property 1: Content Organization Consistency (Metadata)
    Validates that YAML front-matter is correctly formatted and can be parsed.
    """
    with temp_dir_context() as base_dir:
        docs_dir = os.path.join(base_dir, 'docs')
        os.makedirs(docs_dir)
        
        filename = 'test_page.md'
        create_mock_page_with_metadata(docs_dir, filename, metadata)
        
        with open(os.path.join(docs_dir, filename), 'r') as f:
            content = f.read()
            assert content.startswith("---")
            # Extract YAML part
            parts = content.split("---")
            assert len(parts) >= 3
            yaml_part = parts[1]
            data = yaml.safe_load(yaml_part)
            
            for key in metadata:
                assert data[key] == metadata[key]
