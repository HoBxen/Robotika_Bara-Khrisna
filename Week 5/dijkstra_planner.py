import heapq  # Mengimpor heapq untuk menggunakan heap (antrian prioritas)

def dijkstra(graph, start, goal):
    queue = [(0, start, [])]  # Inisialisasi antrian dengan biaya 0, titik awal, dan path kosong
    seen = set()  # Menyimpan node yang sudah diproses
    min_distance = {start: 0}  # Menyimpan jarak minimum dari start ke setiap node

    while queue:  # Selama ada node dalam antrian
        (cost, v1, path) = heapq.heappop(queue)  # Ambil node dengan biaya terendah
        if v1 in seen:  # Jika node sudah diproses, lanjutkan
            continue

        path = path + [v1]  # Tambahkan node saat ini ke jalur
        if v1 == goal:  # Jika sudah mencapai tujuan, kembalikan biaya dan jalur
            return cost, path

        seen.add(v1)  # Tandai node ini sudah diproses
        for v2, c in graph[v1].items():  # Periksa tetangga dari node saat ini
            if v2 in seen:  # Jika tetangga sudah diproses, lewati
                continue
            prev = min_distance.get(v2, None)  # Ambil jarak minimum sebelumnya ke tetangga
            next_cost = cost + c  # Hitung biaya baru ke tetangga
            if prev is None or next_cost < prev:  # Jika lebih baik dari yang sebelumnya
                min_distance[v2] = next_cost  # Perbarui jarak minimum
                heapq.heappush(queue, (next_cost, v2, path))  # Tambahkan ke antrian

    return float("inf"), []  # Jika tidak ada jalur ditemukan

# Contoh graf yang merepresentasikan ruang bebas
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

# Memanggil fungsi dijkstra dengan titik awal 'A' dan tujuan 'D'
cost, path = dijkstra(graph, 'A', 'D')
print("Cost:", cost)  # Menampilkan total biaya
print("Path:", path)  # Menampilkan jalur yang dilalui