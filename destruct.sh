#!/bin/bash
echo "Wiping app!"
echo "Deleting migrations directory"
rm -rf migrations/
echo "Deleting database file"
rm myapp/myapp.db
echo "Deleting all .pyc files"
echo "find . -name "*.pyc" -exec rm -rf {} \;"
find . -name "*.pyc" -exec rm -rf {} \;