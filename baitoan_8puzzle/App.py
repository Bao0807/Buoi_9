import os
import sys
import customtkinter as ctk

if __package__ is None:
	sys.path.append(os.path.dirname(os.path.dirname(__file__)))
	from baitoan_8puzzle.UI import PuzzleApp
else:
	from .UI import PuzzleApp


def main():
	ctk.set_appearance_mode("light")
	ctk.set_default_color_theme("blue")
	app = PuzzleApp()
	app.mainloop()


if __name__ == "__main__":
	main()
