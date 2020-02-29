from CNC import CNC
import signal


def handler(s, f):
    print("Program interrupted. Cleaning up.")
    cnc.shutdown()
    exit(0)


signal.signal(signal.SIGINT, handler)


if __name__ == "__main__":

    # Define cnc
    cnc = CNC(200)

    # Input filename
    filename = 'mstp/' + input('File: ')

    # Load the svg into the cnc
    # cnc.load_svg(filename)
    cnc.load_mstp(filename)

    # Draw loaded svg
    cnc.run()

    # Shutdown cnc
    cnc.shutdown()
