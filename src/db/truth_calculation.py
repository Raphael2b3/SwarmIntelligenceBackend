report_damper = 5  # je höher der wert um so mehr Menschen müssen diese connection reporten damit das zugrunde


# liegende Statement einfluss verliert


def R(n):
    return 0.5 if n > 0 else 0


def truth_of_node(child_connections, node_truth_by_vote):
    r = R(len(child_connections))
    # = R*v(k) + (1-R)*summe[ i in C_k: w_c(i) * g_k(i) ]/ summe[ i in C_k, g_k(i)]

    sum_of_weights = 0
    sum_weighted_child_truth = 0

    for con in child_connections:
        sum_weighted_child_truth += con["weighted_truth"]
        sum_of_weights += con["weight"]

    out = r * node_truth_by_vote + (1 - r) * sum_weighted_child_truth / sum_of_weights
    return out
