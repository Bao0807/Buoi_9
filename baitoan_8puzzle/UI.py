import random
import customtkinter as ctk
from tkinter import Canvas, Listbox, Scrollbar

from . import AStar
from . import BFS
from . import DFS
from . import Greedy
from . import IDS
from . import SimpleHillClimbing
from . import UCS


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def is_solvable(state):
	"""Kiem tra trang thai co giai duoc khong"""
	flat = [n for n in state if n != 0]
	inversions = 0
	for i in range(len(flat)):
		for j in range(i + 1, len(flat)):
			if flat[i] > flat[j]:
				inversions += 1
	return inversions % 2 == 0


def random_state():
	"""Sinh trang thai ngau nhien hop le"""
	state = list(GOAL_STATE)
	while True:
		random.shuffle(state)
		candidate = tuple(state)
		if is_solvable(candidate) and candidate != GOAL_STATE:
			return candidate


class PuzzleApp(ctk.CTk):
	def __init__(self):
		"""Khoi tao giao dien"""
		super().__init__()
		self.title("8-Puzzle BFS/DFS/IDS/UCS/Greedy/A*/Hill Climbing")
		self.minsize(560, 420)
		self.resizable(True, True)

		self.current_state = GOAL_STATE
		self.solution_path = []
		self.solution_moves = []
		self.anim_index = 0
		self.selected_algo = ctk.StringVar(value="BFS")

		main_frame = ctk.CTkFrame(self)
		main_frame.pack(padx=10, pady=10, fill="both", expand=True)

		left_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
		left_frame.pack(side="left", padx=(0, 8), pady=6, fill="both", expand=True)

		right_frame = ctk.CTkFrame(main_frame)
		right_frame.pack(side="right", padx=(8, 0), pady=6, fill="y")

		top_left = ctk.CTkFrame(left_frame, fg_color="transparent")
		top_left.pack(fill="x")

		self.canvas = Canvas(top_left, width=330, height=330, bg="#f6f4ef", highlightthickness=0)
		self.canvas.pack(pady=(6, 4), fill="both", expand=True)

		self.status_label = ctk.CTkLabel(top_left, text="Ready")
		self.status_label.pack(pady=(4, 6))

		bottom_left = ctk.CTkFrame(left_frame)
		bottom_left.pack(padx=6, pady=(2, 6), fill="both", expand=True)

		ctk.CTkLabel(bottom_left, text="State list").pack(pady=(6, 2))
		list_container = ctk.CTkFrame(bottom_left, fg_color="transparent")
		list_container.pack(padx=6, pady=(0, 6), fill="both", expand=True)

		self.state_list = Listbox(list_container, height=8, activestyle="dotbox")
		self.state_list.pack(side="left", fill="both", expand=True)
		scrollbar = Scrollbar(list_container, command=self.state_list.yview)
		scrollbar.pack(side="right", fill="y")
		self.state_list.config(yscrollcommand=scrollbar.set)

		controls = ctk.CTkFrame(right_frame)
		controls.pack(pady=(6, 4), padx=8)

		self.input_entry = ctk.CTkEntry(controls, width=220, placeholder_text="1 2 3 4 5 6 7 8 0")
		self.input_entry.grid(row=0, column=0, columnspan=2, padx=8, pady=4)

		self.apply_button = ctk.CTkButton(controls, text="Apply State", command=self.apply_state)
		self.apply_button.grid(row=1, column=0, padx=8, pady=4, sticky="ew")

		self.random_button = ctk.CTkButton(controls, text="Random", command=self.set_random_state)
		self.random_button.grid(row=1, column=1, padx=8, pady=4, sticky="ew")

		self.reset_button = ctk.CTkButton(controls, text="Reset", command=self.reset)
		self.reset_button.grid(row=2, column=0, columnspan=2, padx=8, pady=4, sticky="ew")

		algo_frame = ctk.CTkFrame(right_frame)
		algo_frame.pack(pady=4, padx=8)

		ctk.CTkLabel(algo_frame, text="Algorithm:").grid(row=0, column=0, padx=6, pady=4)
		self.algo_menu = ctk.CTkOptionMenu(
			algo_frame,
			values=["BFS", "DFS", "IDS", "UCS", "Greedy", "A*", "Hill Climbing"],
			variable=self.selected_algo,
		)
		self.algo_menu.grid(row=0, column=1, padx=6, pady=4, sticky="ew")

		self.solve_button = ctk.CTkButton(right_frame, text="Solve", command=self.solve)
		self.solve_button.pack(pady=(4, 6), padx=8, fill="x")

		self.moves_label = ctk.CTkLabel(right_frame, text="Moves: ", wraplength=220, justify="left")
		self.moves_label.pack(pady=(2, 8), padx=8, fill="x")

		self.bind("<Configure>", self.on_resize)
		self.draw_board(self.current_state)
		self.update_entry_from_state()

	def on_resize(self, _event):
		"""Ve lai ban co khi doi kich thuoc cua so."""
		state = self.current_state
		if self.solution_path and self.anim_index > 0:
			index = min(self.anim_index - 1, len(self.solution_path) - 1)
			state = self.solution_path[index]
		self.draw_board(state)

	def reset(self):
		"""Dat lai trang thai mac dinh"""
		self.current_state = GOAL_STATE
		self.solution_path = []
		self.solution_moves = []
		self.anim_index = 0
		self.status_label.configure(text="Ready")
		self.moves_label.configure(text="Moves: ")
		self.update_state_list([])
		self.draw_board(self.current_state)
		self.update_entry_from_state()

	def update_entry_from_state(self):
		"""Cap nhat o nhap theo trang thai"""
		self.input_entry.delete(0, "end")
		self.input_entry.insert(0, " ".join(str(n) for n in self.current_state))

	def apply_state(self):
		"""Doc o nhap va cap nhat trang thai"""
		text = self.input_entry.get().strip()
		parts = [p for p in text.replace(",", " ").split() if p]
		try:
			numbers = [int(p) for p in parts]
		except ValueError:
			self.status_label.configure(text="Invalid input")
			return

		if len(numbers) != 9 or set(numbers) != set(range(9)):
			self.status_label.configure(text="Need 9 numbers: 0-8")
			return

		self.current_state = tuple(numbers)
		self.solution_path = []
		self.solution_moves = []
		self.anim_index = 0
		self.status_label.configure(text="State updated")
		self.moves_label.configure(text="Moves: ")
		self.update_state_list([])
		self.draw_board(self.current_state)

	def set_random_state(self):
		"""Chon trang thai ngau nhien"""
		self.current_state = random_state()
		self.solution_path = []
		self.solution_moves = []
		self.anim_index = 0
		self.status_label.configure(text="Random state")
		self.moves_label.configure(text="Moves: ")
		self.update_state_list([])
		self.draw_board(self.current_state)
		self.update_entry_from_state()

	def solve(self):
		"""Giai theo thuat toan da chon"""
		self.apply_state()
		if self.status_label.cget("text") in {"Invalid input", "Need 9 numbers: 0-8"}:
			return
		self.status_label.configure(text="Solving...")
		self.update_idletasks()

		algo = self.selected_algo.get()
		result = None
		if algo == "BFS":
			result = BFS.bfs(self.current_state)
		elif algo == "DFS":
			result = DFS.dfs(self.current_state)
		elif algo == "IDS":
			result = IDS.ids(self.current_state)
		elif algo == "UCS":
			result = UCS.ucs(self.current_state)
		elif algo == "Greedy":
			result = Greedy.greedy_search(self.current_state)
		elif algo == "A*":
			result = AStar.a_star(self.current_state)
		elif algo == "Hill Climbing":
			result = SimpleHillClimbing.simple_hill_climbing(self.current_state)

		if not result:
			self.status_label.configure(text="No solution (or depth limit)")
			return

		if algo == "IDS":
			path, moves, limit = result
			self.status_label.configure(text=f"Steps: {len(path) - 1} | Depth limit: {limit}")
		elif algo == "UCS":
			path, moves, cost = result
			self.status_label.configure(text=f"Steps: {len(path) - 1} | Cost: {cost}")
		elif algo == "DFS":
			path, moves = result
			self.status_label.configure(text=f"Steps: {len(path) - 1} | Max depth: {DFS.MAX_DEPTH}")
		elif algo == "Greedy":
			path, moves = result
			self.status_label.configure(text=f"Steps: {len(path) - 1}")
		elif algo == "A*":
			path, moves, cost = result
			self.status_label.configure(text=f"Steps: {len(path) - 1} | f: {cost}")
		elif algo == "Hill Climbing":
			path, moves, solved = result
			if solved:
				self.status_label.configure(text=f"Steps: {len(path) - 1}")
			else:
				self.status_label.configure(text=f"Stopped at local optimum | Steps: {len(path) - 1}")
		else:
			path, moves = result
			self.status_label.configure(text=f"Steps: {len(path) - 1}")

		self.solution_path = path
		self.solution_moves = moves
		self.anim_index = 0
		self.moves_label.configure(text=f"Moves: {''.join(moves)}")
		self.update_state_list(path)
		self.animate()

	def update_state_list(self, path):
		"""Cap nhat danh sach trang thai co the cuon xem."""
		self.state_list.delete(0, "end")
		for idx, state in enumerate(path):
			state_text = " ".join(str(n) for n in state)
			self.state_list.insert("end", f"Step {idx}: {state_text}")

	def animate(self):
		"""Chay tung buoc"""
		if self.anim_index >= len(self.solution_path):
			return
		state = self.solution_path[self.anim_index]
		self.draw_board(state)
		self.anim_index += 1
		self.after(250, self.animate)

	def draw_board(self, state):
		"""Ve ban co"""
		self.canvas.delete("all")
		canvas_width = max(self.canvas.winfo_width(), 1)
		canvas_height = max(self.canvas.winfo_height(), 1)
		board_size = min(canvas_width, canvas_height)
		tile_size = max(int(board_size / 3), 1)
		padding = max(int(tile_size * 0.08), 4)
		font_size = max(int(tile_size * 0.45), 12)
		for i, value in enumerate(state):
			row, col = divmod(i, 3)
			x0 = col * tile_size + padding
			y0 = row * tile_size + padding
			x1 = x0 + tile_size - padding
			y1 = y0 + tile_size - padding
			if value != 0:
				self.canvas.create_rectangle(x0, y0, x1, y1, fill="#d8b384", outline="#8d6e52", width=2)
				self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(value), font=("Arial", font_size, "bold"))
			else:
				self.canvas.create_rectangle(x0, y0, x1, y1, fill="#f6f4ef", outline="#e0d8cf", width=2)
