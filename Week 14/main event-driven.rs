use std::collections::VecDeque;

#[derive(Debug, Clone, Copy)]
struct Point {
    x: i32,
    y: i32,
}

impl Point {
    fn new(x: i32, y: i32) -> Self {
        Point { x, y }
    }
}

#[derive(Debug)]
enum Event {
    ObstacleDetected(Point),
    GoalChanged(Point),
    Idle,
}

struct Robot {
    position: Point,
    goal: Point,
}

impl Robot {
    fn new(start: Point, goal: Point) -> Self {
        Robot { position: start, goal }
    }

    fn handle_event(&mut self, event: Event) {
        match event {
            Event::ObstacleDetected(obstacle) => {
                println!("Rintangan terdeteksi di {:?}, menghindar!", obstacle);
                self.avoid_obstacle(obstacle);
            }
            Event::GoalChanged(new_goal) => {
                println!("Tujuan berubah ke {:?}, bergerak ke tujuan baru!", new_goal);
                self.goal = new_goal;
                self.move_to_goal();
            }
            Event::Idle => {
                println!("Tidak ada perubahan, tetap di posisi.");
            }
        }
    }

    fn avoid_obstacle(&mut self, obstacle: Point) {
        // Menghindari rintangan secara sederhana dengan bergerak ke arah berbeda
        if self.position.x == obstacle.x {
            self.position.y += 1;
        } else {
            self.position.x += 1;
        }
        println!("Posisi setelah menghindar: {:?}", self.position);
    }

    fn move_to_goal(&mut self) {
        println!("Bergerak ke tujuan dari posisi {:?} ke {:?}", self.position, self.goal);
        while self.position.x != self.goal.x || self.position.y != self.goal.y {
            if self.position.x < self.goal.x {
                self.position.x += 1;
            } else if self.position.x > self.goal.x {
                self.position.x -= 1;
            }

            if self.position.y < self.goal.y {
                self.position.y += 1;
            } else if self.position.y > self.goal.y {
                self.position.y -= 1;
            }

            println!("Posisi saat ini: {:?}", self.position);
        }
        println!("Tujuan tercapai di {:?}", self.goal);
    }
}

fn main() {
    let mut robot = Robot::new(Point::new(0, 0), Point::new(5, 5));

    let mut events = VecDeque::new();
    events.push_back(Event::Idle);
    events.push_back(Event::ObstacleDetected(Point::new(2, 2)));
    events.push_back(Event::GoalChanged(Point::new(7, 7)));

    while let Some(event) = events.pop_front() {
        robot.handle_event(event);
    }
}
