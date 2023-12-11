import pygame
import sys
import time

class RobotAnimation:
    def __init__(self, robot_setpoints):
        pygame.init()

        self.robot_setpoints = robot_setpoints
        self.num_robots = len(robot_setpoints)
        self.robots = [{"position": [20, 480], "index": 0, "iter": 0}, {"position": [780, 480], "index": 1, "iter": 0}, {"position": [20, 120], "index": 2, "iter": 0}, {"position": [780, 120], "index": 3, "iter": 0}]

        self.screen_size = (800, 600)
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

        pygame.draw.rect(self.screen, (255, 0, 255), pygame.Rect(0, 80, 80, 80))
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(720, 80, 80, 80))
        pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(0, 440, 80, 80))
        pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(720, 440, 80, 80))

        color_dict = {0: (0, 0, 255), 1: (0, 255, 0), 2: (255, 0, 0), 3: (255, 0, 255)}

        for robot in self.robots:
            pygame.draw.circle(self.screen, color_dict[robot["index"]], (int(robot["position"][0]), int(robot["position"][1])), 30)  # Blue circle representing the robot

        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(0, 0, 800, 80))
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(0, 520, 800, 600))
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(0, 160, 360, 280))
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(440, 160, 360, 280))

        pygame.display.flip()

        if (self.counter == 0):
            # input("Hit Enter to run")
            time.sleep(2)
            self.counter = 1

    def run(self):

        while self.running:
            self.update()
            self.draw()
            self.clock.tick(30)  # Adjust the frame rate

        pygame.quit()
        sys.exit()

robot_setpoints = {0: [([30, 480]), ([400, 480]), ([30, 480]), ([30, 480]), ([770, 480]), ([770, 480]), ([770, 480]), ([770, 480])], 
1: [([770, 480]), ([770, 480]), ([770, 480]), ([400, 480]), ([400, 200]), ([400, 480]), ([30, 480]), ([30, 480])], 
2: [([30, 120]), ([30, 120]), ([400, 120]), ([770, 120]), ([400, 120]), ([770, 120]), ([770, 120]), ([770, 120])], 
3: [([770, 120]), ([400, 120]), ([400, 480]), ([400, 120]), ([30, 120]), ([30, 120]), ([30, 120]), ([30, 120])]}

robot_animation = RobotAnimation(robot_setpoints)
robot_animation.run()


# [-0.3 , -0.05] = [20, 480]
# [ 0.  , -0.05] = [400, 480]
# [ 0.3 , -0.05] = [780, 480]
# [0. , 0.2] = [400, 200]
# [-0.3 ,  0.35] = [20, 120]
# [0.  , 0.35] = [400, 120]
# [0.3 , 0.35] = [780, 120]




