#!/bin/bash

if [ ! -d "./venv" ]; then
	python3 -m venv venv
	./venv/bin/pip3 install -r ./requirements.txt
fi

CURRENT_DIR=$(pwd)

# Create the mkreport file with dynamic content
cat <<EOF >split_by_silence
#!/bin/bash

PROJECT_DIR=$CURRENT_DIR

\$PROJECT_DIR/venv/bin/python3 \$PROJECT_DIR/main.py "\$@"
EOF

# Move the executable file to the user's local bin
mkdir -p ~/.local/bin
mv split_by_silence ~/.local/bin/

# Make mkreport executable
chmod +x ~/.local/bin/split_by_silence

echo "Installed successfully to ~/.local/bin/split_by_silence"
