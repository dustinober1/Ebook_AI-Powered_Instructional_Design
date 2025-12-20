import os
import yaml
import datetime
import frontmatter

def get_status(last_reviewed_val):
    if not last_reviewed_val:
        return "⚠️ Unknown"
    
    if isinstance(last_reviewed_val, datetime.date):
        last_reviewed = last_reviewed_val
    else:
        try:
            last_reviewed = datetime.datetime.strptime(str(last_reviewed_val), '%Y-%m-%d').date()
        except ValueError:
            return "❌ Invalid Date"
        
    today = datetime.date.today()
    age_days = (today - last_reviewed).days
    
    if age_days < 180: # 6 months
        return "✅ Fresh"
    elif age_days < 365: # 1 year
        return "🕒 Needs Review"
    else:
        return "🚨 Stale"

def run_audit(docs_dir, output_path):
    audit_data = []
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(('.md', '.ipynb')):
                relative_path = os.path.relpath(os.path.join(root, file), docs_dir)
                abs_path = os.path.join(root, file)
                
                try:
                    if file.endswith('.md'):
                        post = frontmatter.load(abs_path)
                        metadata = post.metadata
                    else: # ipynb
                        import json
                        with open(abs_path, 'r') as f:
                            nb = json.load(f)
                            # Looking for metadata in top-level or first markdown cell
                            metadata = nb.get('metadata', {}).get('frontmatter', {})
                    
                    title = metadata.get('title', file)
                    last_reviewed = metadata.get('last_reviewed', '')
                    authors = metadata.get('authors', [])
                    
                    audit_data.append({
                        'title': title,
                        'path': relative_path,
                        'last_reviewed': last_reviewed,
                        'status': get_status(last_reviewed),
                        'authors': ", ".join(authors) if isinstance(authors, list) else str(authors)
                    })
                except Exception as e:
                    print(f"Error auditing {file}: {e}")

    # Sort by path
    audit_data.sort(key=lambda x: x['path'])
    
    with open(output_path, 'w') as f:
        f.write("# Content Maintenance Dashboard\n\n")
        f.write("This page tracks the review status of all ebook content based on the `last_reviewed` metadata field.\n\n")
        f.write("| Page | Last Reviewed | Status | Authors |\n")
        f.write("| --- | --- | --- | --- |\n")
        for item in audit_data:
            f.write(f"| {item['title']} | {item['last_reviewed']} | {item['status']} | {item['authors']} |\n")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    run_audit(
        os.path.join(root_dir, "docs"),
        os.path.join(root_dir, "docs/maintenance.md")
    )
