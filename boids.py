import dudraw
from random import randint
from quads import QuadTree
from quads import BoundingBox
import math


# Set the simulation space dimensions
x_scale = 100
y_scale = 100

dudraw.set_x_scale(0, x_scale)
dudraw.set_y_scale(0, y_scale)


class AllBoids:
    def __init__(self, count):
        # Initialize a group of boids (birds) with random positions
        self.boids = {}
        for i in range(count):
            random1 = randint(10, x_scale - 10)
            random2 = randint(10, y_scale - 10)
            self.boids[(random1, random2)] = Boid(random1, random2, 1)

    def draw(self):
        # Draw all the boids (birds)
        for boid in self.boids.values():
            boid.draw()

        # Draw the average position of all boids as a larger circle
        avg_x, avg_y = self.get_average_position()
        avg_boid = Boid(avg_x, avg_y, 2)
        avg_boid.draw()

    def get_average_position(self):
        # Calculate the average x and y position of all the boids (center of the flock)
        avg_x = 0
        avg_y = 0
        for boid in self.boids.values():
            avg_x += boid.x
            avg_y += boid.y
        return avg_x / len(self.boids), avg_y / len(self.boids)
    
    def get_average_position_and_velocity_points(self, points):
        # Calculate the average x and y position of a subset of points (local neighbors)
        avg_x = 0
        avg_y = 0
        avg_vel_x = 0
        avg_vel_y = 0
        for point in points:
            avg_x += point.x
            avg_y += point.y
            avg_vel_x += point.data.x_velocity
            avg_vel_y += point.data.y_velocity
        return avg_x / len(points), avg_y / len(points), avg_vel_x / len(points), avg_vel_y / len(points)
    
    def repel_collision(self, boid, collisions):
        total_x_repulsion = 0
        total_y_repulsion = 0
        strength = 50  # Constant to scale repulsion
        epsilon = 0.1  # Small value to prevent division by zero

        # Compute repulsion forces from each neighbor
        for collision in collisions:
            distance = math.sqrt((collision.x - boid.x) ** 2 + (collision.y - boid.y) ** 2)
            avoidance_factor = strength / (distance + epsilon)  # Stronger repulsion if closer
            
            # Calculate the repulsion force for this collision
            total_x_repulsion += (boid.x - collision.x) * avoidance_factor
            total_y_repulsion += (boid.y - collision.y) * avoidance_factor

        return total_x_repulsion, total_y_repulsion
    
    def boids_approach_average(self):
        # Make each boid (bird) move slightly toward the flock's center
        avg_x, avg_y = self.get_average_position()
        for boid in self.boids.values():
            # Adjust velocity to reduce the distance to the center of the flock
            boid.x_velocity += (avg_x - boid.x)/1000
            boid.y_velocity += (avg_y - boid.y)/1000
            # Update position based on velocity
            boid.x += boid.x_velocity
            boid.y += boid.y_velocity

    def check_borders(self):
        # Prevent boids (birds) from leaving the defined area by reflecting them off the edges
        for boid in self.boids.values():
            if boid.x >= 100 or boid.x <= 0:
                if boid.x >= 100:
                    boid.x = 100
                else:
                    boid.x = 0
                # Reverse x velocity and reduce it to simulate a bounce
                boid.x_velocity *= -1
            if boid.y >= 100 or boid.y <= 0:
                if boid.y >= 100:
                    boid.y = 100
                else:
                    boid.y = 0
                # Reverse y velocity and reduce it to simulate a bounce
                boid.y_velocity *= -1

    def move_to_neighbors(self, neighbor_num, delay):
        # Make each boid (bird) move toward its nearby neighbors
        if delay % 1 == 0:
            # Build a quadtree to efficiently find nearby boids
            quadTree = QuadTree((x_scale / 2, y_scale / 2), x_scale, y_scale)
            for boid in self.boids.values():
                x = boid.x
                y = boid.y
                quadTree.insert((x, y), boid)
            for boid in self.boids.values():
                # Get a list of nearby boids
                x = boid.x
                y = boid.y
                collision_bounding_radius = 2
                neighbor_bounding_radius = 15

                neighbor_bb = BoundingBox(x-neighbor_bounding_radius, y-neighbor_bounding_radius, x+neighbor_bounding_radius, y+neighbor_bounding_radius)
                collision_bb = BoundingBox(x-collision_bounding_radius, y-collision_bounding_radius, x+collision_bounding_radius, y+collision_bounding_radius)
                collisions = quadTree.within_bb(collision_bb)
                neighbors = quadTree.within_bb(neighbor_bb)
                avg_x_c, avg_y_c, avg_vel_x_c, avg_vel_y_c = self.get_average_position_and_velocity_points(collisions)


                x_repel, y_repel = self.repel_collision(boid, collisions)

                boid.x_velocity += x_repel
                boid.y_velocity += y_repel


                # coll_vel_aling_fac = 0.005  # Small factor for gradual alignment
                # boid.x_velocity -= (avg_vel_x_c - boid.x_velocity) * coll_vel_aling_fac
                # boid.y_velocity -= (avg_vel_y_c - boid.y_velocity) * coll_vel_aling_fac

                # coll_pos_aling_fac = 1
                # boid.x_velocity += (avg_x_c - boid.x) * coll_pos_aling_fac
                # boid.y_velocity += (avg_y_c - boid.y) * coll_pos_aling_fac

               




                # Calculate the average position of neighbors
                avg_x, avg_y, avg_vel_x, avg_vel_y = self.get_average_position_and_velocity_points(neighbors)




                neigh_vel_aling_fac = 1.1  # Small factor for gradual alignment
                boid.x_velocity += (avg_vel_x - boid.x_velocity) * neigh_vel_aling_fac
                boid.y_velocity += (avg_vel_y - boid.y_velocity) * neigh_vel_aling_fac


                # Adjust velocity to move toward the average position of neighbors
                neigh_pos_aling_fac = 0.001
                boid.x_velocity += (avg_x - boid.x) * neigh_pos_aling_fac
                boid.y_velocity += (avg_y - boid.y) * neigh_pos_aling_fac
                
                
                
                # Update position based on new velocity
                boid.x += boid.x_velocity
                boid.y += boid.y_velocity
                # Store the average position for the next update
                boid.avg_x, boid.avg_y = avg_x, avg_y

        else:
            # In subsequent frames, continue moving toward the previously calculated average position
            for boid in self.boids.values():
                boid.x_velocity += (boid.avg_x - boid.x) * alignment_factor
                boid.y_velocity += (boid.avg_y - boid.y) * alignment_factor
                boid.x += boid.x_velocity
                boid.y += boid.y_velocity


    def accomadate_direction(self, boid, neighbors):
        pass


    def get_average_velocity_points(self, points):
        # Calculate the average x and y position of a subset of points (local neighbors)
        for point in points:
            boid = self.boids[(round(point.x), round(point.y))]
            print(boid)
        # return avg_x / len(points), avg_y / len(points)

class Boid:
    def __init__(self, x, y, size):
        # Initialize a boid (bird) with position, velocity, and size
        self.x = x
        self.y = y
        self.x_velocity = randint(-10,10)/100
        self.y_velocity = randint(-10,10)/100
        self.avg_x = 0
        self.avg_y = 0
        self.size = size
        self.smile = ":)"

    def draw(self):
        # Draw the boid as a filled circle
        dudraw.filled_circle(self.x, self.y, self.size)

    def update_velocity():
        pass

    def __str__(self):
        # String representation of a boid
        return f"Boid({self.x}, {self.y})"


# Create a group of 100 boids (birds)
b = AllBoids(200)
b.draw()

# Simulation loop
x = 0
while True:
    b.draw()  # Draw the boids
    b.move_to_neighbors(20, x)  # Make boids move toward neighbors
    b.check_borders()  # Prevent boids from leaving the area
    dudraw.show(1)  # Update the screen
    dudraw.clear()  # Clear the screen for the next frame
    x += 1  # Increment the delay
