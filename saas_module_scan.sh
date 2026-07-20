#!/data/data/com.termux/files/usr/bin/bash

echo "=================================="
echo " SaaS MODULE SCAN"
echo "=================================="

for m in tenant subscription billing trial platform business_type admin permissions
do
    echo
    echo "=============================="
    echo "MODULE: $m"
    echo "=============================="

    if [ -d "src/domains/$m" ]; then
        find src/domains/$m -maxdepth 2 -type f \
        \( -name "*.py" ! -name "*.backup*" ! -name "*.bak" \) | sort

        echo
        echo "--- Classes ---"
        grep -R "^class " src/domains/$m \
        --include="*.py" 2>/dev/null || true

        echo
        echo "--- Functions ---"
        grep -R "^def " src/domains/$m \
        --include="*.py" 2>/dev/null || true

    else
        echo "NOT FOUND"
    fi

done

echo
echo "=================================="
echo "SAAS MODELS"
echo "=================================="

grep -R "^class " src/models \
--include="*.py" 2>/dev/null || true

echo
echo "=================================="
echo "END"
echo "=================================="

