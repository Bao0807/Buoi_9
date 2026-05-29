import heapq


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
MOVE_DIRS = [(-1, 0, "U"), (1, 0, "D"), (0, -1, "L"), (0, 1, "R")]


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



def ucs(start_state):
	"""Chay UCS tu trang thai bat dau va tra ve (duong di, nuoc di, cost)."""
	if start_state == GOAL_STATE:
		return [start_state], [], 0
	if not is_solvable(start_state):
		return None

	frontier = []
	heapq.heappush(frontier, (0, start_state))
	best_cost = {start_state: 0}
	parent = {start_state: None}
	parent_move = {start_state: None}

	while frontier:
		cost, node = heapq.heappop(frontier)
		if node == GOAL_STATE:
			path, moves = build_path(parent, parent_move, node)
			return path, moves, cost
		if cost != best_cost.get(node):
			continue
		for child, move in get_neighbors(node):
			new_cost = cost + 1
			if new_cost < best_cost.get(child, float("inf")):
				best_cost[child] = new_cost
				parent[child] = node
				parent_move[child] = move
				heapq.heappush(frontier, (new_cost, child))
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
