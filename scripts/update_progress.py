from pathlib import Path
from datetime import datetime
import re

def main():
    repo_root = Path(__file__).parent.parent
    progress_file = repo_root / "PROGRESS.md"
    readme_file = repo_root / "README.md"
    
    try:
        # Read files
        progress = progress_file.read_text()
        readme = readme_file.read_text()
        
        # Calculate progress
        completed = len(re.findall(r'- \[X\]', progress))
        total = len(re.findall(r'- \[[X ]\]', progress))
        percent = int((completed/total)*100) if total > 0 else 0
        
        # Update README
        updated = re.sub(
            r'!\[Progress\]\(.*\)',
            f'![Progress](https://progress-bar.dev/{percent}/?title=Progress)',
            readme
        )
        updated = re.sub(
            r'Last Updated:.*',
            f'Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
            updated
        )
        
        # Write back
        readme_file.write_text(updated)
        print(f"Updated {completed}/{total} ({percent}%)")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
