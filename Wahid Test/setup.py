import sys
from cx_Freeze import setup, Executable
setup(
	name = "MAIN",
	version = "3.1",
	description = '',
	executables = [Executable('spriteGroup.py', base = "Win32GUI")]
	)