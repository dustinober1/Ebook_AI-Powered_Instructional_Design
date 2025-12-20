# AI-Powered Instructional Design

> **An open-source ebook exploring the intersection of Artificial Intelligence and Instructional Design (ID).**

This repository contains the source code and content for the *AI-Powered Instructional Design* ebook. It is built as a modern, accessible web book using **MkDocs** and **Material for MkDocs**.

## 📚 About the Book

As we move into the "Third Wave" of AI in education, the role of the Instructional Designer is shifting from creator to architect. This book serves as both a strategic guide and a technical manual for modern IDs who want to leverage AI for:
- Hyper-personalized learning experiences.
- Automated content generation and orchestration.
- Advanced prompt engineering (RACE, Chain-of-Thought).
- Data-driven learning analytics.

## 🚀 Features

- **Premium Reading Experience**: Built with the *Material for MkDocs* theme, featuring custom Typography and Layouts.
- **Dark & Light Mode**: Fully accessible themes for any reading environment.
- **Responsive Design**: Optimizes automatically for mobile, tablet, and desktop.
- **Search & Navigation**: Instant search across all chapters, glossary, and references.
- **PDF Generation**: Automatically compiles the entire book into a PDF for offline reading.

## 🛠️ Technology Stack

- **Core**: [MkDocs](https://www.mkdocs.org/)
- **Theme**: [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- **PDF**: [mkdocs-with-pdf](https://github.com/gpoulin/mkdocs-with-pdf)

## 🏁 Getting Started

### Prerequisites
- Python 3.9 or higher
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dustinober/AI_ISD.git
   cd AI_ISD
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally

To view the ebook on your local machine with live-reloading:

```bash
mkdocs serve
```

Open your browser to `http://127.0.0.1:8000`.

### Building for Production

To build the static site (html/css/js):

```bash
mkdocs build
```
The output will be in the `site/` directory.

## 📂 Project Structure

```
├── docs/
│   ├── assets/            # Images and Covers
│   ├── chapters/          # Main ebook content (Markdown)
│   ├── stylesheets/       # Custom CSS
│   ├── index.md           # Landing page
│   ├── glossary.md        # Glossary of Terms
│   └── bibliography.md    # References
├── .github/               # CI/CD Workflows
├── mkdocs.yml             # Site configuration
└── requirements.txt       # Python dependencies
```

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for details.
