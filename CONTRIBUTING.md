# Contributing to AI-Powered Instructional Design

Thank you for your interest in contributing to this open-source ebook! We welcome contributions to content, code, accessibility, and design.

## Local Development Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/dustinober/AI_ISD.git
    cd AI_ISD
    ```
2.  **Set up Virtual Environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Mac/Linux
    # .venv\Scripts\activate   # Windows
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run Dev Server**:
    ```bash
    mkdocs serve
    ```
    Access the site at `http://127.0.0.1:8000`.

## Content Guidelines

- **Format**: All chapters should be written in Markdown (`.md`) or Jupyter Notebooks (`.ipynb`).
- **Metadata**: Each chapter must include YAML front-matter (see `docs/template_chapter.md`).
- **Style**: Follow APA 7th Edition for all citations. Use a professional yet accessible tone.
- **Images**: Use descriptive alt-text for all images to ensure accessibility.

## Pull Request Process

1.  **Create a Branch**: Use descriptive names like `content/ai-ethics` or `fix/nav-issue`.
2.  **Verify Changes**: Run the test suite before submitting:
    ```bash
    pytest tests/
    ```
3.  **Submit PR**: Provide a clear description of your changes. Ensure CI checks pass.
4.  **Review**: A maintainer will review your PR. Address feedback promptly.

## Code of Conduct

We are committed to fostering a welcoming and inclusive community. Please be respectful in all interactions.
