class TruthCalculator:
    report_damper = 5  # je höher der wert um so mehr Menschen müssen diese connection reporten damit das zugrunde

    # liegende Statement einfluss verliert

    truth_cache = {}  # id:Wahrheitswert paare

    def R(self, n):
        return 0.5 if n > 0 else 0

    def truth_of_node(self, child_truths, child_weights, node_truth_by_vote):
        R = self.R(len(child_weights))
        ' = R*v(k) + (1-R)*summe[ i in C_k: w_c(i) * g_k(i) ]/ summe[ i in C_k, g_k(i)]'
        sum_of_weights = 0
        sum_weighted_child_truth = 0
        i = 0
        for t in child_truths:
            sum_weighted_child_truth += child_weights[i] * t
            sum_of_weights += child_weights[i]
            i += 1
        out = R * node_truth_by_vote + (1 - R) * sum_weighted_child_truth / sum_of_weights
        return out

    def truth_of_node_by_votes(self, votes):
        return sum([v for v in votes]) / len(votes)

    def weight_of_connection(self, votes):
        return sum([v for v in votes]) / len(votes)
        # return math.e ** (-n_reports / self.report_damper).
