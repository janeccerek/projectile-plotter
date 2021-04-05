import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def calculate_projectile():
    dt = 0.01
    g = 9.81
    print("Podaj kolejno oddzielając przecinkiem: \n")
    m = float(input("masę ciała [kg]: "))
    h = float(input("wysokość początkową [m]: "))
    B = float(input("współczynnik oporu powietrza [kg/m]: "))
    theta = float(input("kąt pod jakim wyrzucono ciało [stopnie]: "))
    v0 = float(input("prędkość początkową [m/s]: "))
    v_x = v0 * np.cos(np.radians(theta))
    v_y = v0 * np.sin(np.radians(theta))
    pos = [[0], [h]]
    iter = 0
    x = 0
    y = h
    while y >= 0.0:
        force_x = B * v_x ** 2
        force_y = g + np.sign(v_y) * B * v_y ** 2
        x = x + v_x * dt - (force_x / (2 * m)) * dt ** 2
        y = y + v_y * dt - (force_y / (2 * m)) * dt ** 2
        v_x = v_x - (force_x / m) * dt
        v_y = v_y - (force_y / m) * dt
        pos[0].append(x)
        pos[1].append(y)
        iter += 1

    pos[0].append(x + v_x * dt - (force_x / (2 * m)) * dt ** 2)
    pos[1].append(0)
    iter += 1
    return pos, iter


pos_list, numframes = calculate_projectile()


fig = plt.subplots()
plt.xlim(0, 1.2*max(pos_list[0]))
plt.ylim(0, 1.2*max(pos_list[1]))
plt.xlabel("współrzędna x [m]")
plt.ylabel("współrzędna y [m]")
line, = plt.plot([], [], color="green")
point, = plt.plot([], [], marker = "o", color="green")
time_text  = plt.text(0.02, 0.95, '')
xdata, ydata = [], []


def init():
    line.set_data([],[])
    point.set_data([],[])
    return line,


def animate(i):
    xdata.append(pos_list[0][i])
    ydata.append(pos_list[1][i])
    line.set_data(xdata, ydata)
    point.set_data(pos_list[0][i], pos_list[1][i])
    t = 0.01 * i
    time_text.set_text("czas: {:.2f}s".format(t))
    return line, point, time_text


anim = animation.FuncAnimation(fig[0], animate, init_func=init,
							frames=numframes, interval=10, blit=True,
                            repeat=False)
plt.show()
