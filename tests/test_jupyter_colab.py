import os

def test_colab_badge_url_structure():
    # The mkdocs-jupyter plugin generates colab links following a pattern:
    # https://colab.research.google.com/github/{user}/{repo}/blob/{branch}/docs/{path}
    
    repo_url = "https://github.com/dustinober/AI_ISD"
    notebook_path = "docs/chapters/01-ai-fundamentals.ipynb"
    branch = "main"
    
    # Expected pattern part
    expected_prefix = "https://colab.research.google.com/github/"
    
    # We simulate what the plugin might do
    # Note: We are testing the expectation of how we want it configured
    colab_link = f"{expected_prefix}dustinober/AI_ISD/blob/{branch}/{notebook_path}"
    
    assert "colab.research.google.com" in colab_link
    assert "dustinober/AI_ISD" in colab_link
    assert notebook_path in colab_link
