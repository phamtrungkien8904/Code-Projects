v = [0.67,0.67,0.63,0.68,0.70]
def mittelwert(v):
    summe = 0
    for i in v:
        summe += i
    return summe / len(v)

def sigma(v):
    m = mittelwert(v)
    summe = 0
    for i in v:
        summe += (i - m) ** 2
    return (summe / (len(v) - 1)) ** 0.5

def unsicherheit(v):
    return sigma(v) / (len(v) ** 0.5)

print("Mittelwert:", mittelwert(v))
print("Standardabweichung:", sigma(v))
print("Unsicherheit:", unsicherheit(v))
