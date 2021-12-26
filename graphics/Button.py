import pygame
from src.GraphAlgoInterface import GraphAlgoInterface
pygame.init()
pygame.font.init()


class Button:
    def __init__(self, title):
        self.original_title = title
        self.title = title
        self.rect = pygame.Rect((0, 0), (0, 0))
        self.color = (255, 255, 255)
        self.font = None
        self.action = None
        self.activated = False

    def set_click_listener(self, func_name):
        if func_name == 'center_point':
            self.action = center_point_action
        if func_name == 'shortest_path':
            self.action = shortest_path_action
        if func_name == 'TSP':
            self.action = tsp_action

    def render(self, surface: pygame.surface,  pos: (int, int), size: (int, int)):
        self.rect.topleft = pos
        self.rect.size = size
        self.font = pygame.font.SysFont('Ariel', int(min(size[0]*0.1,size[1]*0.5)))

        title_srf = self.font.render(self.title, True, (0, 0, 0))
        title_rect = title_srf.get_rect(center=self.rect.center)
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(title_srf, title_rect)

    def check(self, pos: (int, int)):
        if not self.activated:  # we have an action to perform
            if self.rect.collidepoint(pos):
                self.color = (195, 195, 195)
                return True
            else:
                self.color = (255, 255, 255)
                return False

    def reset(self):
        self.title = self.original_title
        self.activated = False
        self.color = (255, 255, 255)


def center_point_action(g: GraphAlgoInterface, b: Button):
    b.title = "Loading..."
    results = g.centerPoint()
    b.activated = True
    b.title = "Max Min Distance: "+str(results[1])[:5]
    b.color = (200, 200, 30)
    return results[0]


def shortest_path_action(*args):
    if len(args) == 1:
        b = args[0]
        b.title = "Choose 2 Nodes First"
        b.color = (185, 122, 87)
        b.activated = True

    else:
        g, b, n1, n2 = args
        b.title = "Loading..."
        path = g.shortest_path(n1, n2)
        b.activated = True
        b.title = "Distance: " + "{:.3f}".format(path[0])
        b.color = (200, 200, 30)
        return path[1]


def tsp_action(*args):
    if len(args) == 1:
        b = args[0]
        b.title = "Choose 2+ Nodes First"
        b.color = (185, 122, 87)
        b.activated = True

    else:
        g, b, nodes = args
        b.title = "Loading..."
        path = g.TSP(nodes)
        b.activated = True
        b.title = "Distance: " + "{:.3f}".format(path[1])
        b.color = (200, 200, 30)
        return path[0]
