import pygame
import sys
import time

class RobotAnimation:
    def __init__(self, robot_setpoints):
        pygame.init()

        self.robot_setpoints = robot_setpoints
        self.num_robots = len(robot_setpoints)
        self.robots = [{"position": robot_setpoints[0][0], "index": 0, "iter": 0}, {"position": robot_setpoints[1][0], "index": 1, "iter": 0}, {"position": robot_setpoints[2][0], "index": 2, "iter": 0}, {"position": robot_setpoints[3][0], "index": 3, "iter": 0}, {"position": robot_setpoints[4][0], "index": 4, "iter": 0}, {"position": robot_setpoints[5][0], "index": 5, "iter": 0}]

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
        pygame.draw.rect(self.screen, (0, 125, 125), pygame.Rect(robot_setpoints[5][length-1][0]-20, robot_setpoints[5][length-1][1]-20, 40, 40))

        color_dict = {0: (0, 0, 255), 1: (0, 255, 0), 2: (255, 0, 0), 3: (255, 0, 255), 4: (0, 255, 255), 5: (0, 125, 125)}

        for robot in self.robots:
            pygame.draw.circle(self.screen, color_dict[robot["index"]], (int(robot["position"][0]), int(robot["position"][1])), 5)
            # pygame.draw.rect(self.screen, color_dict[robot["index"]], robot_setpoints[robot["index"]][length-1][0]-20, robot_setpoints[robot["index"]][length-1][1]-20, 40, 40)

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

robot_setpoints = {0: [[520.824868, 657.492484], [473.341912, 588.327868], [281.016184, 705.882424], [213.56614000000002, 139.285072], [244.0, 136.0]], 
                    1: [[266.252044, 686.437864], [328.229308, 703.5075879999999], [360.983092, 644.8516119999999], [549.534844, 154.147684], [556.0, 136.0]], 
                    2: [[109.89649600000001, 385.902088], [163.44175600000003, 404.479864], [169.900156, 458.437768], [678.883432, 405.815896], [700.0, 400.0]], 
                    3: [[213.56614000000002, 139.285072], [366.60676, 312.99376], [362.918596, 348.537112], [520.824868, 657.492484], [556.0, 664.0]], 
                    4: [[549.534844, 154.147684], [511.815376, 244.722436], [462.34102, 319.80466], [266.252044, 686.437864], [256.0, 664.0]], 
                    5: [[678.883432, 405.815896], [608.785732, 431.807968], [437.141716, 560.30398], [109.89649600000001, 385.902088], [100.0, 400.0]]}

robot_animation = RobotAnimation(robot_setpoints)
robot_animation.run()


