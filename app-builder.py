import PyInstaller.__main__
import sys
import os
import shutil

script_name = "voice-translator-system.py"
icon_file = "icon.ico"
asset_files = "icon.png"

add_data_option = f"{asset_files};."

PyInstaller.__main__.run([
    "--name=voice-translator",                # Name of the executable
    f"--icon={icon_file}",                    # Icon for the executable
    "--onefile",                              # Pack everything into one file
    "--windowed",                             # No console window for GUI applications
    f"--add-data={add_data_option}",          # Add asset files
    script_name                               # Your main script
])

dist_folder = os.path.join(os.getcwd(), "dist")

if not os.path.exists(dist_folder):
    os.makedirs(dist_folder)

icon_dest = os.path.join(dist_folder, icon_file)
asset_dest = os.path.join(dist_folder, asset_files)

if os.path.exists(icon_file):
    shutil.copy(icon_file, "dist")
    print(f"Icon copied to: {icon_dest}")
else:
    print(f"Icon file '{icon_file}' not found.")

if os.path.exists(asset_files):
    shutil.copy(asset_files, "dist")
    print(f"asset_files copied to: {asset_dest}")
else:
    print(f"Icon file '{asset_files}' not found.")

print("Build completed! Check the 'dist' directory.")
