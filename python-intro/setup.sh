#!/bin/bash
# Python Network Automation Lab Setup Script
# For Cisco IOS/IOS-XE Devices

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║     Python Network Automation Lab Setup (Cisco IOS)          ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "   Please install Python 3.8 or higher from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python found: $(python3 --version)"

# Check Python version is 3.8+
MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 8 ]); then
    echo "❌ Error: Python 3.8 or higher is required"
    echo "   Current version: $PYTHON_VERSION"
    exit 1
fi

# Check for pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed"
    exit 1
fi

echo "✓ pip3 found"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠  Virtual environment already exists"
    read -p "   Remove and recreate? (y/n): " recreate_venv
    if [[ $recreate_venv == "y" || $recreate_venv == "Y" ]]; then
        rm -rf venv
        python3 -m venv venv
        echo "✓ Virtual environment recreated"
    else
        echo "✓ Using existing virtual environment"
    fi
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip -q
echo "✓ pip upgraded"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

# Verify key packages
echo ""
echo "Verifying installation..."
python3 << 'EOF'
import sys
success = True

try:
    import netmiko
    print("  ✓ netmiko installed (version: {})".format(netmiko.__version__))
except ImportError:
    print("  ❌ netmiko not found")
    success = False

try:
    import dotenv
    print("  ✓ python-dotenv installed")
except ImportError:
    print("  ❌ python-dotenv not found")
    success = False

try:
    import paramiko
    print("  ✓ paramiko installed")
except ImportError:
    print("  ❌ paramiko not found")
    success = False

if not success:
    sys.exit(1)
EOF

# Create directory structure
echo ""
echo "Creating directory structure..."

mkdir -p scripts
mkdir -p examples
mkdir -p outputs

touch outputs/.gitkeep

echo "✓ Directories created"

# Move files to appropriate directories if they exist in root
echo ""
echo "Organizing files..."

# Move part*.py files to scripts/ with new naming
if ls part*.py 1> /dev/null 2>&1; then
    for file in part*.py; do
        if [ -f "$file" ]; then
            num=$(echo $file | grep -o '[0-9]\+')
            case $num in
                1) mv "$file" scripts/01_netmiko_basics.py 2>/dev/null || true ;;
                2) mv "$file" scripts/02_env_variables.py 2>/dev/null || true ;;
                3) mv "$file" scripts/03_for_loops.py 2>/dev/null || true ;;
                4) mv "$file" scripts/04_nested_loops.py 2>/dev/null || true ;;
                5) mv "$file" scripts/05_read_write_files.py 2>/dev/null || true ;;
                6) mv "$file" scripts/06_csv_operations.py 2>/dev/null || true ;;
                7) mv "$file" scripts/07_error_handling.py 2>/dev/null || true ;;
                8) mv "$file" scripts/08_functions.py 2>/dev/null || true ;;
                9) mv "$file" scripts/09_concurrent.py 2>/dev/null || true ;;
            esac
        fi
    done
    echo "✓ Scripts moved to scripts/ directory"
fi

# Move CSV and text files to examples/
for file in *.csv *.txt; do
    if [ -f "$file" ] && [ "$file" != "requirements.txt" ]; then
        mv "$file" examples/ 2>/dev/null || true
    fi
done

# Move csv-example.py if exists
if [ -f "csv-example.py" ]; then
    mv csv-example.py scripts/ 2>/dev/null || true
fi

echo "✓ Files organized"

# Setup .env file
echo ""
echo "================================================"
echo "Environment Configuration"
echo "================================================"

if [ -f ".env" ]; then
    echo "✓ .env file already exists"
else
    if [ -f ".env-example" ]; then
        read -p "Create .env file from template? (y/n): " create_env
        if [[ $create_env == "y" || $create_env == "Y" ]]; then
            cp .env-example .env
            echo "✓ .env file created"
            echo ""
            echo "⚠  IMPORTANT: Edit .env file with your Cisco device credentials"
            echo "   nano .env"
        fi
    else
        echo "⚠  No .env-example found, creating template..."
        cat > .env << 'ENVEOF'
# Cisco IOS Device Credentials
USERNAME=admin
PASSWORD=password
ENVEOF
        echo "✓ .env template created"
        echo "⚠  Edit .env with your actual credentials"
    fi
fi

# Verify setup
echo ""
echo "================================================"
echo "Verifying Setup"
echo "================================================"

# Check if we can import netmiko
python3 << 'EOF'
try:
    from netmiko import ConnectHandler
    print("✓ Netmiko import successful")
except Exception as e:
    print(f"❌ Error importing Netmiko: {e}")
    exit(1)
EOF

# Display next steps
echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║                    Setup Complete! ✓                          ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📍 Lab Focus: Cisco IOS/IOS-XE Devices"
echo "🔄 Future Labs: Juniper Junos, Aruba, Arista (Coming Soon)"
echo ""
echo "Next steps:"
echo ""
echo "1. Configure your credentials:"
echo "   nano .env"
echo ""
echo "2. Update device IP in scripts/01_netmiko_basics.py"
echo ""
echo "3. Activate virtual environment (if not already active):"
echo "   source venv/bin/activate"
echo ""
echo "4. Run your first script:"
echo "   python scripts/01_netmiko_basics.py"
echo ""
echo "Quick reference:"
echo "  - Quick Start: cat QUICKSTART.md"
echo "  - Main README: cat README.md"
echo "  - Entry Point: cat START-HERE.md"
echo ""
echo "📚 Platform Support:"
echo "  ✓ Cisco IOS/IOS-XE (this lab)"
echo "  ⏳ Juniper Junos (planned)"
echo "  ⏳ Aruba AOS-CX (planned)"
echo "  ⏳ Arista EOS (planned)"
echo ""
echo "Happy automating! 🚀"
