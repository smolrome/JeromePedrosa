import re
from pathlib import Path
from datetime import datetime

def debug_visual(completed, total, percentage):
    """Visual debug output for terminal"""
    print("\n" + "═" * 50)
    print("🐛 DEBUG OUTPUT")
    print(f"Completed tasks: {completed}")
    print(f"Total tasks: {total}")
    bar = '🟩' * (percentage//10) + '⬜' * (10 - percentage//10)
    print(f"\nVisual Progress: {bar} {percentage}%")
    print(f"Detailed: |{'✓' * completed}{' ' * (total - completed)}|")
    print("═" * 50 + "\n")

def validate_patterns(content):
    """Test if regex patterns match expected content"""
    print("\n🔍 REGEX VALIDATION:")
    
    # Test progress pattern
    progress_match = re.findall(r'- \[[xX ]\]', content, re.IGNORECASE)
    print(f"Found {len(progress_match)} checklist items")
    
    # Test completed pattern
    completed_match = re.findall(r'- \[[xX]\]', content)
    print(f"Found {len(completed_match)} completed items")
    
    return len(completed_match), len(progress_match)

def file_debug(path):
    """Debug file existence and content"""
    print(f"\n📄 FILE DEBUG: {path}")
    print(f"Exists: {path.exists()}")
    if path.exists():
        print(f"First 3 lines:\n{path.read_text().splitlines()[:3]}")

def main():
    try:
        # Debug: Show current directory
        print(f"\nCurrent directory: {Path.cwd()}")
        
        # File paths
        repo_root = Path(__file__).parent.parent
        progress_file = repo_root / "PROGRESS.md"
        readme_file = repo_root / "README.md"
        
        # Debug files
        file_debug(progress_file)
        file_debug(readme_file)
        
        # Read and validate content
        content = progress_file.read_text()
        completed, total = validate_patterns(content)
        percentage = int((completed / total) * 100) if total > 0 else 0
        
        # Debug visualization
        debug_visual(completed, total, percentage)
        
        # Update README
        readme = readme_file.read_text()
        
        # Debug original progress bar
        progress_match = re.search(r'<img src="https://progress-bar\.dev/(\d+).*?" width="100%"/>', readme)
        if progress_match:
            print(f"Current progress in README: {progress_match.group(1)}%")
        
        # Perform updates
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
        
        # Write changes
        readme_file.write_text(updated)
        print(f"\n✅ Successfully updated to {percentage}%")
        
        # Verify write
        new_content = readme_file.read_text()
        print(f"Updated timestamp: {'Success' if datetime.now().strftime('%Y-%m-%d') in new_content else 'Failed'}")
        print(f"Updated progress bar: {'Success' if f'progress-bar.dev/{percentage}/' in new_content else 'Failed'}")

    except Exception as e:
        print(f"\n🚨 CRITICAL ERROR: {str(e)}")
        print("Debug info above may help identify the issue")
        raise

if __name__ == "__main__":
    print("🚀 Starting progress update script...")
    main()
    print("✨ Script completed")
