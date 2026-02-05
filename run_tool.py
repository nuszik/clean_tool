import streamlit.web.cli as stcli
import os, sys

def resolve_path(path):
    resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path

if __name__ == "__main__":
    # This tells Streamlit to run your specific script
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("your_clean_script.py"), # Replace with your actual filename
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())
