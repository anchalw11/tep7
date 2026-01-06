#!/bin/bash

# Google Analytics tag to add
GTAG_CODE='<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NTYR4QELSE"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('\''js'\'', new Date());

  gtag('\''config'\'', '\''G-NTYR4QELSE'\'');
</script>'

# Find all HTML files and add the Google Analytics tag
find . -name "*.html" -type f | while read -r file; do
    echo "Processing $file..."

    # Check if the file already has the Google Analytics tag
    if grep -q "G-NTYR4QELSE" "$file"; then
        echo "  Already has Google Analytics tag, skipping..."
        continue
    fi

    # Use sed to add the Google Analytics tag after <head>
    # Create a backup and modify in place
    sed -i.bak "/^<head>/a\\
$GTAG_CODE" "$file"

    # Check if the tag was added successfully
    if grep -q "G-NTYR4QELSE" "$file"; then
        echo "  Added Google Analytics tag to $file"
        # Remove backup file
        rm "$file.bak"
    else
        echo "  Warning: Could not add Google Analytics tag to $file"
        # Restore from backup
        mv "$file.bak" "$file"
    fi
done

echo "Google Analytics tag addition completed!"
