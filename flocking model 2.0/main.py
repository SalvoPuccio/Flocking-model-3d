from boid import *
from vpython import *
from random import uniform 
from typing import List

N_BOIDS = 10

# raggio massimo i
MAX_RADIUS = 1000

def setupScene(scene):
   scene.width = 1280
   scene.height = 720

def main():
   setupScene(scene)

   boids:List[Boid] = []
   for _ in range(0, N_BOIDS):
      
      # tutti i boidi devono essere dentro 
      # una 'sfera' di raggio 'MAX_RADIUS'
      while True:
         x = uniform(-1, 1) * MAX_RADIUS
         y = uniform(-1, 1) * MAX_RADIUS
         z = uniform(-1, 1) * MAX_RADIUS 

         if x * x + y * y + z * z < MAX_RADIUS:
            break
      
      velocity = vector(uniform(-0.01, 0.01), uniform(-0.01, 0.01), uniform(-0.01, 0.01))
      boids.append(Boid(vector(x, y, z), velocity))

   while True:
      rate(60)

      for boid in boids:
         boid.applyForce(boid.forceCohesion())
         boid.applyForce(boid.forceAlignment())
         boid.applyForce(boid.forceSeparation())
         boid.applyForce(boid.forceToCenter())

      for boid in boids:
         boid.frame(boids)
         boid.resetForce()

# il codice deve essere avviato solamente
# se questo file viene avviato come uno script
if __name__ == "__main__":
   main()