import sys
import os
import shutil
import tempfile
import yaml

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generate_bib import generate_bibliography

def test_bibliography_generation():
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_path = os.path.join(tmpdir, "bib.yml")
        md_path = os.path.join(tmpdir, "bib.md")
        
        data = [
            {
                'id': 'a',
                'authors': ['Alpha, A.'],
                'title': 'Alpha Title',
                'year': 2020
            },
            {
                'id': 'b',
                'authors': ['Beta, B.'],
                'title': 'Beta Title',
                'year': 2021
            }
        ]
        
        with open(yaml_path, 'w') as f:
            yaml.dump(data, f)
            
        generate_bibliography(yaml_path, md_path)
        
        assert os.path.exists(md_path)
        with open(md_path, 'r') as f:
            content = f.read()
            assert "Alpha Title" in content
            assert "Beta Title" in content
            assert "# Bibliography" in content
