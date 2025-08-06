#!/bin/bash

# Convert standalone .md files to Hugo page bundles
# This script converts files like content/pg/alter-type.md to content/pg/alter-type/index.md

set -e

# Define the content directory
CONTENT_DIR="content/pg"

# Counter for processed files
COUNT=0

echo "Starting conversion of standalone .md files to Hugo page bundles..."
echo "Working in directory: $CONTENT_DIR"
echo ""

# Find all .md files in the content/pg directory (excluding index files and files already in bundles)
find "$CONTENT_DIR" -maxdepth 1 -type f -name "*.md" | while read -r file; do
    # Get the base name without extension
    basename=$(basename "$file" .md)
    
    # Skip _index files (section pages)
    if [[ "$basename" == "_index" || "$basename" == "_index.en" ]]; then
        continue
    fi
    
    # Skip if it's the featured.jpg placeholder
    if [[ "$basename" == "featured" ]]; then
        continue
    fi
    
    # Create the target directory
    target_dir="$CONTENT_DIR/$basename"
    
    # Check if directory already exists
    if [ -d "$target_dir" ]; then
        echo "⚠️  Directory already exists: $target_dir (skipping)"
        continue
    fi
    
    # Create the directory
    mkdir -p "$target_dir"
    
    # Move the file to index.md in the new directory
    mv "$file" "$target_dir/index.md"
    
    echo "✓ Converted: $file → $target_dir/index.md"
    ((COUNT++))
done

echo ""
echo "Conversion complete! Processed $COUNT files."
echo ""

# List remaining standalone .md files (for verification)
REMAINING=$(find "$CONTENT_DIR" -maxdepth 1 -type f -name "*.md" ! -name "_index*.md" 2>/dev/null | wc -l)
if [ "$REMAINING" -gt 0 ]; then
    echo "Remaining standalone .md files:"
    find "$CONTENT_DIR" -maxdepth 1 -type f -name "*.md" ! -name "_index*.md"
else
    echo "All standalone .md files have been converted to page bundles."
fi