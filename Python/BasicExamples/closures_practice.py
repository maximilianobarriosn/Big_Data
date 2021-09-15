def add_number(num):
    def adder(number):
        return num+number
    return adder

a_10 = add_number(10)
a_10(21)

print("a_10: %s" %a_10)
print("a_10(21): %s" %a_10(21))
