#!/data/data/com.termux/files/usr/bin/bash

echo "========================================"
echo " BUSINESS OS DEPENDENCY SCAN"
echo "========================================"

MODULES="accounting purchase payment customer_finance ai_insight dashboard inventory order invoice supplier receivable"

for m in $MODULES
do
    echo
    echo "================================"
    echo "MODULE : $m"
    echo "================================"

    if [ -d "src/domains/$m" ]; then
        find "src/domains/$m" -maxdepth 2 -type f \
        \( -name "*.py" ! -name "*.backup*" ! -name "*.bak" \) | sort

        echo
        echo "--- Classes ---"
        grep -R "^class " "src/domains/$m" --include="*.py" 2>/dev/null || true

        echo
        echo "--- Functions ---"
        grep -R "^def " "src/domains/$m" --include="*.py" 2>/dev/null || true
    else
        echo "Not Found"
    fi
done

echo
echo "========================================"
echo " MODELS"
echo "========================================"

grep -R "^class " src/models --include="*.py" 2>/dev/null || true

echo
echo "========================================"
echo " END"
echo "========================================"
