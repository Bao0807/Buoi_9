

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
MOVE_DIRS = [(-1, 0, "U"), (1, 0, "D"), (0, -1, "L"), (0, 1, "R")]
MAX_DEPTH = 50


def get_neighbors(state):
	"""Lay cac trang thai ke va huong di UDLR"""
	zero_index = state.index(0)
	zx, zy = divmod(zero_index, 3)
	neighbors = []
	for dx, dy, move in MOVE_DIRS:
		nx, ny = zx + dx, zy + dy
		if 0 <= nx < 3 and 0 <= ny < 3:
			swap_index = nx * 3 + ny
			new_state = list(state)
			new_state[zero_index], new_state[swap_index] = new_state[swap_index], new_state[zero_index]
			neighbors.append((tuple(new_state), move))
	return neighbors


def is_solvable(state):
	"""Kiem tra trang thai co giai duoc khong"""
	flat = [n for n in state if n != 0]
	inversions = 0
	for i in range(len(flat)):
		for j in range(i + 1, len(flat)):
			if flat[i] > flat[j]:
				inversions += 1
	return inversions % 2 == 0


def dfs(start_state):
	"""DFS tim duong di va nuoc di"""
	if start_state == GOAL_STATE:
		return [start_state], []
	if not is_solvable(start_state):
		return None

	stack = [(start_state, 0)]
	explored = {start_state}
	parent = {start_state: None}
	parent_move = {start_state: None}

	while stack:
		node, depth = stack.pop()
		if depth >= MAX_DEPTH:
			continue
		neighbors = get_neighbors(node)
		for child, move in reversed(neighbors):
			if child not in explored:
				parent[child] = node
				parent_move[child] = move
				if child == GOAL_STATE:
					return build_path(parent, parent_move, child)
				explored.add(child)
				stack.append((child, depth + 1))
	return None


def build_path(parent, parent_move, goal_state):
	"""Truy vet lai duong di va chuoi nuoc di"""
	path = []
	moves = []
	current = goal_state
	while current is not None:
		path.append(current)
		move = parent_move[current]
		if move is not None:
			moves.append(move)
		current = parent[current]
	path.reverse()
	moves.reverse()
	return path, moves


