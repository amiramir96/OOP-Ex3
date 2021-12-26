import math
import pygame
from src.GraphAlgoInterface import GraphAlgoInterface
from graphics.Button import Button


def scale(val, new_min, new_max, prev_min, prev_max):
    """
    scale value to new boundaries
    """
    rel_pos = (val - prev_min) / (prev_max - prev_min)
    return new_min + rel_pos * (new_max - new_min)


def a_b_given_c_m(c, m):
    """
    a^2 + b^2 = c^2
    get a,b when c and his slope (m) are known
    """
    # b = m*a,   c^2 = a^2 + (m*a)^2,  a^2 = (c^2)/(1+m^2)
    a = math.sqrt((c ** 2) / (1 + m ** 2))
    b = m * a
    return a, b


def draw_arrow(screen, p1: tuple, p2: tuple, color: (int, int, int) = (0, 0, 0), radius: int = 15):
    x1, y1, x2, y2 = p1[0], p1[1], p2[0], p2[1]
    # where the triangle cuts the line
    triangle_cut_point = (x1 + 0.9 * (x2 - x1), y1 + 0.9 * (y2 - y1))
    # extreme case: slope is infinity or zero
    if x1 == x2:  # if the line is vertical, the arrow base will be horizontal
        x = radius / 2
        y = 0
    elif y1 == y2:
        x = 0
        y = radius / 2
    else:  # calculate the points of the arrow base for a base length of r
        inverse_line_slop = -1 / ((y2 - y1) / (x2 - x1))
        x, y = a_b_given_c_m(radius / 2, inverse_line_slop)
    triangle_point1 = (triangle_cut_point[0] + x, triangle_cut_point[1] + y)
    triangle_point2 = (triangle_cut_point[0] - x, triangle_cut_point[1] - y)
    # draw line
    pygame.draw.line(screen, color, (x1, y1), (x2, y2), math.ceil(radius / 10))
    pygame.draw.polygon(screen, color, [(x2, y2), triangle_point1, triangle_point2])


def plot(g: GraphAlgoInterface):
    # initialize pygame and font (singletons)
    pygame.init()
    pygame.font.init()
    # create screen
    width, height = 1080, 720
    screen = pygame.display.set_mode((width, height), depth=32, flags=pygame.constants.RESIZABLE)
    pygame.display.set_caption('Graph display')
    # set clock to control FPS
    clock = pygame.time.Clock()

    nodes = g.get_graph().get_all_v().values()
    #  find min and max for x and y values
    min_x = min(nodes, key=lambda n: n[1][0])[1][0]
    max_x = max(nodes, key=lambda n: n[1][0])[1][0]
    min_y = min(nodes, key=lambda n: n[1][1])[1][1]
    max_y = max(nodes, key=lambda n: n[1][1])[1][1]

    center_point_button = Button("CENTER POINT")
    center_point_button.set_click_listener('center_point')
    shortest_path_button = Button("SHORTEST PATH")
    shortest_path_button.set_click_listener('shortest_path')
    tsp_button = Button("TSP")
    tsp_button.set_click_listener('TSP')
    reset_button = Button("RESET")

    chosen_nodes = []
    color_nodes = []
    color_edges = []
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if center_point_button.check(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                color_nodes.append(center_point_button.action(g, center_point_button))

            if shortest_path_button.check(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if len(chosen_nodes) == 2:
                    path_nodes = shortest_path_button.action(g, shortest_path_button, chosen_nodes[0], chosen_nodes[1])
                    for i in range(len(path_nodes) - 1):
                        color_edges.append((path_nodes[i], path_nodes[i + 1]))
                else:  # reset
                    chosen_nodes = []
                    shortest_path_button.action(shortest_path_button)

            if tsp_button.check(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if len(chosen_nodes) >= 2:
                    path_nodes = tsp_button.action(g, tsp_button, chosen_nodes)
                    for i in range(len(path_nodes) - 1):
                        color_edges.append((path_nodes[i], path_nodes[i + 1]))
                else:  # reset
                    chosen_nodes = []
                    tsp_button.action(tsp_button)

            # reset
            if reset_button.check(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                chosen_nodes = []
                color_nodes = []
                color_edges = []
                center_point_button.reset()
                shortest_path_button.reset()
                tsp_button.reset()

        screen.fill(pygame.Color(239, 228, 176))
        # scale radius of nodes
        r = scale(200, 0, screen.get_width(), 0, width) / len(nodes)
        FONT = pygame.font.SysFont('Ariel', max(int(r), 10))
        margin = screen.get_width() / 20  # screen margins
        # paint nodes and edges
        for node in nodes:
            node_id = node[0]
            if node_id in color_nodes:
                color = (34, 177, 76)
            elif node_id in chosen_nodes:
                color = (163, 73, 164)
            else:
                color = (63, 72, 204)

            x, y = node[1][0], node[1][1]
            # scale position according to screen
            x = scale(x, margin, screen.get_width() - margin, min_x, max_x)
            y = scale(y, margin, screen.get_height() - 3*margin, min_y, max_y)
            node_circle = pygame.Rect((x - r, y - r), (2 * r, 2 * r))
            if node_circle.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                if node_id not in chosen_nodes:
                    chosen_nodes.append(node_id)
            pygame.draw.circle(screen, color, (x, y), r)
            # draw id
            id_srf = FONT.render(str(node_id), True, (0, 0, 0))
            id_rect = id_srf.get_rect(center=(x, y - 1.5 * r))
            screen.blit(id_srf, id_rect)

        # draw all edges
        for node in nodes:
            node_id = node[0]
            x, y = node[1][0], node[1][1]
            # scale position according to screen
            x = scale(x, margin, screen.get_width() - margin, min_x, max_x)
            y = scale(y, margin, screen.get_height() - 3*margin, min_y, max_y)
            # pygame.draw.circle(screen, pygame.Color(63, 72, 204), (x, y), r)
            # draw edges
            for edge in g.get_graph().all_out_edges_of_node(node[0]).items():
                color = (0, 0, 0)
                if (node_id, g.get_graph().get_all_v()[edge[0]][0]) in color_edges:
                    color = (0, 162, 232)
                dest_x = g.get_graph().get_all_v()[edge[0]][1][0]
                dest_y = g.get_graph().get_all_v()[edge[0]][1][1]
                dest_x = scale(dest_x, margin, screen.get_width() - margin, min_x, max_x)
                dest_y = scale(dest_y, margin, screen.get_height() - 3*margin, min_y, max_y)
                # pygame.draw.line(screen, pygame.Color(0,0,0),(x,y),(dest_x,dest_y),4)
                draw_arrow(screen, (x, y), (dest_x, dest_y), color, radius=r)

        # draw special edges
        for node in nodes:
            node_id = node[0]
            x, y = node[1][0], node[1][1]
            # scale position according to screen
            x = scale(x, margin, screen.get_width() - margin, min_x, max_x)
            y = scale(y, margin, screen.get_height() - 3*margin, min_y, max_y)
            # pygame.draw.circle(screen, pygame.Color(63, 72, 204), (x, y), r)
            # draw edges
            for edge in g.get_graph().all_out_edges_of_node(node[0]).items():
                if (node_id, g.get_graph().get_all_v()[edge[0]][0]) in color_edges:
                    color = (0, 162, 232)
                    dest_x = g.get_graph().get_all_v()[edge[0]][1][0]
                    dest_y = g.get_graph().get_all_v()[edge[0]][1][1]
                    dest_x = scale(dest_x, margin, screen.get_width() - margin, min_x, max_x)
                    dest_y = scale(dest_y, margin, screen.get_height() - 3*margin, min_y, max_y)
                    # pygame.draw.line(screen, pygame.Color(0,0,0),(x,y),(dest_x,dest_y),4)
                    draw_arrow(screen, (x, y), (dest_x, dest_y), color, radius=r)

        # draw buttons
        center_point_button.render(screen, (margin / 5, screen.get_height() - margin*1.5 - margin/5),
                                   (margin*4, margin*1.5))
        reset_button.render(screen, (screen.get_width() - margin / 5 - margin * 4,
                                     screen.get_height() - margin*1.5 - margin/5), (margin * 4, margin * 1.5))
        shortest_path_button.render(screen, (2 * (margin / 5) + margin * 4, screen.get_height() - margin*1.5 - margin/5),
                                    (margin * 4, margin * 1.5))
        tsp_button.render(screen, (3 * (margin / 5) + margin * 8, screen.get_height() - margin*1.5 - margin/5),
                          (margin * 4, margin * 1.5))

        pygame.display.update()
        clock.tick(60)
