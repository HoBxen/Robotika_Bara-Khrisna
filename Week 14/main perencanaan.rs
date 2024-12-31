use std::collections::VecDeque;

#[derive(Debug, Clone, Copy)]
struct Point {
    x: usize,
    y: usize,
}

fn is_valid(x: isize, y: isize, grid: &Vec<Vec<i32>>, visited: &Vec<Vec<bool>>) -> bool {
    let rows = grid.len() as isize;
    let cols = grid[0].len() as isize;
    x >= 0 && y >= 0 && x < rows && y < cols && grid[x as usize][y as usize] == 0 && !visited[x as usize][y as usize]
}

fn find_path(grid: Vec<Vec<i32>>, start: Point, goal: Point) -> Option<Vec<Point>> {
    let directions = vec![(0, 1), (1, 0), (0, -1), (-1, 0)];
    let mut visited = vec![vec![false; grid[0].len()]; grid.len()];
    let mut queue = VecDeque::new();
    let mut parent = vec![vec![None; grid[0].len()]; grid.len()];

    queue.push_back(start);
    visited[start.x][start.y] = true;

    while let Some(current) = queue.pop_front() {
        if current.x == goal.x && current.y == goal.y {
            let mut path = vec![];
            let mut p = Some(current);

            while let Some(point) = p {
                path.push(Point { x: point.x, y: point.y });
                p = parent[point.x][point.y];
            }

            path.reverse();
            return Some(path);
        }

        for (dx, dy) in &directions {
            let new_x = current.x as isize + dx;
            let new_y = current.y as isize + dy;

            if is_valid(new_x, new_y, &grid, &visited) {
                let new_x = new_x as usize;
                let new_y = new_y as usize;

                visited[new_x][new_y] = true;
                queue.push_back(Point { x: new_x, y: new_y });
                parent[new_x][new_y] = Some(current);
            }
        }
    }

    None
}

fn main() {
    let grid = vec![
        vec![0, 0, 1, 0, 0],
        vec![1, 0, 1, 0, 1],
        vec![0, 0, 0, 0, 0],
        vec![0, 1, 1, 1, 0],
        vec![0, 0, 0, 0, 0],
    ];

    let start = Point { x: 0, y: 0 };
    let goal = Point { x: 4, y: 4 };

    match find_path(grid, start, goal) {
        Some(path) => {
            println!("Jalur ditemukan:");
            for point in path {
                println!("({}, {})", point.x, point.y);
            }
        }
        None => println!("Tidak ada jalur yang ditemukan."),
    }
}
