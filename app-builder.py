# Under Developement to build platform-specific exe
# from __future__ import annotations
# from cx_Freeze import Executable, setup

# setup(
#     name="voice-translator",
#     version="v0.0.0",
#     description="Real-Time Voice Translator GUI",
#     executables=[Executable("main.py", icon="icon.ico", target_name="voice-translator.exe")],
#     options={
#         "build_exe": {
#             "include_files": [("icon.png")],
#             "zip_include_packages": ["env/"],
#             "zip_exclude_packages": []
#         }
#     },
# )