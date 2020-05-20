import os
cmd = """
osascript -e 'tell application "System Events" to keystroke " "' 
"""
# minimize active window
os.system(cmd)