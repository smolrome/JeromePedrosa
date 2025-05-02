import re
from pathlib import Path
from datetime import datetime

def calculate_progress():
    progress_file = Path("PROGRESS.md")
    content = progress_file.read_text()
    
    # Count all checklist items
    total = len(re.findall(r'- \[[xX ]\]', content, re.IGNORECASE))
    completed = len(re.findall(r'- \[[xX]\]', content))
    
    # Calculate percentage (avoid division by zero)
    percentage = int((completed / total) * 100) if total > 0 else 0
    return percentage

def update_readme(percentage):
    readme = Path("README.md")
    content = readme.read_text()
    
    # Corrected regex pattern (fixed quotes and spacing)
    new_content = re.sub(
        r'<img src="https://progress-bar\.dev/\d+.*" width="100%"/>',
        f'<img src="https://progress-bar.dev/{percentage}/?title=Overall%20Completion" width="100%"/>',
        content
    )
    
    # Update timestamp
    new_content = re.sub(
        r'\*\*Last Updated:\*\*.*',
        f'**Last Updated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}',
        new_content
    )
    
    readme.write_text(new_content)

if __name__ == "__main__":
    progress = calculate_progress()
    update_readme(progress)
    print(f"Updated progress to {progress}%")
