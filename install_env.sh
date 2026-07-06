# Check if proot-distro is installed
if ! command -v proot-distro &> /dev/null; then
    pkg install proot-distro -y
fi

# Install Ubuntu to run Docker (Standard procedure for Termux)
proot-distro install ubuntu
echo "Run 'proot-distro login ubuntu' to enter the environment, then install docker inside."
