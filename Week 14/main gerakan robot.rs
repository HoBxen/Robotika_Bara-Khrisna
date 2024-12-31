use std::io;

#[derive(Debug)]
struct Robot {
    x: i32,
    y: i32,
}

impl Robot {
    fn new() -> Self {
        Robot { x: 0, y: 0 }
    }

    fn move_robot(&mut self, direction: &str) {
        match direction {
            "up" => self.y += 1,
            "down" => self.y -= 1,
            "left" => self.x -= 1,
            "right" => self.x += 1,
            _ => println!("Perintah tidak dikenal. Gunakan 'up', 'down', 'left', atau 'right'."),
        }
    }

    fn get_position(&self) -> (i32, i32) {
        (self.x, self.y)
    }
}

fn main() {
    let mut robot = Robot::new();
    let mut input = String::new();

    println!("Posisi awal robot: {:?}", robot.get_position());

    loop {
        println!("Masukkan perintah gerakan (up, down, left, right) atau 'exit' untuk keluar:");
        input.clear();
        io::stdin().read_line(&mut input).expect("Gagal membaca input");
        let command = input.trim();

        if command == "exit" {
            println!("Keluar dari program. Posisi akhir robot: {:?}", robot.get_position());
            break;
        }

        robot.move_robot(command);
        println!("Posisi robot saat ini: {:?}", robot.get_position());
    }
}
