class Counter(object):
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def __iter__(self):
        counter = self.low
        while self.high >= counter:
            yield counter
            counter += 1

genobj = Counter(5,10)
for num in genobj:
    print(num, end=' ')

for num in genobj:
    print(num, end=' ')
