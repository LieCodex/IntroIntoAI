from __future__ import annotations

import heapq
from dataclasses import dataclass

import matplotlib.pyplot as plt


GRID_SIZE = 10
CELL_DISTANCE_MILES = 10.0
TOTAL_CELLS = GRID_SIZE * GRID_SIZE


PLACE_NAMES = [
	"Davao City",
	"Panabo",
	"Tagum",
	"Mati",
	"Digos",
	"Samal",
	"Bansalan",
	"Padada",
	"Malalag",
	"Sulop",
	"Midsayap",
	"Kidapawan",
	"Kabacan",
	"Makilala",
	"Matalam",
	"Pigcawayan",
	"Libungan",
	"Alamada",
	"Carmen (Cotabato)",
	"Tulunan",
	"General Santos",
	"Koronadal",
	"Polomolok",
	"Surallah",
	"Tupi",
	"Tampakan",
	"Lake Sebu",
	"Sto. Nino (South Cotabato)",
	"Norala",
	"Banga (South Cotabato)",
	"Cagayan de Oro",
	"Iligan",
	"Malaybalay",
	"Valencia (Bukidnon)",
	"Manolo Fortich",
	"Talakag",
	"Don Carlos",
	"Maramag",
	"Quezon (Bukidnon)",
	"Kitaotao",
	"Zamboanga City",
	"Pagadian",
	"Dipolog",
	"Dapitan",
	"Ipil",
	"Molave",
	"Aurora (Zamboanga del Sur)",
	"Ramon Magsaysay (ZDS)",
	"Tukuran",
	"Kumalarang",
	"Butuan",
	"Bayugan",
	"Cabadbaran",
	"Surigao City",
	"Bislig",
	"Tandag",
	"Cortes (Surigao del Sur)",
	"Lianga",
	"Hinatuan",
	"Tagbina",
	"Cotabato City",
	"Marawi",
	"Lamitan",
	"Isabela City",
	"Jolo",
	"Bongao",
	"Parang (Maguindanao)",
	"Datu Odin Sinsuat",
	"Buluan",
	"Sultan Kudarat (Maguindanao)",
	"Gingoog",
	"El Salvador (Misamis Oriental)",
	"Ozamiz",
	"Tangub",
	"Oroquieta",
	"Plaridel (Misamis Occidental)",
	"Jimenez",
	"Aloran",
	"Bonifacio (MisOcc)",
	"Clarin (MisOcc)",
	"Compostela",
	"Nabunturan",
	"Monkayo",
	"Maco",
	"Mawab",
	"Pantukan",
	"New Bataan",
	"Maragusan",
	"Laak",
	"Mabini (Davao de Oro)",
	"Digos (Davao del Sur)",
	"Sta. Cruz (Davao del Sur)",
	"Hagonoy (Davao del Sur)",
	"Matanao",
	"Kiblawan",
	"Magsaysay (Davao del Sur)",
	"Malita",
	"Santa Maria (Davao Occidental)",
	"Don Marcelino",
]


@dataclass(frozen=True)
class Cell:
	row: int
	col: int


def build_grid_places() -> list[list[str]]:
	filled_places = PLACE_NAMES[:TOTAL_CELLS]
	if len(filled_places) < TOTAL_CELLS:
		for idx in range(len(filled_places), TOTAL_CELLS):
			filled_places.append(f"Mindanao Place {idx + 1}")

	return [
		filled_places[row * GRID_SIZE : (row + 1) * GRID_SIZE]
		for row in range(GRID_SIZE)
	]


def heuristic(a: Cell, b: Cell) -> float:
	return (abs(a.row - b.row) + abs(a.col - b.col)) * CELL_DISTANCE_MILES


def neighbors(cell: Cell) -> list[Cell]:
	adjacent = []
	directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
	for d_row, d_col in directions:
		next_row = cell.row + d_row
		next_col = cell.col + d_col
		if 0 <= next_row < GRID_SIZE and 0 <= next_col < GRID_SIZE:
			adjacent.append(Cell(next_row, next_col))
	return adjacent


def a_star(start: Cell, goal: Cell) -> tuple[list[Cell], float]:
	open_heap: list[tuple[float, int, Cell]] = []
	counter = 0
	heapq.heappush(open_heap, (0.0, counter, start))

	came_from: dict[Cell, Cell] = {}
	g_score: dict[Cell, float] = {start: 0.0}

	while open_heap:
		_, _, current = heapq.heappop(open_heap)
		if current == goal:
			path = reconstruct_path(came_from, current)
			return path, g_score[current]

		for nxt in neighbors(current):
			tentative = g_score[current] + CELL_DISTANCE_MILES
			if tentative < g_score.get(nxt, float("inf")):
				came_from[nxt] = current
				g_score[nxt] = tentative
				counter += 1
				f_score = tentative + heuristic(nxt, goal)
				heapq.heappush(open_heap, (f_score, counter, nxt))

	return [], float("inf")


def reconstruct_path(came_from: dict[Cell, Cell], current: Cell) -> list[Cell]:
	path = [current]
	while current in came_from:
		current = came_from[current]
		path.append(current)
	path.reverse()
	return path


def display_grid_index(grid: list[list[str]]) -> None:
	print("\n10x10 Mindanao Grid (index -> place)")
	print("=" * 70)
	for row in range(GRID_SIZE):
		entries = []
		for col in range(GRID_SIZE):
			idx = row * GRID_SIZE + col
			entries.append(f"{idx:02d}:{grid[row][col][:12]:12}")
		print("  ".join(entries))
	print("=" * 70)


def get_user_choice(grid: list[list[str]], prompt: str) -> Cell:
	while True:
		raw = input(prompt).strip()
		if raw.isdigit():
			idx = int(raw)
			if 0 <= idx < GRID_SIZE * GRID_SIZE:
				return Cell(idx // GRID_SIZE, idx % GRID_SIZE)

		normalized = raw.lower()
		for row in range(GRID_SIZE):
			for col in range(GRID_SIZE):
				place = grid[row][col].lower()
				if normalized == place:
					return Cell(row, col)

		print("Invalid input. Use a valid index (0-99) or exact place name.")


def short_label(name: str) -> str:
	name = name.replace("(", "").replace(")", "")
	if len(name) <= 8:
		return name
	return name[:8]


def visualize(grid: list[list[str]], path: list[Cell], start: Cell, goal: Cell, miles: float) -> None:
	fig, ax = plt.subplots(figsize=(11, 11))
	ax.set_xlim(-0.5, GRID_SIZE - 0.5)
	ax.set_ylim(GRID_SIZE - 0.5, -0.5)
	ax.set_xticks(range(GRID_SIZE))
	ax.set_yticks(range(GRID_SIZE))
	ax.set_title("A* Pathfinding on 10x10 Mindanao Grid")
	ax.grid(True, which="major", color="black", linewidth=0.8)

	for row in range(GRID_SIZE):
		for col in range(GRID_SIZE):
			label = short_label(grid[row][col])
			ax.text(col, row, label, ha="center", va="center", fontsize=6)

	if path:
		x_coords = [cell.col for cell in path]
		y_coords = [cell.row for cell in path]
		ax.plot(x_coords, y_coords, color="blue", linewidth=2.5, marker="o", markersize=4)

	ax.scatter(start.col, start.row, color="green", s=130, label="Start", zorder=3)
	ax.scatter(goal.col, goal.row, color="red", s=130, label="Destination", zorder=3)
	ax.legend(loc="upper left")

	start_name = grid[start.row][start.col]
	goal_name = grid[goal.row][goal.col]
	ax.set_xlabel(
		f"Route: {start_name} -> {goal_name} | Total Distance: {miles:.1f} miles"
	)

	plt.tight_layout()
	plt.show()


def main() -> None:
	grid = build_grid_places()
	print("A* 10x10 Grid Navigation (Mindanao Cities/Municipalities)")
	print(f"Each move to an adjacent cell = {CELL_DISTANCE_MILES} miles")

	display_grid_index(grid)

	start = get_user_choice(grid, "Enter START index (0-99) or exact place name: ")
	goal = get_user_choice(grid, "Enter DESTINATION index (0-99) or exact place name: ")

	path, miles = a_star(start, goal)
	if not path:
		print("No path found.")
		return

	print("\nComputed path:")
	for step in path:
		print(f"- {grid[step.row][step.col]} ({step.row},{step.col})")
	print(f"\nTotal distance: {miles:.1f} miles")

	visualize(grid, path, start, goal, miles)


if __name__ == "__main__":
	main()
