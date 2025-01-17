def get_neighbors(node, grid):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Atas, bawah, kiri, kanan
    for d in directions:
        neighbor = (node[0] + d[0], node[1] + d[1])
        if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]] == 0:
            neighbors.append(neighbor)
    return neighbors

def a_star(start, goal, grid):
    open_list = []  # Daftar node yang perlu diperiksa
    closed_list = set()  # Daftar node yang sudah diperiksa
    open_list.append(start)  # Tambahkan node awal ke open_list

    g = {start: 0}  # Menyimpan jarak dari start ke node saat ini
    f = {start: heuristic(start, goal)}  # Menyimpan nilai f (cost + heuristic)

    came_from = {}  # Melacak jalur

    while open_list:  # Selama ada node di open list
        current = min(open_list, key=lambda x: f[x])  # Ambil node dengan nilai f terendah

        if current == goal:  # Jika mencapai tujuan
            path = []  # Jalur kosong untuk menyimpan hasil
            while current in came_from:  # Bangun jalur dari goal ke start
                path.append(current)
                current = came_from[current]  # Kembali ke node sebelumnya
            path.append(start)  # Tambahkan node awal
            return path[::-1]  # Kembalikan jalur terbalik
        open_list.remove(current)  # Hapus node saat ini dari open_list
        closed_list.add(current)  # Tambahkan node ke closed_list

        for neighbor in get_neighbors(current, grid):  # Periksa tetangga
            if neighbor in closed_list:  # Lewati jika sudah diperiksa
                continue

            tentative_g = g[current] + 1  # Hitung jarak sementara
            if neighbor not in open_list:  # Jika tetangga belum ada di open_list
                open_list.append(neighbor)  # Tambahkan ke open_list
            elif tentative_g >= g.get(neighbor, float('inf')):  # Jika jarak lebih besar
                continue

            came_from[neighbor] = current  # Melacak dari mana tetangga berasal
            g[neighbor] = tentative_g  # Perbarui jarak
            f[neighbor] = g[neighbor] + heuristic(neighbor, goal)  # Hitung nilai f
    return []  # Kembalikan jalur kosong jika tidak ditemukan

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Menghitung jarak Manhattan

# Contoh grid
grid = [
    [0, 1, 0, 0],
    [0, 1, 0, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 0]
]

path = a_star((0, 0), (3, 3), grid)  # Memanggil fungsi A* untuk mencari jalur
print("Path:", path)  # Menampilkan jalur yang ditemukan
