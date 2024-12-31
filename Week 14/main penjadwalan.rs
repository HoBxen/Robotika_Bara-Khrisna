use std::collections::BinaryHeap;
use std::cmp::Ordering;

#[derive(Eq)]
struct Task {
    priority: i32,
    description: String,
}

impl Ord for Task {
    fn cmp(&self, other: &Self) -> Ordering {
        other.priority.cmp(&self.priority) // Reverse order for max-heap
    }
}

impl PartialOrd for Task {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl PartialEq for Task {
    fn eq(&self, other: &Self) -> bool {
        self.priority == other.priority
    }
}

fn main() {
    let mut task_queue = BinaryHeap::new();

    // Menambahkan tugas ke antrean
    task_queue.push(Task {
        priority: 3,
        description: String::from("Mengisi ulang baterai"),
    });

    task_queue.push(Task {
        priority: 5,
        description: String::from("Memeriksa sensor"),
    });

    task_queue.push(Task {
        priority: 1,
        description: String::from("Membersihkan area kerja"),
    });

    task_queue.push(Task {
        priority: 4,
        description: String::from("Mengambil objek"),
    });

    // Menyelesaikan tugas berdasarkan prioritas
    println!("Memulai penjadwalan tugas berdasarkan prioritas:");
    while let Some(task) = task_queue.pop() {
        println!("Menyelesaikan tugas dengan prioritas {}: {}", task.priority, task.description);
    }
}
