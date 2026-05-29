

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
MOVE_DIRS = [(-1, 0, "U"), (1, 0, "D"), (0, -1, "L"), (0, 1, "R")]
MAX_DEPTH = 30


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


def make_node(state, parent, move, depth):
	"""Tao node cho DLS"""
	return {"state": state, "parent": parent, "move": move, "depth": depth}


def is_cycle(node):
	"""Kiem tra chu trinh theo duong cha"""
	state = node["state"]
	current = node["parent"]
	while current is not None:
		if current["state"] == state:
			return True
		current = current["parent"]
	return False


def depth_limited_search(start_state, limit):
	"""DLS dung stack (LIFO) va tra ve node/cutoff/failure"""
	frontier = [make_node(start_state, None, None, 0)]
	cutoff_occurred = False

	while frontier:
		node = frontier.pop()
		if node["state"] == GOAL_STATE:
			return node
		if node["depth"] > limit:
			cutoff_occurred = True
			continue
		if is_cycle(node):
			continue
		neighbors = get_neighbors(node["state"])
		for child_state, move in reversed(neighbors):
			child = make_node(child_state, node, move, node["depth"] + 1)
			frontier.append(child)

	if cutoff_occurred:
		return "cutoff"
	return None


def ids(start_state):
	"""IDS tim duong di va nuoc di"""
	if start_state == GOAL_STATE:
		return [start_state], [], 0
	if not is_solvable(start_state):
		return None

	for limit in range(MAX_DEPTH + 1):
		result = depth_limited_search(start_state, limit)
		if result == "cutoff":
			continue
		if result is None:
			return None
		path, moves = build_path_from_node(result)
		return path, moves, limit
	return None


def build_path_from_node(goal_node):
	"""Truy vet lai duong di va chuoi nuoc di"""
	path = []
	moves = []
	current = goal_node
	while current is not None:
		path.append(current["state"])
		if current["move"] is not None:
			moves.append(current["move"])
		current = current["parent"]
	path.reverse()
	moves.reverse()
	return path, moves


