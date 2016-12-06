
from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "ProgrammeTest",
    version = "1",
    description = "Votre programme test",
    executables = [Executable("script.py")],
)
