
report_damper = 5  # je höher der wert um so mehr Menschen müssen diese connection reporten damit das zugrunde

# liegende Statement einfluss verliert


def R(n):
    return 0.5 if n > 0 else 0

def truth_of_node(child_truths, child_weights, node_truth_by_vote):
    r = R(len(child_weights))
    # = R*v(k) + (1-R)*summe[ i in C_k: w_c(i) * g_k(i) ]/ summe[ i in C_k, g_k(i)]

    sum_of_weights = 0
    sum_weighted_child_truth = 0
    i = 0
    for weight in child_weights:
        sum_weighted_child_truth += weight * child_truths[i]
        sum_of_weights += weight
        i += 1

    out = r * node_truth_by_vote + (1 - r) * sum_weighted_child_truth / sum_of_weights
    return out

def truth_of_node_by_votes(votes):
    return sum([v for v in votes]) / len(votes)

def weight_of_connection(votes):
    """
    Wenn eine connection nicht mehr durch durschnitte gewichtet wird sondern durch eine komplexe funktion
    :param votes:
    :return:
    """
    return sum([v for v in votes]) / len(votes)
    # return math.e ** (-n_reports / self.report_damper).
