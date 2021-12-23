import pygame
from src.GraphAlgoInterface import GraphAlgoInterface
from src.GraphAlgo import GraphAlgo

# initialize pygame and font (singletons)
pygame.init()
pygame.font.init()
# set font
FONT = pygame.font.SysFont('Ariel', 15)
# create screen
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), depth=32, flags=pygame.constants.RESIZABLE)
pygame.display.set_caption('Graph display')
# set clock to control FPS
clock = pygame.time.Clock()


def scale(val, new_min, new_max, prev_min, prev_max):
    """
    scale value to new boundaries
    """
    rel_pos = (val-prev_min)/(prev_max-prev_min)
    return new_min + rel_pos*(new_max-new_min)


def plot(g: GraphAlgoInterface):
    nodes = g.get_graph().get_all_v().values()
    #  find min and max for x and y values
    for x in g.get_graph().get_all_v().values():
        print(x)
    min_x = min(nodes, key=lambda n: n[1][0])[1][0]
    max_x = max(nodes, key=lambda n: n[1][0])[1][0]
    min_y = min(nodes, key=lambda n: n[1][1])[1][1]
    max_y = max(nodes, key=lambda n: n[1][1])[1][1]

      # radius for the nodes TODO update according to node_num
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        screen.fill(pygame.Color(239, 228, 176))
        r = scale(200, 0, screen.get_width(), 0, WIDTH) / len(nodes)

        # paint nodes and edges
        for node in nodes:
            node_id = node[0]
            x, y = node[1][0], node[1][1]
            # scale position according to screen
            x = scale(x, 50, screen.get_width()-50, min_x, max_x)
            y = scale(y, 150, screen.get_height()-50, min_y, max_y)
            pygame.draw.circle(screen, pygame.Color(63, 72, 204), (x, y), r)
            # draw edges
            for edge in g.get_graph().all_out_edges_of_node(node[0]).values():
                dest_x = g.get_graph().get_all_v()[edge[0]][1][0]
                dest_y = g.get_graph().get_all_v()[edge[0]][1][1]
                dest_x = scale(dest_x, 50, screen.get_width() - 50, min_x, max_x)
                dest_y = scale(dest_y, 150, screen.get_height() - 50, min_y, max_y)
                pygame.draw.line(screen, pygame.Color(0,0,0),(x,y),(dest_x,dest_y),4)

        # drawing an arrow:
        # pygame.draw.polygon(screen, (0, 0, 0),
        #                     ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    g = GraphAlgo()
    g.load_from_json('data\\A1.json')
    print(scale(1,0,10,0,5))
    plot(g)
