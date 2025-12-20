import os

def test_community_files_exist():
    """
    Task 11.1: Verify presence of governance documentation.
    """
    assert os.path.exists("CONTRIBUTING.md")
    assert os.path.exists(".github/ISSUE_TEMPLATE/bug_report.md")
    assert os.path.exists(".github/ISSUE_TEMPLATE/content_suggestion.md")

def test_contributing_content():
    with open("CONTRIBUTING.md", "r") as f:
        content = f.read()
        assert "Local Development Setup" in content
        assert "Pull Request Process" in content
        assert "APA 7th Edition" in content
