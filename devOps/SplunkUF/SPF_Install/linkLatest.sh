#!/bin/bash

# Iterate over each splunk*{.deb,.rpm,.tgz,.deb.md5,.rpm.md5,.tgz.md5} file in the current directory
for file in splunk*{.deb,.rpm,.tgz,.deb.md5,.rpm.md5,.tgz.md5}; do
    # Skip if no matching files are found
    [ -e "$file" ] || continue
    
    # Simple regex to extract base name and extension
    if [[ "$file" =~ ^(splunk|splunkforwarder)-.*\.(deb|rpm|tgz)(\.md5)?$ ]]; then
        b1="${BASH_REMATCH[1]}"   # Extract base name (splunk or splunkforwarder)
        ext="${BASH_REMATCH[2]}"          # Extract extension (deb, rpm, tgz)

        # If the file ends with .md5, remove the md5 suffix to determine the extension
        if [[ "$file" == *.md5 ]]; then
            base_name="latest-${b1}.${ext}.md5"
        else
            base_name="latest-${b1}.${ext}"
        fi
        
        # Unlink existing symlink if it exists
        if [ -L "$base_name" ]; then
            unlink "$base_name"
            echo "Unlinked existing symlink: $base_name"
        fi

        # Prevent overwriting actual files like .deb, .rpm
        if [ ! -e "$base_name" ]; then
            # Create the symlink to 'latest' if it doesn't already exist
            ln -sf "$file" "./${base_name}"
            echo "Created symlink: ${base_name} -> $file"
        else
            echo "Skipping symlink creation for $base_name as it already exists as a regular file."
        fi
    else
        echo "Skipping file: $file (doesn't match expected pattern)"
    fi
done
