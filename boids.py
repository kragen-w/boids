import dudraw
from random import randint
from quads import QuadTree

x_scale = 100
y_scale = 100

dudraw.set_x_scale(0,x_scale)
dudraw.set_y_scale(0,y_scale)


class AllBoids:
    def __init__(self, count):
        self.boids = []
        for i in range(count):
            random1 = randint(10, x_scale - 10)
            random2 = randint(10, y_scale - 10)
            self.boids.append((Boid(random1, random2, 1)))

    def draw(self):
        for boid in self.boids:
            boid.draw()

        avg_x, avg_y = self.get_average_position()
        avg_boid = Boid(avg_x, avg_y, 2)
        avg_boid.draw()

    def get_average_position(self):
        avg_x = 0
        avg_y = 0
        for boid in self.boids:
            avg_x += boid.x
            avg_y += boid.y
        return avg_x / len(self.boids), avg_y / len(self.boids)
    
    def get_average_position_points(self, points):
        avg_x = 0
        avg_y = 0
        for point in points:
            avg_x += point.x
            avg_y += point.y
        return avg_x / len(points), avg_y / len(points)
    
    def boids_approach_average(self):
        avg_x, avg_y = self.get_average_position()
        # avg_x, avg_y = 50, 50
        for boid in self.boids:
            boid.x_velocity += (avg_x - boid.x)
            boid.y_velocity += (avg_y - boid.y)
            boid.x += boid.x_velocity
            boid.y += boid.y_velocity





            # boid.x += (avg_x - boid.x)/1000
            # boid.y += (avg_y - boid.y)/1000


            # boid.x -= (boid.x - avg_x)/1000
            # boid.y -= (boid.y + avg_y)/1000

    def check_borders(self):
        for boid in self.boids:
            if boid.x >= 100 or boid.x <= 0:
                if boid.x >= 100:
                    boid.x = 100
                else:
                    boid.x = 0
                boid.x_velocity *= -0.7
            if boid.y >= 100 or boid.y <= 0:
                if boid.y >= 100:
                    boid.y = 100
                else:
                    boid.y = 0
                boid.y_velocity *= -0.7

    def move_to_neighbors(self, neightbor_num, delay):
        if delay % 1 == 0:
            quadTree = QuadTree((x_scale/2,y_scale/2), x_scale, y_scale)
            for boid in self.boids:
                x = boid.x
                y = boid.y
                quadTree.insert((x,y))
            for boid in self.boids:
                x = boid.x
                y = boid.y
                neighbors = quadTree.nearest_neighbors((x, y), neightbor_num)
                avg_x, avg_y = self.get_average_position_points(neighbors)
                boid.x_velocity += (avg_x - boid.x)/10000
                boid.y_velocity += (avg_y - boid.y)/10000
                boid.x += boid.x_velocity
                boid.y += boid.y_velocity
                boid.avg_x, boid.avg_y = avg_x, avg_y
        else:
            for boid in self.boids:
                boid.x_velocity += (boid.avg_x - boid.x)/10000
                boid.y_velocity += (boid.avg_y - boid.y)/10000
                boid.x += boid.x_velocity
                boid.y += boid.y_velocity

            

class Boid:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        # self.x_velocity = 1/randint(100,300)
        # self.y_velocity = 1/randint(100,300)
        self.x_velocity = 0
        self.y_velocity = 0
        self.avg_x = 0
        self.avg_y = 0
        self.size = size

    def draw(self):
        dudraw.filled_circle(self.x, self.y, self.size)

    def update_velocity():
        pass
    def __str__(self):
        return f"Boid({self.x}, {self.y})"

    

b = AllBoids(100)
b.draw()

x = 0
while True:
    b.draw()
    b.move_to_neighbors(30, x)
    b.check_borders()
    dudraw.show(1)
    dudraw.clear()
    x += 1



