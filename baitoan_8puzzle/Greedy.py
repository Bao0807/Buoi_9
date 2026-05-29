import heapq


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
MOVE_DIRS = [(-1, 0, "U"), (1, 0, "D"), (0, -1, "L"), (0, 1, "R")]
GOAL_POS = {value: idx for idx, value in enumerate(GOAL_STATE)}


def get_neighbors(state):
	"""Tra ve cac trang thai ke va nuoc di tu trang thai hien tai."""
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
	"""Kiem tra trang thai 8-puzzle co the giai duoc hay khong."""
	flat = [n for n in state if n != 0]
	inversions = 0
	for i in range(len(flat)):
		for j in range(i + 1, len(flat)):
			if flat[i] > flat[j]:
				inversions += 1
	return inversions % 2 == 0


def manhattan(state):
	"""Tinh heuristic Manhattan cho trang thai."""
	distance = 0
	for idx, value in enumerate(state):
		if value == 0:
			continue
		goal_idx = GOAL_POS[value]
		x1, y1 = divmod(idx, 3)
		x2, y2 = divmod(goal_idx, 3)
		distance += abs(x1 - x2) + abs(y1 - y2)
	return distance


def greedy_search(start_state):
	"""Greedy search (Best-First) voi heuristic Manhattan."""
	if start_state == GOAL_STATE:
		return [start_state], []
	if not is_solvable(start_state):
		return None

	frontier = []
	counter = 0
	heapq.heappush(frontier, (manhattan(start_state), counter, start_state))
	parent = {start_state: None}
	parent_move = {start_state: None}
	reached = set()

	while frontier:
		_, _, node = heapq.heappop(frontier)
		if node in reached:
			continue
		if node == GOAL_STATE:
			return build_path(parent, parent_move, node)
		reached.add(node)
		for child, move in get_neighbors(node):
			if child in reached or child in parent:
				continue
			parent[child] = node
			parent_move[child] = move
			counter += 1
			heapq.heappush(frontier, (manhattan(child), counter, child))
	return None


def build_path(parent, parent_move, goal_state):
	"""Truy vet lai duong di va chuoi nuoc di tu cac bang parent."""
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
