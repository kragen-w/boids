import dudraw
from random import randint
from quads import QuadTree
from quads import BoundingBox
import math


"""
todo:

understand all of the vector math
put things in terms of delta x and delta y instead of speed and shit
implement quad tree by yourself
add better collision detection and wall detection
"""

x_scale = 600
y_scale = 600
dudraw.set_canvas_size(800,800)

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
        # avg_boid.draw()

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
    



    def turn_toward(self, boid_x, boid_y, boid_vx, boid_vy, target_x, target_y, turn_angle, speed):
        """
        Turn the boid slightly toward the target point.

        Parameters:
        - boid_x, boid_y: Current position of the boid.
        - boid_vx, boid_vy: Current velocity of the boid.
        - target_x, target_y: Coordinates of the target point.
        - turn_angle: Maximum angle (in radians) the boid can turn.

        Returns:
        - (new_vx, new_vy): Updated velocity vector.
        """
        # Compute direction to the target
        dir_x = target_x - boid_x
        dir_y = target_y - boid_y
        distance = math.sqrt(dir_x**2 + dir_y**2)
        if distance == 0:
            return boid_vx, boid_vy  # No change if the boid is already at the target
        dir_x /= distance
        dir_y /= distance

        # Normalize boid's current velocity
        velocity_magnitude = math.sqrt(boid_vx**2 + boid_vy**2)
        if velocity_magnitude == 0:
            boid_vx, boid_vy = dir_x, dir_y  # If stationary, point directly at the target
            velocity_magnitude = 1

        boid_vx /= velocity_magnitude
        boid_vy /= velocity_magnitude

        # Compute the angle between the boid's velocity and the direction to the target
        dot_product = boid_vx * dir_x + boid_vy * dir_y
        angle_to_target = math.acos(max(-1, min(1, dot_product)))

        # Determine the rotation direction (clockwise or counterclockwise)
        cross_product = boid_vx * dir_y - boid_vy * dir_x
        rotation_direction = 1 if cross_product > 0 else -1

        # If the angle to the target is smaller than turn_angle, align directly
        if abs(angle_to_target) < turn_angle:
            return dir_x * speed, dir_y * speed

        # Rotate the velocity vector by turn_angle in the proper direction
        angle_to_rotate = turn_angle * rotation_direction
        cos_theta = math.cos(angle_to_rotate)
        sin_theta = math.sin(angle_to_rotate)

        new_vx = boid_vx * cos_theta - boid_vy * sin_theta
        new_vy = boid_vx * sin_theta + boid_vy * cos_theta

        # Scale the new velocity to match the desired speed
        return new_vx * speed, new_vy * speed

    

    def align_vector(self, current_vx, current_vy, target_vx, target_vy, alpha, reverse):
        # Normalize current vector
        current_magnitude = math.sqrt(current_vx**2 + current_vy**2)
        if current_magnitude != 0:
            current_vx /= current_magnitude
            current_vy /= current_magnitude

        # Normalize target vector
        target_magnitude = math.sqrt(target_vx**2 + target_vy**2)
        if target_magnitude != 0:
            target_vx /= target_magnitude
            target_vy /= target_magnitude

        if reverse:
            target_vx *= -1
            target_vy *= -1

        # Interpolate between the two vectors
        blended_vx = (1 - alpha) * current_vx + alpha * target_vx
        blended_vy = (1 - alpha) * current_vy + alpha * target_vy

        # Re-normalize to maintain the original magnitude of the current vector
        result_magnitude = current_magnitude
        final_magnitude = math.sqrt(blended_vx**2 + blended_vy**2)
        if final_magnitude != 0:
            blended_vx = blended_vx / final_magnitude * result_magnitude
            blended_vy = blended_vy / final_magnitude * result_magnitude

        return blended_vx, blended_vy

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

    def boids_approach_average(self, collision_radius, neighbor_radius, turn_speed, align_rate, away_rate):


        # Build a quadtree to efficiently find nearby boids
        quadTree = QuadTree((x_scale / 2, y_scale / 2), x_scale, y_scale)
        for boid in self.boids:
            x = boid.x
            y = boid.y
            quadTree.insert((x, y), boid)
        for boid in self.boids:
            # Get a list of nearby boids
            x = boid.x
            y = boid.y
            collision_bounding_radius = collision_radius
            neighbor_bounding_radius = neighbor_radius

            neighbor_bb = BoundingBox(x-neighbor_bounding_radius, y-neighbor_bounding_radius, x+neighbor_bounding_radius, y+neighbor_bounding_radius)
            collision_bb = BoundingBox(x-collision_bounding_radius, y-collision_bounding_radius, x+collision_bounding_radius, y+collision_bounding_radius)
            collisions = quadTree.within_bb(collision_bb)
            neighbors = quadTree.within_bb(neighbor_bb)



            



            avg_x, avg_y, avg_vel_x, avg_vel_y = self.get_average_position_and_velocity_points(neighbors)
            # avg_x, avg_y = self.get_average_position()
            avg_x_c, avg_y_c, avg_vel_x_c, avg_vel_y_c = self.get_average_position_and_velocity_points(collisions)
            boid.x_velocity, boid.y_velocity = self.turn_toward(boid.x, boid.y, boid.x_velocity, boid.y_velocity, avg_x, avg_y, math.radians(turn_speed), boid.speed)
            boid.x_velocity, boid.y_velocity = self.align_vector(boid.x_velocity, boid.y_velocity, avg_vel_x, avg_vel_y, align_rate, False)
            boid.x_velocity, boid.y_velocity = self.align_vector(boid.x_velocity, boid.y_velocity, avg_vel_x_c, avg_vel_y_c, away_rate, True)
            # self.rotate_away_from_obstacle(boid, avg_x_c, avg_y_c, .5, .5)

            boid.x += boid.x_velocity
            boid.y += boid.y_velocity

            

    def check_borders(self):
        for boid in self.boids:
            if boid.x >= x_scale or boid.x <= 0:
                if boid.x >= x_scale:
                    boid.x = x_scale
                else:
                    boid.x = 0
                boid.x_velocity *= -1
            if boid.y >= y_scale or boid.y <= 0:
                if boid.y >= y_scale:
                    boid.y = y_scale
                else:
                    boid.y = 0
                boid.y_velocity *= -1

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
        self.speed = 2
        self.x_velocity = randint(-10,10)/100
        self.y_velocity = randint(-10,10)/100
        # self.x_velocity = 1
        # self.y_velocity = 1
        self.avg_x = 0
        self.avg_y = 0
        self.size = size

    def draw(self):
        dudraw.filled_circle(self.x, self.y, self.size)
        dudraw.line(self.x, self.y, self.x + self.x_velocity * 4, self.y + self.y_velocity * 4)
    def update_velocity():
        pass
    def __str__(self):
        return f"Boid({self.x}, {self.y})"

    

b = AllBoids(800)
b.draw()


collision_radius = randint(1,7)
neighbor_radius = randint(10,100)
turn_speed = randint(1,2)
align_rate = randint(1,10)/10
away_rate = randint(1,10)/13
while away_rate > align_rate * .9:
    away_rate = randint(1,10)/5

print("collision_radius: ", collision_radius)
print("neighbor_radius: ", neighbor_radius)
print("turn_speed: ", turn_speed)
print("align_rate: ", align_rate)
print("away_rate: ", away_rate)



x = 0
while True:
    b.draw()
    b.boids_approach_average(7, 15, .01, .4, .27)
    # b.boids_approach_average(collision_radius, neighbor_radius, turn_speed, align_rate, away_rate)
    b.check_borders()
    dudraw.show(1)
    dudraw.clear()
    x += 1



# hall of fame
# b.boids_approach_average(7, 15, .01, .4, .27)
# b.boids_approach_average(5, 19, 5, .1, .1)
# b.boids_approach_average(7, 16, .3, .3, .3)
# b.boids_approach_average(7, 15, .01, .3, .27)
# b.boids_approach_average(7, 30, .3, .1, .1)
# b.boids_approach_average(7, 50, 2, .02, .02)




"""
https://stackoverflow.com/questions/3939433/determine-points-within-a-given-radius-algorithm
https://www.youtube.com/watch?v=4LWmRuB-uNU
https://www.geeksforgeeks.org/quad-tree/
https://quads.readthedocs.io/en/latest/
https://www.reddit.com/r/gameenginedevs/comments/jp30c6/efficient_and_well_explained_implementation_of_a/
https://www.google.com/search?q=what+does+normalizeing+a+vecor+mean&oq=what+does+normalizeing+a+vecor+mean&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIJCAEQABgNGIAEMg0IAhAAGIYDGIAEGIoFMg0IAxAAGIYDGIAEGIoFMgoIBBAAGKIEGIkFMgoIBRAAGKIEGIkF0gEIOTA5MWowajeoAgCwAgA&sourceid=chrome&ie=UTF-8
https://www.youtube.com/watch?v=gpc7u3331oQ
https://eater.net/boids
https://jrtechs.net/data-science/implementing-a-quadtree-in-python


"""