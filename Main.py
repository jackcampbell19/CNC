from CNC import CNC
import signal
import time


def handler(s, f):
    print("Program interrupted. Cleaning up.")
    cnc.shutdown()
    exit(0)


def error(e):
    print(e)


if __name__ == "__main__":

    signal.signal(signal.SIGINT, handler)

    # Define cnc
    cnc = CNC(200, error_handler=error)

    # Input filename
    filename = 'ct/' + input('File: ')

    # Load the svg into the cnc
    # cnc.load_svg(filename)
    cnc.load_mstp(filename)

    # Draw loaded svg
    cnc.run()

    # Shutdown cnc
    cnc.shutdown()
