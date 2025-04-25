#!/bin/bash

# Navigate to the directory
cd docs/SPL_searches

# Process each .txt file
for file in *.txt; do
  if [ -f "$file" ]; then
    # Get the base name without extension
    base_name="${file%.txt}"
    
    # Create new .md file
    echo "### ${base_name//_/ } Examples" > "${base_name}.md"
    echo "" >> "${base_name}.md"
    echo '```' >> "${base_name}.md"
    cat "$file" >> "${base_name}.md"
    echo '```' >> "${base_name}.md"
    
    # Remove the original .txt file
    rm "$file"
    
    echo "Converted $file to ${base_name}.md"
  fi
done

echo "Conversion complete!" 