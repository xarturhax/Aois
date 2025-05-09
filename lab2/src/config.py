END_INDEX = -1
INITIAL_STATE = (0, 0, 0, 0, 0, 0, 0, 0)
INCREMENT_STATE = (0, 0, 0, 0, 0, 0, 0, 1)
LOGIC_OPERATORS = {"|", "&", "!", "~", ">", "(", ")"}
PRECEDENCE = {"(": 1, "|": 2, "!": 2, "&": 3, "~": 4, ">": 5}