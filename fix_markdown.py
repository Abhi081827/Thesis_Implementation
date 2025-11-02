#!/usr/bin/env python3
"""
Fix markdown files by removing ```html code blocks around HTML tables.
This allows proper rendering on GitHub.
"""

import os
import re
from pathlib import Path

def fix_markdown_file(file_path):
    """Fix a single markdown file by removing ```html wrappers."""
    print(f"Processing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count occurrences before fixing
    html_blocks = content.count('```html')
    closing_blocks = content.count('```\n\n```html')
    
    if html_blocks == 0:
        print(f"  ✓ No HTML blocks found in {file_path.name}")
        return False
    
    # Remove ```html at the beginning of code blocks
    content = re.sub(r'```html\n', '', content)
    
    # Remove ``` at the end of code blocks (but be careful not to remove other code blocks)
    # Look for ``` followed by either end of file, newlines, or start of new section
    content = re.sub(r'\n```\n\n(?=(<|\n|$))', '\n\n', content)
    content = re.sub(r'\n```\n(?=(<|\n|$))', '\n', content)
    content = re.sub(r'\n```$', '', content)
    
    # Clean up any extra newlines that might have been created
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Write back the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ Fixed {html_blocks} HTML blocks in {file_path.name}")
    return True

def fix_all_markdown_files(directory):
    """Fix all markdown files in a directory."""
    directory = Path(directory)
    
    if not directory.exists():
        print(f"❌ Directory not found: {directory}")
        return
    
    print(f"\n🔧 Fixing markdown files in: {directory}")
    print("=" * 50)
    
    md_files = list(directory.glob("*.md"))
    
    if not md_files:
        print(f"No markdown files found in {directory}")
        return
    
    fixed_count = 0
    for md_file in md_files:
        if fix_markdown_file(md_file):
            fixed_count += 1
    
    print(f"\n✅ Summary: Fixed {fixed_count} out of {len(md_files)} files")

def main():
    """Main function to fix markdown files."""
    print("🚀 Markdown HTML Block Fixer")
    print("Removing ```html wrappers for proper GitHub rendering")
    
    # Fix NanoNet markdown output (main issue)
    fix_all_markdown_files("nanonet_markdown_output")
    
    # Also check other directories just in case
    fix_all_markdown_files("paddle_markdown_output") 
    fix_all_markdown_files("tesseract_markdown_output")
    
    print("\n🎉 All markdown files have been processed!")
    print("💡 Tip: Commit and push these changes to GitHub for proper table rendering.")

if __name__ == "__main__":
    main()