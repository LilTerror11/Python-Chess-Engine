from classes import Board, AttributeDict, AnyMove

x = Board()

d = AttributeDict({})

p = AnyMove(0, 0, 0, 0, 0)

t = p

for i in range(10):
    t = AnyMove(0, 0, 0, 0, i, t)

print(list(t))
