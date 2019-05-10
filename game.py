import numpy as np
import time

class Game:
    def __init__(self, vision, controller):
        self.vision = vision
        self.controller = controller
        self.state = 'not started'

    def can_see_object(self, template, threshold=0.9):
        matches = self.vision.find_template(template, threshold=threshold)
        return np.shape(matches)[1] >= 1

    def click_object(self, template, offset=(0, 0)):
        matches = self.vision.find_template(template)

        x = matches[1][0] + offset[0]
        y = matches[0][0] + offset[1]

        self.controller.move_mouse(x, y)
        self.controller.left_mouse_click()

        time.sleep(0.5)

    def round_starting(self, player):
        return self.can_see_object('%s-health-bar' % player)

    def round_finished(self):
        return self.can_see_object('tap-to-continue')

    def click_to_continue(self):
        return self.click_object('tap-to-continue', offset=(50, 30))

    def can_start_round(self):
        return self.can_see_object('next-button')

    def start_round(self):
        return self.click_object('next-button', offset=(100, 30))

    def has_full_rocket(self):
        return self.can_see_object('full-rocket')

    def use_full_rocket(self):
        return self.click_object('full-rocket')

    def found_pinata(self):
        return self.can_see_object('filled-with-goodies')

    def click_cancel(self):
        return self.click_object('cancel-button')

    def run(self):
        while True:
            self.vision.refresh_frame()
            if self.state == 'not started' and self.round_starting('bison'):
                self.log('Round needs to be started, launching bison')
                self.launch_player()
                self.state = 'started'
            if self.state == 'not started' and self.round_starting('pineapple'):
                self.log('Round needs to be started, launching pineapple')
                self.launch_player()
                self.state = 'started'
            elif self.state == 'started' and self.found_pinata():
                self.log('Found a pinata, attempting to skip')
                self.click_cancel()
            elif self.state == 'started' and self.round_finished():
                self.log('Round finished, clicking to continue')
                self.click_to_continue()
                self.state = 'mission_finished'
            elif self.state == 'started' and self.has_full_rocket():
                self.log('Round in progress, has full rocket, attempting to use it')
                self.use_full_rocket()
            elif self.state == 'mission_finished' and self.can_start_round():
                self.log('Mission finished, trying to restart round')
                self.start_round()
                self.state = 'not started'
            else:
                self.log('Not doing anything')
            time.sleep(1)

    def log(self, text):
        print('[%s] %s' % (time.strftime('%H:%M:%S'), text))