import math


def octile_distance_pos(pos_a, pos_b):
    """Calculate the octile distance between position a and b.

    Args:
        pos_a (tuple): The (x,y) coordinates of position A.
        pos_b (tuple): The (x,y) coordinates of position B.
    """
    x_delta = abs(pos_a[0] - pos_b[0])
    y_delta = abs(pos_a[1] - pos_b[1])
    if x_delta > y_delta:
        return x_delta - y_delta + math.sqrt(2) * y_delta
    return y_delta - x_delta + math.sqrt(2) * x_delta


def octile_distance(node_a, node_b):
    """Calculate the octile distance between node A and node B, using the
    positional field 'pos' of the nodes.

    Args:
        node_a (Node): Node A
        node_b (Node): Node B

    Returns:
        float: The octile distance between the nodes.
    """
    return octile_distance_pos(node_a.pos, node_b.pos)


def calculate_path_cost(path):
    """Calculate the cost of movement of moving from the first position on the list
    to the last.

    Args:
        path (list): A list of (x,y) positions of the path. The path is assumed to
        be in traversal order (p_0 -> p_i -> ... -> p_n), where p_(i-1) is the neighbor
        of p_i for all 0 < i <= n.
    """
    cost = 0

    if len(path) < 2:
        return cost

    pos = path[0]
    for next_pos in path[1:]:
        cost += math.sqrt((pos[0]-next_pos[0])**2 +
                          (pos[1]-next_pos[1])**2)
        pos = next_pos

    return cost
