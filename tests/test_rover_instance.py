from nose.tools import with_setup

from unittest import TestCase
from rover import Rover

compass_headings = ['N', 'E', 'S', 'W']

class TestRover(TestCase):

    def setUp(self):
        self.rover = Rover()

    def test_rover_compass(self):
        assert self.rover.compass == compass_headings

    def test_rover_position(self):
        assert self.rover.position == (self.rover.x, self.rover.y, self.rover.direction)

    def test_rover_set_position(self):
        self.rover.set_position(4, 9, 'W')
        assert self.rover.position == (4, 9, 'W')

    def test_rover_compass_index(self):
        for i in range(0, len(compass_headings)):
            self.rover.direction = compass_headings[i]
            assert self.rover.compass_index == i

    def test_rover_axis(self):
        for i in range(0, len(compass_headings)):
            self.rover.direction = compass_headings[i]
            if self.rover.direction in ['E', 'W']:
                assert self.rover.axis == 0
            else:
                assert self.rover.axis == 1

    def test_rover_multiplier(self):
        for i in range(0, len(compass_headings)):
            self.rover.direction = compass_headings[i]
            if self.rover.direction in ['N', 'E']:
                assert self.rover.multiplier == 1
            else:
                assert self.rover.multiplier == -1



def move_and_check_position(initial_coordinates, initial_direction, command, offset):
    rover = Rover(*initial_coordinates, direction=initial_direction)

    rover.move(command)
    assert rover.position == (initial_coordinates[0] + offset[0],  # x
                              initial_coordinates[1] + offset[1],  # y
                              initial_direction)                   # direction


def rotate_and_check_position(initial_coordinates, initial_direction, command, new_direction):
    rover = Rover(*initial_coordinates, direction=initial_direction)

    rover.move(command)
    assert rover.position == (initial_coordinates[0],   # x
                              initial_coordinates[1],   # y
                              new_direction)            # direction


def test_forwards_movement():
    coordinate_list = [
        (0, 0),
        (0, 0),
        (0, 1),
        (1, 0)
    ]
    offset_list = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
    ]
    for i in range(0, len(compass_headings)):
        initial_coordinates = coordinate_list[i]
        initial_direction = compass_headings[i]
        offset = offset_list[i]
        yield move_and_check_position, initial_coordinates, initial_direction, 'F', offset


def test_backwards_movement():
    coordinate_list = [
        (0, 1),
        (1, 0),
        (0, 0),
        (0, 0)
    ]
    offset_list = [
        (0, -1),
        (-1, 0),
        (0, 1),
        (1, 0)
    ]
    for i in range(0, len(compass_headings)):
        initial_coordinates = coordinate_list[i]
        initial_direction = compass_headings[i]
        offset = offset_list[i]
        yield move_and_check_position, initial_coordinates, initial_direction, 'B', offset


def test_clockwise_rotation():
    rotations = [
        ('N', 'E'),
        ('E', 'S'),
        ('S', 'W'),
        ('W', 'N')
    ]
    for rotation in rotations:
        yield rotate_and_check_position, (0, 0), rotation[0], 'R', rotation[1]

def test_anticlockwise_rotation():
    rotations = [
        ('N', 'W'),
        ('W', 'S'),
        ('S', 'E'),
        ('E', 'N')
    ]
    for rotation in rotations:
        yield rotate_and_check_position, (0, 0), rotation[0], 'L', rotation[1]
