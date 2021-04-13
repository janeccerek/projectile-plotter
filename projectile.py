import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def get_data():
    # funkcja prosi użytkownika o podanie danych i potem wpisuje je do słownika
    print("Witaj w programie rysującym trajektorię ciała.\nPodaj kolejno oddzielając przecinkiem:")
    data = {}
    data.update({"mass": float(input("masę ciała [kg]: "))})
    data.update({"height": float(input("wysokość początkową [m]: "))})
    data.update({"res": float(input("współczynnik oporu powietrza [kg/m]: "))})
    data.update({"theta": float(input("kąt pod jakim wyrzucono ciało [stopnie]: "))})
    data.update({"velocity": float(input("prędkość początkową [m/s]: "))})

    return data


def calculate_projectile(data, dt):
    # funkcja wyznacza trajektorię ciała dla podanych danych
    # wczytanie stałych i wartości początkowych
    g = 9.81
    m = data["mass"]
    h = data["height"]
    B = data["res"]
    theta = data["theta"]
    v0 = data["velocity"]
    v = v0
    v_x = v0 * np.cos(np.radians(theta))
    v_y = v0 * np.sin(np.radians(theta))
    pos = [[0], [h]]
    ii = 1
    x = 0
    y = h

    # korzystam z metody Eulera do numerycznego rozwiązania równania różniczkowego
    while pos[1][ii-1] >= 0.0:
        force_x = B * v_x * v
        force_y = g + B * v_y * v
        x = x + v_x * dt
        y = y + v_y * dt
        v_x = v_x - (force_x / m) * dt
        v_y = v_y - (force_y / m) * dt
        v = np.sqrt(v_y**2 + v_x**2)
        pos[0].append(x)
        pos[1].append(y)
        ii += 1

    return pos


def optimize_interval(data):
    # Funkcja ma za zadanie zoptymalizować używane przy obliczaniu trajektorii dt tak, żeby animacja rysowała się
    # w sensownym czasie. Bez niej dla dużych wartości początkowych wykres rysuje się już niewygodnie długo.
    # Wpływa to na dokładność wyliczeń, ponieważ interwał dt zmienia się i czas spadku z tej samej wysokości dla
    # różnych wartości początkowych może się nieznacznie różnić. Co ważne, nie jest to duży rozrzut.
    dt = 0.01
    for i in range(5):
        pos = calculate_projectile(data, dt)
        if len(pos[1]) < 400:
            dt /= 2
        elif len(pos[1]) > 1000:
            dt *= 2
        else:
            return dt

    return dt


# wywołuję globalnie wartość interwału, dane i listę kolejnych współrzędnych ciała
data = get_data()
interval = optimize_interval(data)
pos_list = calculate_projectile(data, interval)

# deklaruję elementy wykresu wykorzystywane później do animacji: line jest krzywą zakreśloną przez ciało, point to
# marker punktu, w którym w danej chwili znajduje się ciało, a time_text to licznik czasu
fig = plt.subplots()
plt.xlim(1.2*min(pos_list[0]), 1.2*max(pos_list[0]))
plt.ylim(0, 1.2*max(pos_list[1]))
plt.xlabel("współrzędna x [m]")
plt.ylabel("współrzędna y [m]")
plt.title("rzut poziomy z oporem w zależności od $V^2$")
line, = plt.plot([], [], color="green")
point, = plt.plot([], [], marker="o", color="green")
time_text = plt.annotate(0, xy=(1, 1), xytext=(1, 1))
xdata, ydata = [], []


def init():
    # inicjalizuję elementy wykresu
    line.set_data([], [])
    point.set_data([], [])
    time_text.set_text("")
    return line, point, time_text


def animate(i):
    # funkcja aktualizująca wykres poprzez dodawanie kolejnych punktów oraz aktualizowanie licznika czasu
    xdata.append(pos_list[0][i])
    ydata.append(pos_list[1][i])
    line.set_data(xdata, ydata)
    point.set_data(pos_list[0][i], pos_list[1][i])
    t = interval * i
    t = round(t, 2)
    time_text.set_text("czas: " + str(t) + "s")
    return line, point, time_text


# wywołanie animacji
anim = animation.FuncAnimation(fig[0], animate, init_func=init, frames=len(pos_list[1]), interval=20/len(pos_list[1]),
                               blit=True, repeat=False)
plt.show()
