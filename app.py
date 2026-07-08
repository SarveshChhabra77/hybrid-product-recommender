# Proxy entry point for Streamlit Cloud
import os
import sys

# Ensure ui/ is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Run the actual streamlit app
with open(os.path.join("ui", "streamlit_app.py"), "r", encoding="utf-8") as f:
    code = f.read()
exec(code, globals())
