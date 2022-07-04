#!/bin/bash
# This script converts the .dot graphviz into an image
fname="my_input_sample"
dot -Tsvg ${fname}.dot -o ${fname}.svg || \
  echo "This script requires graphviz. Install it on a Mac with: " \
  echo "  brew install graphviz"
