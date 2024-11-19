import dudraw
from random import randint
from quads import QuadTree

# Set the simulation space dimensions
x_scale = 100
y_scale = 100

dudraw.set_x_scale(0, x_scale)
dudraw.set_y_scale(0, y_scale)


class AllBoids:
    def __init__(self, count):
        # Initialize a group of boids (birds) with random positions
        self.boids = []
        for i in range(count):
            random1 = randint(10, x_scale - 10)
            random2 = randint(10, y_scale - 10)
            self.boids.append((Boid(random1, random2, 1)))

    def draw(self):
        # Draw all the boids (birds)
        for boid in self.boids:
            boid.draw()

        # Draw the average position of all boids as a larger circle
        avg_x, avg_y = self.get_average_position()
        avg_boid = Boid(avg_x, avg_y, 2)
        avg_boid.draw()

    def get_average_position(self):
        # Calculate the average x and y position of all the boids (center of the flock)
        avg_x = 0
        avg_y = 0
        for boid in self.boids:
            avg_x += boid.x
            avg_y += boid.y
        return avg_x / len(self.boids), avg_y / len(self.boids)
    
    def get_average_position_points(self, points):
        # Calculate the average x and y position of a subset of points (local neighbors)
        avg_x = 0
        avg_y = 0
        for point in points:
            avg_x += point.x
            avg_y += point.y
        return avg_x / len(points), avg_y / len(points)
    
    def boids_approach_average(self):
        # Make each boid (bird) move slightly toward the flock's center
        avg_x, avg_y = self.get_average_position()
        for boid in self.boids:
            # Adjust velocity to reduce the distance to the center of the flock
            boid.x_velocity += (avg_x - boid.x)
            boid.y_velocity += (avg_y - boid.y)
            # Update position based on velocity
            boid.x += boid.x_velocity
            boid.y += boid.y_velocity

    def check_borders(self):
        # Prevent boids (birds) from leaving the defined area by reflecting them off the edges
        for boid in self.boids:
            if boid.x >= 100 or boid.x <= 0:
                if boid.x >= 100:
                    boid.x = 100
                else:
                    boid.x = 0
                # Reverse x velocity and reduce it to simulate a bounce
                boid.x_velocity *= -0.7
            if boid.y >= 100 or boid.y <= 0:
                if boid.y >= 100:
                    boid.y = 100
                else:
                    boid.y = 0
                # Reverse y velocity and reduce it to simulate a bounce
                boid.y_velocity *= -0.7

    def move_to_neighbors(self, neighbor_num, delay):
        # Make each boid (bird) move toward its nearby neighbors
        if delay % 1 == 0:
            # Build a quadtree to efficiently find nearby boids
            quadTree = QuadTree((x_scale / 2, y_scale / 2), x_scale, y_scale)
            for boid in self.boids:
                x = boid.x
                y = boid.y
                quadTree.insert((x, y))
            for boid in self.boids:
                # Get a list of nearby boids
                x = boid.x
                y = boid.y
                neighbors = quadTree.nearest_neighbors((x, y), neighbor_num)
                # Calculate the average position of neighbors
                avg_x, avg_y = self.get_average_position_points(neighbors)
                # Adjust velocity to move toward the average position of neighbors
                boid.x_velocity += (avg_x - boid.x) / 10000
                boid.y_velocity += (avg_y - boid.y) / 10000
                # Update position based on new velocity
                boid.x += boid.x_velocity
                boid.y += boid.y_velocity
                # Store the average position for the next update
                boid.avg_x, boid.avg_y = avg_x, avg_y
        else:
            # In subsequent frames, continue moving toward the previously calculated average position
            for boid in self.boids:
                boid.x_velocity += (boid.avg_x - boid.x) / 10000
                boid.y_velocity += (boid.avg_y - boid.y) / 10000
                boid.x += boid.x_velocity
                boid.y += boid.y_velocity


class Boid:
    def __init__(self, x, y, size):
        # Initialize a boid (bird) with position, velocity, and size
        self.x = x
        self.y = y
        self.x_velocity = 0
        self.y_velocity = 0
        self.avg_x = 0
        self.avg_y = 0
        self.size = size

    def draw(self):
        # Draw the boid as a filled circle
        dudraw.filled_circle(self.x, self.y, self.size)

    def update_velocity():
        pass

    def __str__(self):
        # String representation of a boid
        return f"Boid({self.x}, {self.y})"


# Create a group of 100 boids (birds)
b = AllBoids(100)
b.draw()

# Simulation loop
x = 0
while True:
    b.draw()  # Draw the boids
    b.move_to_neighbors(30, x)  # Make boids move toward neighbors
    b.check_borders()  # Prevent boids from leaving the area
    dudraw.show(1)  # Update the screen
    dudraw.clear()  # Clear the screen for the next frame
    x += 1  # Increment the delay
