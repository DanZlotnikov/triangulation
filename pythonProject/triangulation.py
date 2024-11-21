import random
import serial
import time
from calculation_tdoa_optimization import *
from utm import *
import math


class Signal:
    def __init__(self, timestamp, milliseconds):
        self.timestamp = timestamp
        self.milliseconds = milliseconds


def calculate_target_position():
    # Speed of signal propagation in air (m/s)
    velocity = 1500
    listener_location = [31.2620188513575, 34.803861311551195]
    _, _, zone_number, zone_letter = from_latlon(listener_location[0], listener_location[1])
    listener_positions = create_equilateral_triangle(31.2620188513575, 34.803861311551195, 20)
    print(listener_positions)

    # Convert Listener Positions and Add Depth (z = 0)
    listener_utm = [
        list(from_latlon(lat, lon)[:2]) + [0]  # Add z = 0
        for lat, lon in listener_positions
    ]

    # Calculate Distances and Time of Arrival (TOA)
    toa = [random.uniform(1, 1.3) for _ in range(len(listener_positions))]
    print(toa)

    # Call Steepest Descent
    rov_lst = np.array(listener_utm)  # Listeners' positions
    t_lst = np.array(toa)  # TOA values
    result, failed = tdoa_optimization(rov_lst, t_lst, velocity,  np.append(np.mean(listener_positions, axis=0), 0), is_2d=True)

    if not failed:
        # Convert Result Back to Lat/Lon
        estimated_latlon = (float(result[0][0]), float(result[0][1]))
        print("Estimated Target Position (Lat, Lon):", estimated_latlon)
    else:
        print("Steepest Descent Failed")

    return result


def listen_to_receiver(com_port, baud_rate=9600, timeout=1):
    try:
        # Open serial port
        with serial.Serial(com_port, baudrate=baud_rate, timeout=timeout) as ser:
            print(f"Listening to {com_port} at {baud_rate} baud...")

            while True:
                # Read line from the serial port
                message = ser.readline().decode('utf-8').strip()

                if message:
                    return message
                # Wait briefly to avoid overloading
                time.sleep(0.1)

    except serial.SerialException as e:
        print(f"Error accessing {com_port}: {e}")
    except KeyboardInterrupt:
        print("\nListening stopped. Exiting...")


def haversine_translation(lat, lon, distance, bearing):
    R = 6371000  # Radius of the Earth in meters

    # Convert latitude, longitude, and bearing to radians
    lat = math.radians(lat)
    lon = math.radians(lon)
    bearing = math.radians(bearing)

    # Calculate new latitude
    new_lat = math.asin(math.sin(lat) * math.cos(distance / R) +
                        math.cos(lat) * math.sin(distance / R) * math.cos(bearing))

    # Calculate new longitude
    new_lon = lon + math.atan2(math.sin(bearing) * math.sin(distance / R) * math.cos(lat),
                               math.cos(distance / R) - math.sin(lat) * math.sin(new_lat))

    # Convert back to degrees
    return math.degrees(new_lat), math.degrees(new_lon)


def create_equilateral_triangle(start_lat, start_lon, side_length):
    A = (start_lat, start_lon)
    B = haversine_translation(start_lat, start_lon, side_length, 0)
    C = haversine_translation(start_lat, start_lon, side_length, 60)

    return [A, B, C]


# Example usage
if __name__ == "__main__":
    # for vertice in triangle_vertices:
    #     #await boat.move(vertice)
    #     message = 'test,123,456'
    #     fields = message.split(',')
    #     signal = Signal(int(fields[1]), int(fields[2]))
    #     signals.append(signal)

    calculate_target_position()


