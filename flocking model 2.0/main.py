from boid import *
from vpython import *
from random import uniform 
from typing import List
from threading import Thread

N_BOIDS = 50
# raggio massimo dello spawn dei boidi dall'origine
MAX_RADIUS = 1000
# distanza della parete dall'origine
BOX_DIST = sqrt(MAX_RADIUS)

def setupScene(scene):
   scene.width = 1280
   scene.height = 720

# crea il box, per rendere più visibile il movimento
def setupBox():
   # floor
   box(pos = vector(0, -BOX_DIST, 0), color = color.blue, length = BOX_DIST*2, height =.1, width = BOX_DIST*2)
   # ceiling
   box(pos = vector(0, BOX_DIST, 0), color = color.blue, length = BOX_DIST*2, height =.1, width = BOX_DIST*2)
   # left wall
   box(pos = vector(BOX_DIST, 0, 0), color = color.green, length = .1, height = BOX_DIST*2, width = BOX_DIST*2)
   # depth wall
   box(pos = vector(0, 0, -BOX_DIST), color = color.purple, length = BOX_DIST*2, height = BOX_DIST*2, width = .1)
   # right wall
   # box(pos = vector(-BOX_DIST, 0, 0), color = color.green, length = .1, height = BOX_DIST*2, width = BOX_DIST*2)

def applyForceBoid(boid: Boid):
   boid.applyForce(boid.forceCohesion())
   boid.applyForce(boid.forceAlignment())
   boid.applyForce(boid.forceSeparation())
   # applica una forza verso l'origine, necessario altrimenti i boidi andrebbero
   # troppo lontani e la camera non riuscirebbe a seguirli
   boid.applyForce(boid.forceToCenter())

def main():
   setupScene(scene)
   setupBox()

   #spawn dei boidi
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

   # while necessario all'animazione, rate si comporta come uno sleep (scandisce i frame)
   threads:List[Thread] = []
   while True:
      rate(100)

      # per ogni boide, la funzione applyForceBoid, viene eseguita come thread
      for boid in boids:
         th = Thread(target=applyForceBoid, args=(boid,))
         threads.append(th)
         th.start()

      # serve per essere sicuri che tutti i thread siano terminati, o aspettare la loro terminazione
      for thread in threads:
         thread.join()

      # azioni da eseguire ad ogni frame per ogni boide
      for boid in boids:
         boid.frame(boids)
         boid.resetForce()
      
      threads = []

# il codice deve essere avviato solamente
# se questo file viene avviato come uno script
if __name__ == "__main__":
   main()