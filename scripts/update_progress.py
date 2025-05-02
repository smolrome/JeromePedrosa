#!/usr/bin/env python3
import re
from datetime import datetime
from pathlib import Path

def main():
    # File paths
    repo_path = Path(__file__).parent.parent
    progress_file = repo_path / "PROGRESS.md"
    readme_file = repo_path / "README.md"
    
    # Read progress file
    progress_content = progress_file.read_text()
    
    # Calculate completion stats
    completed = len(re.findall(r'- \[X\]', progress_content))
    total = len(re.findall(r'- \[[X ]\]', progress_content))
    percentage = int((completed / total) * 100) if total > 0 else 0
    
    # Update README
    readme_content = readme_file.read_text()
    
    # Update progress bar
    readme_content = re.sub(
        r'!\[Progress\]\(.*\)',
        f'![Progress](https://progress-bar.dev/{percentage}/?title=Overall%20Completion)',
        readme_content
    )
    
    # Update last modified date
    readme_content = re.sub(
        r'\*\*Last Updated:\*\*.*',
        f'**Last Updated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}',
        readme_content
    )
    
    # Write changes
    readme_file.write_text(readme_content)
    print(f"✅ Updated progress: {completed}/{total} ({percentage}%)")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise
