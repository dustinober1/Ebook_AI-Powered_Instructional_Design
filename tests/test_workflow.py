import os
import yaml

def test_ci_workflow_exists():
    workflow_path = ".github/workflows/ci.yml"
    assert os.path.exists(workflow_path), f"Workflow file {workflow_path} not found"

def test_ci_workflow_valid_yaml():
    workflow_path = ".github/workflows/ci.yml"
    with open(workflow_path, 'r') as f:
        try:
            data = yaml.safe_load(f)
            assert data['name'] == 'CI/CD Pipeline'
            assert 'jobs' in data
        except yaml.YAMLError as e:
            pytest.fail(f"CI workflow is not a valid YAML: {e}")
