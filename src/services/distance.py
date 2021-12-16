import math


def octile_distance(node_a, node_b):
    """Calculate the octile distance between node A and node B, using the
    positional field 'pos' of the nodes.

    Args:
        node_a (Node): Node A
        node_b (Node): Node B

    Returns:
        float: The octile distance between the nodes.
    """
    x_delta = abs(node_a.pos[0] - node_b.pos[0])
    y_delta = abs(node_a.pos[1] - node_b.pos[1])
    if x_delta > y_delta:
        return x_delta - y_delta + math.sqrt(2) * y_delta
    return y_delta - x_delta + math.sqrt(2) * x_delta
