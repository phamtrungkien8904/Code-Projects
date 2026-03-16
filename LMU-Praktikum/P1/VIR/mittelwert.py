v = [4.24,4.50,4.45,4.38,4.39]
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

eta = (9.81*(15.8e-3)**2)/(18*mittelwert(v))*(2663-916)*10

print("Mittelwert:", mittelwert(v))
print("Standardabweichung:", sigma(v))
print("Unsicherheit:", unsicherheit(v))
print("Eta:", eta)