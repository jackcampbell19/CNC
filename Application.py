import SVG
import tkinter as tk
from tkinter.filedialog import askopenfilename
import Commands
import socket

import matplotlib

matplotlib.use('tkagg')

import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import (
#     FigureCanvasTkAgg, NavigationToolbar2Tk)
# from matplotlib.backend_bases import key_press_handler
# from matplotlib.figure import Figure
# import numpy as np


class Application:

    def __init__(self):
        self.svg_parser = SVG.SVG(200)
        self.current_mstp = None
        self.width = 600
        self.height = 800
        self.TCP_IP = '10.0.0.47'#'raspberrypi.local'
        self.TCP_PORT = 5000
        self.active_socket = None
        self.root = tk.Tk()
        self.x_input = tk.Entry(self.root)
        self.y_input = tk.Entry(self.root)
        self.z_input = tk.Entry(self.root)
        self.connected_indicator = tk.Label(self.root, text='Not Connected', fg='red', bg='black')
        self.gui_init()
        if self.connect():
            self.connected_indicator.config(text='Connected', fg='green')

    # Connect to the CNC.
    def connect(self, tries=5):
        if tries == 0:
            return False
        try:
            self.active_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.active_socket.connect((self.TCP_IP, self.TCP_PORT))
            return True
        except ConnectionRefusedError:
            self.active_socket = None
            return self.connect(tries - 1)

    # Sends a command to the server.
    def send_command(self, command, data=None):
        if not self.active_socket:
            return None
        send_data = Commands.create_command(command, data)
        self.active_socket.sendall(send_data)
        data = self.active_socket.recv(1048576).decode('ascii')
        return data

    def gui_init(self):
        # Root window.
        self.root.geometry(str(self.width) + 'x' + str(self.height))
        self.root.title("Moira CNC")

        main_font = ("Helvetica", 40)

        background_frame = tk.Frame(self.root, bg="black", bd=0)
        background_frame.place(x=0, y=0)
        background_canvas = tk.Canvas(background_frame, width=self.width, height=self.height, bg="black",
                           borderwidth=0, highlightthickness=0)
        background_canvas.grid()

        self.connected_indicator.pack()
        self.connected_indicator.place(relx=0.98, rely=(0.02 * self.width / self.height), anchor=tk.NE)
        self.connected_indicator.lift()



        # fig = Figure(figsize=(5, 4), dpi=100)
        # t = np.arange(0, 3, .01)
        # fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
        #
        # canvas = FigureCanvasTkAgg(fig, master=self.root)
        # canvas.draw()
        # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #
        # toolbar = NavigationToolbar2Tk(canvas, self.root)
        # toolbar.update()
        # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)



        x_label = tk.Label(self.root, text='X:', font=main_font)
        x_label.pack()
        x_label.place(x=10, y=10, width=40, height=50)

        self.x_input.pack()
        self.x_input.lift()
        self.x_input.delete(0, tk.END)
        self.x_input.insert(0, "0")
        self.x_input.config(font=main_font)
        self.x_input.place(x=10 + 40 + 5, y=10, width=120, height=50)

        y_label = tk.Label(self.root, text='Y:', font=main_font)
        y_label.pack()
        y_label.place(x=10, y=55)

        self.y_input.pack()
        self.y_input.lift()
        self.y_input.delete(0, tk.END)
        self.y_input.insert(0, "0")
        self.y_input.config(font=main_font)
        self.y_input.place(x=10 + 40 + 5, y=55, width=120, height=50)

        z_label = tk.Label(self.root, text='Z:', font=main_font)
        z_label.pack()
        z_label.place(x=10, y=100)

        self.z_input.lift()
        self.z_input.pack()
        self.z_input.delete(0, tk.END)
        self.z_input.insert(0, "0")
        self.z_input.config(font=main_font)
        self.z_input.place(x=10 + 40 + 5, y=100, width=120, height=50)

        set_position_button = tk.Button(self.root, text='SET POSITION', command=self.set_position)
        set_position_button.pack()
        set_position_button.place(x=5, y=100 + 55, width=100, height=50)

        set_origin_button = tk.Button(self.root, text='SET ORIGIN', command=self.set_origin)
        set_origin_button.pack()
        set_origin_button.place(x=5, y=100 + 55 + 55, width=100, height=50)

        load_svg_button = tk.Button(self.root, text='Load SVG', command=self.load_svg)
        load_svg_button.pack()
        load_svg_button.place(x=5, y=100 + 55 + 55 + 55, width=100, height=50)

        run_button = tk.Button(self.root, text='RUN', command=self.run)
        run_button.pack()
        run_button.place(x=5, y=100 + 55 + 55 + 55 + 55, width=100, height=50)

        quit_button = tk.Button(self.root, text='SHUTDOWN', command=self.shutdown,
                                highlightbackground="#b5514f", fg="white",
                                highlightthickness=60)
        quit_button.pack()
        quit_button.place(relx=0.95, rely=1 - (0.05 * self.width / self.height),
                          anchor=tk.SE, width=120, height=60)

    def load_svg(self):
        filename = askopenfilename()
        self.svg_parser.parse(filename)
        self.current_mstp = self.svg_parser.coordinates
        # visualize_mstp(self.current_mstp)
        self.send_command(Commands.LOAD_MSTP, self.current_mstp)

    def shutdown(self):
        if self.active_socket is not None:
            self.send_command(Commands.SHUTDOWN)
            self.active_socket.close()
        self.root.destroy()

    def set_origin(self):
        self.send_command(Commands.SET_ORIGIN)

    def set_position(self):
        x = int(self.x_input.get())
        y = int(self.y_input.get())
        z = int(self.z_input.get())
        self.send_command(command=Commands.SET_POSITION, data=[x, y, z])

    def run(self):
        self.send_command(Commands.RUN_MSTP)


# Visualizes motor instruction mstp on graph.
def visualize_mstp(mstp):
    sequences = mstp
    x = []
    y = []
    for [(x0, y0, z0), sequence] in sequences:
        cx, cy = x0, y0
        for [dx, dy, dz] in sequence:
            cx += dx
            cy += dy
            x.append(cx)
            y.append(cy)

    fig = plt.figure()
    plt.xlim(0, 5000)
    plt.ylim(5000, 0)
    graph, = plt.plot([], [], '.')

    def animate(i):
        graph.set_data(x[:i], y[:i])
        return graph

    # ani = FuncAnimation(fig, animate, frames=len(x) + 1, interval=1)
    graph.set_data(x, y)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


if __name__ == '__main__':
    app = Application()
    app.root.mainloop()
