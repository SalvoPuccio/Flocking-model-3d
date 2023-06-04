from random import random as rand
from vpython import *
from math import isclose as isclose, atan

# class*
class Boid:
   RADIUS = 1
   # raggio in cui si percepiscono i vicini, per coesione e allineamento
   NEIGHBOR_RADIUS = 20
   # raggio in cui un vicino è considerato da "scansare"
   SEPARATION_RADIUS = 10
   MAX_SPEED = 0.5
   MAX_FORCE_MAGNITUDE = 0.01
   FORCE_TOCENTER_FACTOR = 25.0
   NULL_VECTOR = vector(0, 0, 0)

   def __init__(self, position: vector, velocity: vector):
      self.acceleration = vector(0, 0, 0)
      self.shape = sphere(pos = position, radius = Boid.RADIUS, velocity = velocity)
      self.neigh = []
      self.closeNeigh = []

   def applyForce(self, force: vector):
      self.acceleration += force

   def resetForce(self):
      self.acceleration = vector(0, 0, 0)

   def frame(self, boids: list):
      self.shape.pos += self.shape.velocity
      self.shape.velocity += self.acceleration
      self.updateNeigh(boids)

   # forza verso il centro dei vicini
   def forceCohesion(self) -> vector:
      if len(self.neigh) == 0:
         return Boid.NULL_VECTOR

      sum = Boid.NULL_VECTOR
      for neigh in self.neigh:
         sum += neigh.shape.pos
      
      force = sum / len(self.neigh)
      
      # limite alla forza, usiamo la norma per tenere 
      # conto della forza preesistente e al contemo la limitiamo
      if force.mag > Boid.MAX_FORCE_MAGNITUDE:
         force = force.norm() * (Boid.MAX_FORCE_MAGNITUDE)

      return force

   def forceAlignment(self) -> vector:
      if len(self.neigh) == 0:
         return Boid.NULL_VECTOR

      sum = Boid.NULL_VECTOR
      for neigh in self.neigh:
         sum += neigh.shape.velocity
      
      force = sum / len(self.neigh)
      if force.mag > Boid.MAX_FORCE_MAGNITUDE:
         force = force.norm() * (Boid.MAX_FORCE_MAGNITUDE)

      return force

   def forceSeparation(self) -> vector:
      sum = Boid.NULL_VECTOR
      count = 0

      # ad ogni boide troppo vicino associa una forza repulsiva
      # pesata sulla distanza
      for (neigh, euc_dis) in self.closeNeigh:
         sum += (self.shape.pos - neigh.shape.pos).norm() / euc_dis
         count += 1

      if count == 0:
         return Boid.NULL_VECTOR

      # media le forze repulsive
      force = sum / count  

      # limite alla forza, come al solito tiene conto 
      # della forza preesistente
      if not isclose(force.mag, 0):
         force = force.norm() * (Boid.MAX_SPEED)
         force -= self.shape.velocity # ??????????????????????????????????????????????????????????????

         if force.mag > Boid.MAX_FORCE_MAGNITUDE:
            force = force.norm() * (Boid.MAX_FORCE_MAGNITUDE)

      return force

   def forceToCenter(self) -> vector:
      centerDistance = (self.shape.pos - Boid.NULL_VECTOR).mag
      factor = 1.0 / pi * atan((centerDistance - Boid.FORCE_TOCENTER_FACTOR) / 4.0) + 0.5
      force = (-self.shape.pos).norm()
      
      if force.mag > Boid.MAX_FORCE_MAGNITUDE * 8: # 8?????????
         force = force.norm()
         force *= Boid.MAX_FORCE_MAGNITUDE * 8
      force *= factor

      return force

   def updateNeigh(self, boids):
      for boid in boids:
         # distanza calcolata dal centro delle sfere
         euc_dis = (self.shape.pos - boid.shape.pos).mag 
         # anche se è lo stesso punto, non ritorna proprio 0
         if (euc_dis < Boid.NEIGHBOR_RADIUS) and not isclose(euc_dis, 0.0): 
            self.neigh.append(boid) 
            if euc_dis < Boid.SEPARATION_RADIUS:
               self.closeNeigh.append((boid, euc_dis))
