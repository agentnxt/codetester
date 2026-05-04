#!/usr/bin/env bash

# 🎥 CodeTester Demo Recorder
# रिकॉर्ड a clean terminal demo using asciinema + agg (GIF generator)

set -e

OUTPUT_DIR="assets"
CAST_FILE="$OUTPUT_DIR/demo.cast"
GIF_FILE="$OUTPUT_DIR/demo-cli.gif"

mkdir -p $OUTPUT_DIR

echo "👉 Starting recording..."
echo "Run your demo commands. Press Ctrl+D when done."

# Record terminal session
asciinema rec $CAST_FILE

echo "👉 Converting to GIF..."

# Convert to GIF (requires agg: https://github.com/asciinema/agg)
agg $CAST_FILE $GIF_FILE \
  --theme monokai \
  --font-size 14 \
  --speed 1.5 \
  --padding 20

echo "✅ Demo GIF generated at $GIF_FILE"

echo "👉 Tips for a great demo:"
echo "- Use a clean project with a failing test"
echo "- Show: run test -> failure -> analyze_and_fix"
echo "- Keep it under 30 seconds"
