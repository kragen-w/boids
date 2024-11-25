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

x_scale = 400
y_scale = 400
dudraw.set_canvas_size(800,800)

dudraw.set_x_scale(0,x_scale)
dudraw.set_y_scale(0,y_scale)


class AllBoids:
    def __init__(self, count, neighbor_radius, collision_radius):
        self.boids = []
        self.coll_rad = collision_radius#put this in loop for changing this on the fly in the future
        self.neigh_rad = neighbor_radius
        for i in range(count):
            random1 = randint(60, x_scale - 60)
            random2 = randint(60, y_scale - 60)
            self.boids.append((Boid(random1, random2, 1)))
        
        self.mouse_x = x_scale/2
        self.mouse_y = y_scale/2
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
    


    def move_to_neighbors(self):
        quadTree = QuadTree((x_scale/2,y_scale/2), x_scale, y_scale)
        for boid in self.boids:
            quadTree.insert((boid.x,boid.y), boid)
        for boid in self.boids:




            # neighbor_bb = BoundingBox(round(x-self.neigh_rad), round(y-self.neigh_rad), round(x+self.neigh_rad), round(y+self.neigh_rad))
            # collision_bb = BoundingBox(x-self.coll_rad, y-self.coll_rad, x+self.coll_rad, y+self.coll_rad)
            # collisions = quadTree.within_bb(collision_bb)
            # neighbors = quadTree.within_bb(neighbor_bb)


            neighbor_bb = BoundingBox(boid.x-self.neigh_rad, boid.y-self.neigh_rad, boid.x+self.neigh_rad, boid.y+self.neigh_rad)
            collision_bb = BoundingBox(boid.x-self.coll_rad,boid.y-self.coll_rad, boid.x+self.coll_rad, boid.y+self.coll_rad)
            collisions = quadTree.within_bb(collision_bb)
            neighbors = quadTree.within_bb(neighbor_bb)

            self.mouse_x = dudraw.mouse_x()
            self.mouse_y = dudraw.mouse_y()

            boid.bird_brain()
            boid.move_away(collisions)
            
            boid.move_twards(neighbors)
            boid.speed_limit()
            boid.avoid_borders()
            boid.align(neighbors)
            # boid.bird_brain()
            boid.x += boid.dx
            boid.y += boid.dy

    
        

class Boid:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.dx = randint(-30,30)/10
        self.dy = randint(-30,30)/10
        self.size = size

    def draw(self):
        dudraw.filled_circle(self.x, self.y, self.size)
        dudraw.line(self.x, self.y, self.x + self.dx * 5, self.y + self.dy * 5)
    def update_velocity():
        pass
    def __str__(self):
        return f"Boid({self.x}, {self.y})"
    def loop(self, neighbors, collisions):

        pass

    def move_twards(self, other_boids):
        move_factor_x = 0
        move_factor_y = 0
        move_rate_twards = 0.0019
        for boid in other_boids:
            move_factor_x += boid.data.x
            move_factor_y += boid.data.y

        
        if len(other_boids) != 0:
            move_factor_x /= len(other_boids)
            move_factor_y /= len(other_boids)

            self.dx += (move_factor_x - self.x) * move_rate_twards
            self.dy += (move_factor_y - self.y) * move_rate_twards
# this is different becuase you add the vectors to it, making it large if there are a lot of nearby boids they have to avoid
    def move_away(self, other_boids):
        move_factor_x = 0
        move_factor_y = 0
        move_rate_away = 0.01
        for boid in other_boids:
            distance = math.sqrt((boid.data.x - self.x) ** 2 + (boid.data.y - self.y) ** 2) + .001
            move_factor_x += (self.x - boid.data.x) * (move_rate_away / distance)
            move_factor_y += (self.y - boid.data.y) * (move_rate_away / distance)

        
       

        self.dx += move_factor_x 
        self.dy += move_factor_y 


    def align(self, other_boids):
        avg_dx = 0
        avg_dy = 0
        align_rate = .07


        for boid in other_boids:
            avg_dx += boid.data.dx
            avg_dy += boid.data.dy

        if len(other_boids) != 0:
            avg_dx = avg_dx / len(other_boids)
            avg_dy = avg_dy / len(other_boids)

        self.dx += (avg_dx) * align_rate
        self.dy += (avg_dy) * align_rate
        


    def avoid_borders(self):
        border_width = 60
        if self.x > x_scale - border_width:
            if self.x > x_scale - border_width / 2:
                    self.dx -= .1
            self.dx -= .05
        if self.x < border_width:
            if self.x < border_width / 2:
                self.dx += .1
            self.dx += .05
        if self.y > y_scale - border_width:
            if self.y > y_scale - border_width / 2:
                    self.dy -= .1
            self.dy -= .05
        if self.y < border_width:
            if self.y < border_width / 2:
                self.dy += .1
            self.dy += .05
        
    def speed_limit(self):
        speed_limit = 1
        speed = math.sqrt(self.dx * self.dx + self.dy * self.dy)
        if speed > speed_limit:
            self.dx = (self.dx / speed) * speed_limit
            self.dy = (self.dy / speed) * speed_limit

        # speed_lower_limit = 1
        # if speed < speed_lower_limit:
        #     self.dx = (self.dx / speed) * speed_limit
        #     self.dy = (self.dy / speed) * speed_limit

        # if speed > speed_limit:
        #     self.dx *= .9
        #     self.dy *= .9

        # else:
        #     self.dx *= 1.1
        #     self.dy *= 1.1
        
    def bird_brain(self):
        self.dx += randint(-100,100)/1000
        self.dy += randint(-100,100)/1000

b = AllBoids(200, 13, 10)
b.draw()


x = 0
while True:
    b.draw()
    b.move_to_neighbors()
    # b.boids_approach_average(collision_radius, neighbor_radius, turn_speed, align_rate, away_rate)
    # b.check_borders()
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