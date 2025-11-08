#!/bin/bash
# Wrapper script to run Python with correct environment

# Activate pyenv
eval "$(pyenv init -)"
pyenv shell 3.12.11

# Run the comparison script
python3 compare_preprocessing.py "$@"
