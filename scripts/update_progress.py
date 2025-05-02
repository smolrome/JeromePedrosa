import re
from pathlib import Path
from datetime import datetime

def main():
    # File paths
    repo_root = Path(__file__).parent.parent
    progress_file = repo_root / "PROGRESS.md"
    readme_file = repo_root / "README.md"
    
    try:
        # Calculate progress
        content = progress_file.read_text()
        completed = len(re.findall(r'- \[[xX]\]', content))
        total = len(re.findall(r'- \[[xX ]\]', content, re.IGNORECASE))
        percentage = int((completed / total) * 100) if total > 0 else 0

        # Update README
        readme = readme_file.read_text()
        updated = re.sub(
            r'<img src="https://progress-bar\.dev/\d+.*?" width="100%"/>',
            f'<img src="https://progress-bar.dev/{percentage}/?title=Overall%20Completion" width="100%"/>',
            readme
        )
        updated = re.sub(
            r'\*\*Last Updated:\*\*.*',
            f'**Last Updated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}',
            updated
        )
        
        readme_file.write_text(updated)
        print(f"Success! Updated to {percentage}%")

    except Exception as e:
        print(f"🚨 Error: {e}")
        raise

if __name__ == "__main__":
    main()
