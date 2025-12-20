import yaml
import os

def format_apa7(entry):
    """
    Simple APA 7th Edition formatter for basic entries.
    Template: Author, A. A., & Author, B. B. (Year). Title. Publication. URL
    """
    authors_list = entry['authors']
    if len(authors_list) == 1:
        authors = authors_list[0]
    elif len(authors_list) == 2:
        authors = f"{authors_list[0]} & {authors_list[1]}"
    else:
        authors = ", ".join(authors_list[:-1]) + ", & " + authors_list[-1]
        
    title = entry['title']
    year = entry['year']
    pub = entry.get('publication', '')
    url = entry.get('url', '')
    
    apa = f"{authors} ({year}). *{title}*."
    if pub:
        apa += f" {pub}."
    if url:
        apa += f" {url}"
    
    return apa

def generate_bibliography(yaml_path, output_path):
    if not os.path.exists(yaml_path):
        return
        
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
        
    # Sort by first author's last name
    data.sort(key=lambda x: x['authors'][0].split(",")[0])
    
    with open(output_path, 'w') as f:
        f.write("# Bibliography\n\n")
        f.write("All sources cited in this ebook follow the APA 7th Edition format.\n\n")
        for entry in data:
            f.write(f"- {format_apa7(entry)}\n\n")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    generate_bibliography(
        os.path.join(root_dir, "docs/bibliography.yml"),
        os.path.join(root_dir, "docs/bibliography.md")
    )
