#!/usr/bin/env python3
"""Patch cli.py to load KeyboardHotkeyListener"""

with open('nemo/core/cli.py', 'r') as f:
    lines = f.readlines()

# Find the line with "raise ImportError("Could not load four_button_interface")"
insert_index = None
for i, line in enumerate(lines):
    if 'raise ImportError("Could not load four_button_interface")' in line:
        insert_index = i
        break

if insert_index:
    # Insert KeyboardHotkeyListener loading after that
    new_code = '''         
         # Load keyboard_hotkeys for better Windows support
         spec_kb = importlib.util.spec_from_file_location(
             "keyboard_hotkeys",
             str(systems_path / "keyboard_hotkeys.py")
         )
         KeyboardHotkeyListener = None
         if spec_kb and spec_kb.loader:
             try:
                 kb_module = importlib.util.module_from_spec(spec_kb)
                 spec_kb.loader.exec_module(kb_module)
                 KeyboardHotkeyListener = kb_module.KeyboardHotkeyListener
             except:
                 pass
'''
    
    lines.insert(insert_index + 1, new_code)
    
    with open('nemo/core/cli.py', 'w') as f:
        f.writelines(lines)
    
    print("✓ Added KeyboardHotkeyListener loading to CLI")
else:
    print("✗ Could not find insertion point")
