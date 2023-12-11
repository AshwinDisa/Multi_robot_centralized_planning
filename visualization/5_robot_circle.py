import pygame
import sys
import time

class RobotAnimation:
    def __init__(self, robot_setpoints):
        pygame.init()

        self.robot_setpoints = robot_setpoints
        self.num_robots = len(robot_setpoints)
        self.robots = [{"position": robot_setpoints[0][0], "index": 0, "iter": 0}, {"position": robot_setpoints[1][0], "index": 1, "iter": 0}, {"position": robot_setpoints[2][0], "index": 2, "iter": 0}, {"position": robot_setpoints[3][0], "index": 3, "iter": 0}, {"position": robot_setpoints[4][0], "index": 4, "iter": 0}]

        self.screen_size = (800, 800)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption('Robot Movement Visualization')

        self.clock = pygame.time.Clock()
        self.running = True
        self.iter = 0
        self.list = []
        self.counter = 0

    def update(self):
        for robot in self.robots:

            target_position = self.robot_setpoints[robot["index"]][self.iter]# [robot["iter"]]
            dx = target_position[0] - robot["position"][0]
            dy = target_position[1] - robot["position"][1]

            distance = 5  # Adjust the speed of the robot
            magnitude = (dx**2 + dy**2)**0.5
            if magnitude > distance:
                ratio = distance / magnitude
                dx *= ratio
                dy *= ratio

            robot["position"][0] += dx
            robot["position"][1] += dy

            if (robot["position"][0] == target_position[0] and robot["position"][1] == target_position[1] and self.iter < len(self.robot_setpoints[0]) - 1):
                
                self.list.append(robot["index"])

                if len(list(set(self.list))) == 4:
                    self.iter += 1
                    self.list = []
                

    def draw(self):
        self.screen.fill((255, 255, 255))  # White background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        length = len(robot_setpoints[0])
        pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(robot_setpoints[0][length-1][0]-20, robot_setpoints[0][length-1][1]-20, 40, 40))
        pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(robot_setpoints[1][length-1][0]-20, robot_setpoints[1][length-1][1]-20, 40, 40))
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(robot_setpoints[2][length-1][0]-20, robot_setpoints[2][length-1][1]-20, 40, 40))
        pygame.draw.rect(self.screen, (255, 0, 255), pygame.Rect(robot_setpoints[3][length-1][0]-20, robot_setpoints[3][length-1][1]-20, 40, 40))
        pygame.draw.rect(self.screen, (0, 255, 255), pygame.Rect(robot_setpoints[4][length-1][0]-20, robot_setpoints[4][length-1][1]-20, 40, 40))

        color_dict = {0: (0, 0, 255), 1: (0, 255, 0), 2: (255, 0, 0), 3: (255, 0, 255), 4: (0, 255, 255)}

        for robot in self.robots:
            pygame.draw.circle(self.screen, color_dict[robot["index"]], (int(robot["position"][0]), int(robot["position"][1])), 30)  # Blue circle representing the robot

        pygame.display.flip()

        if (self.counter == 0):
            time.sleep(2)
            self.counter = 1

    def run(self):

        while self.running:
            self.update()
            self.draw()
            self.clock.tick(30)  

        pygame.quit()
        sys.exit()

robot_setpoints = {0: [[731.099248, 385.827424], [605.87248, 604.31398], [405.59494, 521.505124], [281.016184, 705.882424], [87.114892, 752.566528], [55.9015, 489.255952], [42.91293999999999, 421.907368], [42.91293999999999, 421.907368], [42.91293999999999, 421.907368], [40.0, 400.0]], 
1: [[485.92233999999996, 720.6342159999999], [422.406556, 682.3812760000001], [367.753948, 639.160888], [422.406556, 682.3812760000001], [485.92233999999996, 720.6342159999999], [422.406556, 682.3812760000001], [367.753948, 639.160888], [363.083572, 585.479104], [292.886608, 58.024924000000055], [292.0, 63.99999999999994]], 
2: [[120.25698399999999, 597.213124], [131.33278, 549.643], [179.57825200000002, 549.12544], [132.32049999999998, 541.7518239999999], [437.141716, 560.30398], [608.785732, 431.807968], [741.257128, 186.620404], [688.977688, 163.76062000000002], [688.977688, 163.76062000000002], [688.0, 195.99999999999997]], 
3: [[93.68254000000002, 206.15445999999997], [79.57093600000002, 277.48787200000004], [213.48747999999998, 230.509456], [55.9015, 489.255952], [199.38052000000002, 166.813888], [262.78973199999996, 206.74526799999998], [331.054264, 214.76757999999998], [374.819632, 286.23766], [695.007712, 593.5846], [688.0, 604.0]], 
4: [[514.910248, 75.73461999999995], [509.66022399999997, 134.004592], [473.6704, 142.04508399999997], [374.819632, 286.23766], [362.918596, 348.537112], [462.34102, 319.80466], [362.918596, 348.537112], [230.13601599999998, 405.676924], [281.016184, 705.882424], [292.0, 736.0]]}

robot_animation = RobotAnimation(robot_setpoints)
robot_animation.run()


