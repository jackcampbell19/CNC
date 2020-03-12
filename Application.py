import SVG
import tkinter as tk
from tkinter.filedialog import askopenfilename
import Commands
import socket


def load_file():
    global CURRENT_MSTP
    filename = askopenfilename()
    # file_indicator.config(text=CURRENT_MSTP.split('/')[-1] + ' loaded.', fg='green')
    CURRENT_MSTP = SVGPARSER.parse(filename)


def shutdown():
    if SKIT is not None:
        send_command(Commands.SHUTDOWN)
        SKIT.close()
    root.destroy()


def run():
    pass


def goto():
    x = int(x_input.get())
    y = int(y_input.get())
    z = int(z_input.get())
    send_command(command=Commands.SET_POSITION, data=[x, y, z])


def update_position(x, y, z):
    pass


def send_command(command, data=None):
    send_data = Commands.create_command(command, data)
    SKIT.sendall(send_data)
    data = SKIT.recv(2000000).decode('ascii')
    return data


def connect(tries=5):
    global SKIT
    if tries == 0:
        return False
    try:
        SKIT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SKIT.connect((TCP_IP, TCP_PORT))
        return True
    except ConnectionRefusedError:
        return connect(tries - 1)


SVGPARSER = SVG.SVG(200)
CURRENT_MSTP = None
WIDTH = 600
HEIGHT = 800
TCP_IP = '127.0.0.1'
TCP_PORT = 5000
SKIT = None

if __name__ == '__main__':

    # Open socket.
    connected = connect()

    # Root window.
    root = tk.Tk()
    root.geometry(str(WIDTH) + 'x' + str(HEIGHT))
    root.title("Moira CNC")

    main_font = ("Helvetica", 40)

    if connected:
        connected_indicator = tk.Label(root, text='Connected.', fg='green')
    else:
        connected_indicator = tk.Label(root, text='Not connected.', fg='red')
    connected_indicator.pack()
    connected_indicator.place(relx=0.98, rely=(0.02 * WIDTH / HEIGHT), anchor=tk.NE)

    x_label = tk.Label(root, text='X:', font=main_font)
    x_label.pack()
    x_label.place(x=10, y=10, width=40, height=50)

    x_input = tk.Entry(root)
    x_input.pack()
    x_input.delete(0, tk.END)
    x_input.insert(0, "0")
    x_input.config(font=main_font)
    x_input.place(x=10 + 40 + 5, y=10, width=120, height=50)

    y_label = tk.Label(root, text='Y: 0', font=main_font)
    y_label.pack()
    y_label.place(x=10, y=55)

    y_input = tk.Entry(root)
    y_input.pack()
    y_input.delete(0, tk.END)
    y_input.insert(0, "0")
    y_input.config(font=main_font)
    y_input.place(x=10 + 40 + 5, y=55, width=120, height=50)

    z_label = tk.Label(root, text='Z: 0', font=main_font)
    z_label.pack()
    z_label.place(x=10, y=100)

    z_input = tk.Entry(root)
    z_input.pack()
    z_input.delete(0, tk.END)
    z_input.insert(0, "0")
    z_input.config(font=main_font)
    z_input.place(x=10 + 40 + 5, y=100, width=120, height=50)

    # load_file_button = tk.Button(root, text='Load SVG', width=20, command=load_file)
    # load_file_button.pack()
    #
    # run_button = tk.Button(root, text='RUN', bg='red', width=20, command=run)
    # run_button.pack()

    go_button = tk.Button(root, text='GO', command=goto)
    go_button.pack()
    go_button.place(x=5, y=100 + 55, width=100, height=50)

    quit_button = tk.Button(root, text='SHUTDOWN', command=shutdown, highlightbackground="#b5514f", fg="white",
                            highlightthickness=60)
    quit_button.pack()
    quit_button.place(relx=0.95, rely=1 - (0.05 * WIDTH / HEIGHT), anchor=tk.SE, width=120, height=60)

    # Mainloop
    root.mainloop()