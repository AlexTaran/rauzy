#!/usr/bin/python

from modules.sequence_generator import SequenceGenerator
from modules.vector3 import Vector3
from modules.matrix44 import Matrix44
from modules.camera import Camera
from modules.utils import *
from modules.VertexBuffer import VertexBuffer
from modules.Shader import Shader

import pygame
import sys
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from ctypes import c_void_p

from math import sqrt
from numpy import *
from bigfloat import *

from operator import itemgetter

def draw_coordinate_system(sz = 1.0):
  glLineWidth(1.0)
  glBegin(GL_LINES)
  glColor3f(1.0, 0.0, 0.0)
  glVertex3f(0.0, 0.0, 0.0)
  glVertex3f(1.0, 0.0, 0.0)
  glColor3f(0.0, 1.0, 0.0)
  glVertex3f(0.0, 0.0, 0.0)
  glVertex3f(0.0, 1.0, 0.0)
  glColor3f(0.0, 0.0, 1.0)
  glVertex3f(0.0, 0.0, 0.0)
  glVertex3f(0.0, 0.0, 1.0)
  glEnd()

def gl_init():
  glEnable(GL_DEPTH_TEST)
  glShadeModel(GL_SMOOTH)
  glClearColor(0.0, 0.0, 0.0, 0.0)
  glEnable(GL_COLOR_MATERIAL)

def resize(w, h):
  glViewport(0, 0, w, h)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluPerspective(60.0, float(w)/h, .1, 1000.)
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()


def main():
  if len(sys.argv) != 2:
    print "Wring number of args!"
    return
  CURRENT_POINT_SIZE = 4.0
  CURRENT_STEP = 0.001

  pygame.init()
  display_info = pygame.display.Info()
  screen = pygame.display.set_mode((display_info.current_w, display_info.current_h),
                                   HWSURFACE|OPENGL|DOUBLEBUF|FULLSCREEN)
  clock = pygame.time.Clock()
  resize(display_info.current_w, display_info.current_h)
  projection_matrix = Matrix44.perspective_projection_fov(60.0/180.0*3.14159265358,
                        float(display_info.current_w)/display_info.current_h, .1, 1000.)
  gl_init()

  movement_speed = 5.0
  look_around_speed = 0.005

  pygame.mouse.set_visible(False)
  pygame.event.set_grab(True)

  sequence_iterations = int(sys.argv[1])

  vbo3 = VertexBuffer()
  vbo3.bind(GL_ARRAY_BUFFER)
  with open('../generator/gen/v' + str(sequence_iterations) + ".gen") as f:
    v3 = f.read()
  with open('../generator/gen/c' + str(sequence_iterations) + ".gen") as f:
    c4 = f.read()
  with open('../generator/gen/n' + str(sequence_iterations) + ".gen") as f:
    n4 = f.read()
  with open('../generator/gen/f' + str(sequence_iterations) + ".gen") as f:
    f4 = f.read()
  vbo3.setBinaryData(v3 + c4 + n4, GL_STATIC_DRAW)
  vbo3.unBind()

  faces_vbo = VertexBuffer()
  faces_vbo.bind(GL_ARRAY_BUFFER)
  with open('../generator/gen/f' + str(sequence_iterations) + ".gen") as f:
    f4 = f.read()
  faces_vbo.setBinaryData(f4, GL_STATIC_DRAW)
  faces_vbo.unBind()

  light_angle_phi = 0.0
  light_angle_theta = 0.0

  print "Rendering ",len(c4) / 12, " points"

  print "GLSL Version: ", glGetString(GL_SHADING_LANGUAGE_VERSION)
  simple = Shader()
  simple.loadFromFile('shaders/simplest.txt')

  camera = Camera()
  clock.tick()
  pygame.mouse.get_rel()
  first_mouse_event_skipped = False
  while True:
    pressed = pygame.key.get_pressed()
    finished = False
    for event in pygame.event.get():
      if event.type == QUIT:
        finished = True
        break
      if event.type == KEYUP and event.key == K_ESCAPE:
        finished = True
        break
      if event.type == KEYUP and event.key == K_RIGHTBRACKET:
        if CURRENT_POINT_SIZE < 10.0:
          CURRENT_POINT_SIZE += 1.0
      if event.type == KEYUP and event.key == K_LEFTBRACKET:
        if CURRENT_POINT_SIZE > 1.0:
          CURRENT_POINT_SIZE -= 1.0
      if event.type == KEYUP and event.key == K_p:
        normal = list(camera._dir)
        print normal
      if event.type == KEYUP:
        if event.key == K_9:
          CURRENT_STEP /= 10.0
        if event.key == K_0:
          CURRENT_STEP *= 10.0
        if event.key == K_y:
          normal[0] -= CURRENT_STEP
        if event.key == K_u:
          normal[0] += CURRENT_STEP
        if event.key == K_h:
          normal[1] -= CURRENT_STEP
        if event.key == K_j:
          normal[1] += CURRENT_STEP
        if event.key == K_n:
          normal[2] -= CURRENT_STEP
        if event.key == K_m:
          normal[2] += CURRENT_STEP
    if finished:
      break
    time_passed = clock.tick()
    time_passed_seconds = time_passed / 1000.0
    light_angle_phi   += time_passed_seconds * 0.3
    light_angle_theta += time_passed_seconds * 0.1
    while light_angle_phi > 2 * pi:
      light_angle_phi -= 2 * pi
    while light_angle_theta > 2 * pi:
      light_angle_theta -= 2 * pi
    ## handling camera
    movement_direction = 0.0
    strafe_direction   = 0.0
    if pressed[K_w]:
      movement_direction =  1.0
    if pressed[K_s]:
      movement_direction = -1.0
    if pressed[K_d]:
      strafe_direction =  1.0
    if pressed[K_a]:
      strafe_direction = -1.0
    camera.move       (time_passed_seconds * movement_speed * movement_direction)
    camera.strafeRight(time_passed_seconds * movement_speed * strafe_direction)
    dx, dy = pygame.mouse.get_rel()
    if not first_mouse_event_skipped:
      if dx != 0 or dy != 0:
        dx = 0
        dy = 0
        first_mouse_event_skipped = True
    camera.rotateHoriz(-dx * look_around_speed)
    camera.rotateVert (-dy * look_around_speed)
    ## now render
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPointSize(CURRENT_POINT_SIZE)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glLoadMatrixd(projection_matrix.to_opengl())
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #glTranslatef(0.0, 0.0, -5.0)
    glLoadMatrixd(camera.getLookAtMatrix().to_opengl())
    draw_coordinate_system()
    MVP = projection_matrix * camera.getLookAtMatrix()
    ### 4D simple shader render
    simple.bind()
    simple.enableAttrArray('pos', True)
    simple.enableAttrArray('col', True)
    simple.enableAttrArray('nrm', True)
    simple.setUniformMat4('MVP', MVP)
    light_dir = Vector3(cos(light_angle_phi) * cos(light_angle_theta),
                        sin(light_angle_theta),
                        sin(light_angle_phi) * sin(light_angle_theta))
    simple.setUniformVec3('light_dir', light_dir)
    #print Vector3(cos(light_angle), 0.0, sin(light_angle))
    vbo3.bind(GL_ARRAY_BUFFER)
    glVertexAttribPointer(simple.getAttribLocation('pos'), 3, GL_FLOAT, GL_FALSE, 0, c_void_p(0))
    glVertexAttribPointer(simple.getAttribLocation('col'), 3, GL_FLOAT, GL_FALSE, 0, c_void_p(len(v3)))
    glVertexAttribPointer(simple.getAttribLocation('nrm'), 3, GL_FLOAT, GL_FALSE, 0, c_void_p(len(v3)+len(c4)))
    glDrawArrays(GL_POINTS, 0, len(v3) / 12)
    vbo3.unBind()
    faces_vbo.bind(GL_ARRAY_BUFFER)
    stride = 9 * 4 # nine floats
    glVertexAttribPointer(simple.getAttribLocation('pos'), 3, GL_FLOAT, GL_FALSE, stride, c_void_p(0))
    glVertexAttribPointer(simple.getAttribLocation('col'), 3, GL_FLOAT, GL_FALSE, stride, c_void_p(3 * 4))
    glVertexAttribPointer(simple.getAttribLocation('nrm'), 3, GL_FLOAT, GL_FALSE, stride, c_void_p(6 * 4))
    glDrawArrays(GL_TRIANGLES, 0, len(f4) / 9 / 4)
    faces_vbo.unBind()
    simple.unBind()

    #glPointSize(25.0)
    glLineWidth(15.0)
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
    light_R1 = 4.0
    light_R2 = 3.0
    glVertex3f(light_R1 * light_dir.x, light_R1 * light_dir.y, light_R1 * light_dir.z)
    glVertex3f(light_R2 * light_dir.x, light_R2 * light_dir.y, light_R2 * light_dir.z)
    glEnd()
    ### final flip
    pygame.display.flip()

  pygame.event.set_grab(False)
  pygame.mouse.set_visible(True)

if __name__ == "__main__":
  main()
