'''Information Retrieval (IR) metrics definition'''

def precision(results, relevants):
    retrieved = len(results) # it cannot be 0, it is equal to the config.query.n
    retrieved_relevant = sum([1 if patent in relevants else 0 for patent in results])
    return retrieved_relevant/retrieved

def recall(results, relevants):
    relevant = len(relevants)
    if relevant == 0:
        return 0  # Return 0 recall if there are no relevant documents
    retrieved_relevant = sum([1 if patent in relevants else 0 for patent in results])
    return retrieved_relevant/relevant

def f1_score(results, relevants):
    P = precision(results, relevants)
    R = recall(results, relevants)
    if (R + P) == 0:
        return 0  # Return 0 F1 score if both precision and recall are 0
    return 2 * R * P / (R + P)

def precision_at_k(results, relevants, k):
    return precision(results[:k], relevants)

def recall_at_k(results, relevants, k):
    return recall(results[:k], relevants)

def f1_score_at_k(results, relevants, k):
    return f1_score(results[:k], relevants)