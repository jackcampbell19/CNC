from CNC import CNC


if __name__ == "__main__":

    # Define cnc
    cnc = CNC(200)

    # Input filename
    filename = 'test-files/' + input('SVG: ')
    if filename[len(filename) - 4:] != '.svg':
        print('File must be in .svg format.')
        exit(0)

    # Load the svg into the cnc
    cnc.load_svg(filename)

    # Visualize the processed svg
    cnc.visualize_sequences()