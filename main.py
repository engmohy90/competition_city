"""
main.py - read/write/ points.csv file and add city column
"""

import csv


class City(object):
    """City class .
       defining the city with a name and other prameters.
       :param name and 4 coordinates top_left(x,y) bottom_right(x,y)
       """

    def __init__(self, name, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        self.name = name
        self.top_left_x = int(top_left_x)
        self.top_left_y = int(top_left_y)
        self.bottom_right_x = int(bottom_right_x)
        self.bottom_right_y = int(bottom_right_y)

    def x_in_city(self, x, y):
        """Finding a point in the city by comparing
           the point with max and min edgs of the city.
           :param the points x and y coordinates
           :return True or False
           """
        x = int(x)
        y = int(y)
        cross_x = cross_y = 'out of conditions'
        if self.bottom_right_x > self.top_left_x:
            cross_x = (self.top_left_x <= x and x <= self.bottom_right_x)
        elif self.top_left_x > self.bottom_right_x:
            cross_x = self.bottom_right_x <= x and x <= self.top_left_x

        if self.bottom_right_y > self.top_left_y:
            cross_y = self.top_left_y <= y and y <= self.bottom_right_y
        elif self.top_left_y > self.bottom_right_y:
            cross_y = self.bottom_right_y <= y and y <= self.top_left_y
        if type(cross_x) == bool and type(cross_x) == bool:
            return cross_x and cross_y
        else:
            err = f"given ({self.name}) City cordinates are not handled please redefine cities"
            raise ValueError(err)


def read_data(cities_file='cities.csv', points_file='points.csv'):
    """Read data of a cities and  points csv files
       :param cities_file
       :param points_file
       :return order dict with new data
       """
    cities = []
    new_points = []
    # Read from csv city and make city objects
    with open(cities_file, newline='') as csv_file:
        cities_reader = csv.DictReader(csv_file)
        for row in cities_reader:
            cities.append(City(row['Name'], row['TopLeft_X'],
                               row['TopLeft_Y'], row['BottomRight_X'],
                               row['BottomRight_Y']))
    # Read from csv points
    with open(points_file, newline='') as csv_file:
        points_reader = csv.DictReader(csv_file)
        for point in points_reader:
            point['city'] = 'None'
            # Check every point with all cites assuming that the point has only one city
            for city in cities:
                if city.x_in_city(point['X'], point['Y']):
                    point['city'] = city.name
                    new_points.append(point)
                    break
    return new_points


def make_new_cvs(new_points, new_file='new_points.csv'):
    """write new file with the new points
       :param new_points  the data that will be write in
       :param new_file new file name
       """
    with open(new_file, mode='w') as csv_file:
        fieldnames = ['ID', 'X', 'Y', 'city']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_points)


def main():
    new_points = read_data()
    make_new_cvs(new_points)


if __name__ == '__main__':
    main()
