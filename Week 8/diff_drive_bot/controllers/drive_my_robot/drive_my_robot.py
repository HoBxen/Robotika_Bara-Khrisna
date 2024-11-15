from controller import Robot

if __name__== "__main__":

    robot = Robot()
    
    timestep = 64
    max_speed = 6.28
    
    left_motor = robot.getDevice('motor1')
    right_motor = robot.getDevice('motor2')
    
    left_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    
    right_motor.setPosition(float('inf'))
    right_motor.setVelocity(0.0)
    
    while robot.step(timestep) !=-1:
    
        left_speed = -0.5 * max_speed
        right_speed = -0.25 * max_speed
        
        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)