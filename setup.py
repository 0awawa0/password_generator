from cx_Freeze import setup, Executable


setup(
    name="genpass",
    version="0.1",
    description="Password generator",
    authors="0awawa0",
    executables=[Executable("genpass.py")],
    options={"build_exe": {"include_msvcr": True, "packages": ["pyperclip"]}}
)
