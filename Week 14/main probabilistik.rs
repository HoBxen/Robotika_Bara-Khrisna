use rand::Rng;
use std::collections::HashMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Point {
    x: i32,
    y: i32,
}

impl Point {
    fn new(x: i32, y: i32) -> Self {
        Point { x, y }
    }

    fn distance(&self, other: &Point) -> f64 {
        (((self.x - other.x).pow(2) + (self.y - other.y).pow(2)) as f64).sqrt()
    }
}

struct Robot {
    position: Point,
    goal: Point,
    probabilities: HashMap<Point, f64>,
}

impl Robot {
    fn new(start: Point, goal: Point) -> Self {
        Robot {
            position: start,
            goal,
            probabilities: HashMap::new(),
        }
    }

    fn update_probabilities(&mut self, grid: &Vec<Vec<i32>>) {
        self.probabilities.clear();
        let mut rng = rand::thread_rng();

        for (i, row) in grid.iter().enumerate() {
            for (j, &cell) in row.iter().enumerate() {
                if cell == 0 { // Hanya jalan bebas
                    let noise: f64 = rng.gen_range(0.8..1.2); // Tambahkan ketidakpastian
                    let point = Point::new(i as i32, j as i32);
                    let base_probability = 1.0 / (self.position.distance(&point) + 1.0);
                    self.probabilities.insert(point, base_probability * noise);
                }
            }
        }
    }

    fn choose_next_move(&self) -> Option<Point> {
        self.probabilities
            .iter()
            .filter(|(&point, _)| point != self.position)
            .max_by(|a, b| a.1.partial_cmp(b.1).unwrap())
            .map(|(&point, _)| point)
    }

    fn move_to(&mut self, next_position: Point) {
        println!("Bergerak dari {:?} ke {:?}", self.position, next_position);
        self.position = next_position;
    }

    fn reached_goal(&self) -> bool {
        self.position == self.goal
    }
}

fn main() {
    let grid = vec![
        vec![0, 0, 1, 0, 0],
        vec![1, 0, 1, 0, 1],
        vec![0, 0, 0, 0, 0],
        vec![0, 1, 1, 1, 0],
        vec![0, 0, 0, 0, 0],
    ];

    let start = Point::new(0, 0);
    let goal = Point::new(4, 4);
    let mut robot = Robot::new(start, goal);

    while !robot.reached_goal() {
        robot.update_probabilities(&grid);
        if let Some(next_move) = robot.choose_next_move() {
            robot.move_to(next_move);
        } else {
            println!("Tidak ada jalur yang memungkinkan menuju tujuan.");
            break;
        }
    }

    if robot.reached_goal() {
        println!("Robot telah mencapai tujuan di {:?}", robot.goal);
    }
}
