# Short program to calculate Gravitational force by newtons law (N)

def F(m1, m2, r):
    G = 6.674e-11  # gravitational constant
    return G * ((m1 * m2) / (r ** 2))


while True:
    choice = input("\nPress [C] to calculate, any other key to exit: ").lower()

    if choice != "c":  # != breaks loop if other than [c] input
        print("Shutting down")
        break

    m1 = float(input("Enter mass of body m1 (kg): "))
    m2 = float(input("Enter mass of body m2 (kg): "))
    r = float(input("Enter distance between bodies (m): "))

    force = F(m1, m2, r)
    print("Gravitational force F =", force, "N")
