from game import max_assoc


def test_max_assoc():
    data = [(["a"], 0), (["b"], -1), (["c"], 30), (["d", 20])]
    print(max_assoc(iter(data)))
