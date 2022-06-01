import serial
import serial.tools.list_ports as list_ports
import sys
import math

numSteps = 200

#units: mm and degrees
heightChangePerRotation = 8
centerDist = 225
anglePerStep = 360 / 200
heightPerStep = heightChangePerRotation / 360 * anglePerStep

port_list = list_ports.comports()
open_details = None
for port_info in port_list:
    if "Arduino" in port_info.description:
        open_details = port_info

if open_details is None:
    print("No Arduino found!")
    sys.exit(1)

port = serial.Serial(open_details.name, 9600)

filename = input("Enter a file name: ")
input("Press enter to start scanning!")

points = []

port.write(b'\n')
l = port.readline()
code = int(l)
if code == -2:
    print("Laser initialization failed!")
    sys.exit(2)

while True:
    l = port.readline()
    code = int(l)
    if code == 20:
        point_dat = port.readline()
        point_dat = point_dat.strip()
        point_dat = point_dat.split(b' ')

        horizontal_steps = int(point_dat[0])
        measured_distance = int(point_dat[1])
        vertical_steps = int(point_dat[2])

        # determinam coordonatele cilindrice
        angle = anglePerStep * horizontal_steps
        distance_to_center = abs(measured_distance - centerDist)
        height = heightPerStep * vertical_steps

        # transformam din coordonate polare in coordonate carteziene
        x = distance_to_center * math.cos(math.radians(angle))
        y = distance_to_center * math.sin(math.radians(angle))
        z = height

        points.append((x, y, z))

        port.write(b'\n')
    
    elif code == -30:
        print("Sensor timeout bag pula")

    elif code == 10:
        break

print("Scan done! Saving...")

with open(filename, 'w') as f:
    f.write('ply\n')
    f.write('format ascii 1.0\n')
    f.write('comment Scanat de proiectul la PM\n')
    f.write(f'element vertex {len(points)}\n')
    f.write('property double x\n')
    f.write(f'property double y\n')
    f.write(f'property double z\n')
    f.write(f'end_header\n')
    for point in points:
        f.write(str(point[0]))
        f.write(' ')
        f.write(str(point[1]))
        f.write(' ')
        f.write(str(point[2]))
        f.write('\n')

print('Scan saved! Goodbye!')

