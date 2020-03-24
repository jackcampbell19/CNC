from SVG import SVG
from Raster import Rasterizer
from CoordinateTrace import CoordinateTrace
from MotorStep import MotorStep

if __name__ == "__main__":

    svg = SVG(200, 30)
    rasterizer = Rasterizer()

    while True:

        file = input('Input file: ')
        input_type = file.split('.')[1]

        if input_type not in ['svg', 'jpg', 'ct']:
            print('Error: Invalid input type.')
            continue

        output = input('Export as (.ct/.mstp): ')
        output_name = output.split('.')[0]
        output_type = output.split('.')[1]

        if output_type not in ['ct', 'mstp']:
            print('Error: Invalid output type.')
            continue

        if '/' in output_name:
            print('Error: Name cannot contain paths.')
            continue

        path = input('Export to: ')

        if input_type == 'svg':
            svg.load(file)
            if output_type == 'ct':
                svg.export_ct(output_name, path)
            elif output_type == 'mstp':
                svg.export_mstp(output_name, path)

        if input_type == 'jpg':
            rasterizer.load(file)
            if output_type == 'ct':
                rasterizer.export_ct(output_name, path)
            elif output_type == 'mstp':
                rasterizer.export_mstp(output_name, path)

        if input_type == 'ct':
            ct = CoordinateTrace.load(file)
            mstp = MotorStep(ct=ct)
            mstp.export(path)

        print('Completed.\n')
