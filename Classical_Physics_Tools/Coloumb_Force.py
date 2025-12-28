def F(q1, q2, r):  # defined variables by user

    ke = 8.9875517873681764e9  # Ke electrostatic constant in Coloumbs Law
    return ke * ((q1 * q2) / (r ** 2))


while True:
    choice = input(
        "\nPress [C] to calculate Coloumb Force between two charges, any other key to exit: ").lower()

    if choice != "c":
        print("Shutting down")
        break

    q1 = float(
        input("Enter charge of body q1 (C) (e.g. 1e-6 for microcoulombs): "))
    q2 = float(
        input("Enter charge of body q2 (C) (e.g. 1e-6 for microcoulombs): "))
    r = float(input("Enter distance between charges (m): "))
# be careful of distances, as these get small and can ipact results greatly resulting in very high (N) Coloumb forces

    force = F(q1, q2, r)
    print("Coloumb Force F =", force, "N")
