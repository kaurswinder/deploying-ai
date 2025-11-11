#!/usr/bin/env python3
"""
Main entry point for the Assignment Chat application.
Run this file to start the Gradio interface.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from assignment_chat.interface import main

if __name__ == "__main__":
    main()
