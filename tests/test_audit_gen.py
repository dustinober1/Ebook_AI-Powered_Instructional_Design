import sys
import os
import shutil
import tempfile
import json

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.content_audit import run_audit

def test_audit_dashboard_generation():
    with tempfile.TemporaryDirectory() as tmpdir:
        docs_dir = os.path.join(tmpdir, "docs")
        os.makedirs(docs_dir)
        
        # Create a mock MD file
        with open(os.path.join(docs_dir, "test.md"), 'w') as f:
            f.write("---\ntitle: Test Page\nlast_reviewed: 2025-01-01\nauthors: [Author A]\n---\nContent")
            
        # Create a mock IPYNB file
        nb = {
            "cells": [],
            "metadata": {
                "frontmatter": {
                    "title": "Notebook Page",
                    "last_reviewed": "2024-01-01",
                    "authors": ["Author B"]
                }
            },
            "nbformat": 4,
            "nbformat_minor": 5
        }
        with open(os.path.join(docs_dir, "test.ipynb"), 'w') as f:
            json.dump(nb, f)
            
        output_path = os.path.join(tmpdir, "maintenance.md")
        run_audit(docs_dir, output_path)
        
        assert os.path.exists(output_path)
        with open(output_path, 'r') as f:
            content = f.read()
            assert "Test Page" in content
            assert "Notebook Page" in content
            assert "🚨 Stale" in content or "✅ Fresh" in content
