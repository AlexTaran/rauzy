SCREEN_SIZE = (1366, 768)

from math import radians 

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.ARB import *

import pygame
from pygame.locals import *

from gameobjects.matrix44 import *
from gameobjects.vector3 import *
from gameobjects.locals import *

from Core.camera import *
from Core.VertexBuffer import *
from Core.Shader import *
from Core.Model import *
from Core.modelgen import *
from Core.Simple import *
from Core.Texture import *
from Core.Scene import *
from Core.SceneObject import *
from Maps.TestMap import *
#from VertexArray import *
from Core.Font import *
from Core.FrameBuffer import *
from Core.util import *

def resize(width, height):
    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #gluPerspective(60.0, float(width)/height, .1, 1000.)
    mat = Matrix44.perspective_projection_fov(60.0/180.0*3.14159265358, float(SCREEN_SIZE[0])/SCREEN_SIZE[1], .1, 1000.)
    glLoadMatrixf(mat._m)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    
    glEnable(GL_DEPTH_TEST)
    
    glShadeModel(GL_SMOOTH)
    glClearColor(1.0, 1.0, 1.0, 0.0)

    glEnable(GL_COLOR_MATERIAL)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)        
    glLight(GL_LIGHT0, GL_POSITION,  (0, 1, 1, 0))    
    #glEnable(GL_CULL_FACE)
    #glCullFace(GL_FRONT)
    
cam = None
skbShader = None
scene = None

def renderSkyBox():
    q = scene._models['quad']
    glDisable(GL_DEPTH_TEST)
    skbShader.bind()
    q._vbo.bind(GL_ARRAY_BUFFER)
    skbShader.enableAttrArray('position',True)
    skbShader.enableAttrArray('texcoord',True)
    q.bindAttrPosition(skbShader.getAttribLocation('position'))
    q.bindAttrTexcoord(skbShader.getAttribLocation('texcoord'))
    glUniform1i(skbShader.getUniformLocation('decalMap'),0)
    mv = Matrix44.perspective_projection_fov(60.0/180.0*3.14159265358, float(SCREEN_SIZE[0])/SCREEN_SIZE[1], .1, 1000.) * cam.getRotationMatrix() 
    glActiveTexture(GL_TEXTURE0)
    
    scene._textures[scene._skybox[0]].bind(GL_TEXTURE_2D)
    md = Matrix44.x_rotation(-math.pi*0.5)*Matrix44.z_rotation(math.pi*0.5) *Matrix44.translation(0.0,-5.0,0.0)
    skbShader.setUniformMat4('mvpMatrix',mv*md )
    q.callDrawArrays()
    
    scene._textures[scene._skybox[1]].bind(GL_TEXTURE_2D)
    md = Matrix44.x_rotation(-math.pi*0.5)*Matrix44.z_rotation(-math.pi*0.5) *Matrix44.translation(0.0,-5.0,0.0)
    skbShader.setUniformMat4('mvpMatrix',mv*md )
    q.callDrawArrays()
    
    scene._textures[scene._skybox[2]].bind(GL_TEXTURE_2D)
    md = Matrix44.y_rotation(math.pi) * Matrix44.z_rotation(-math.pi) * Matrix44.translation(0.0,-5.0,0.0)
    skbShader.setUniformMat4('mvpMatrix',mv*md )
    q.callDrawArrays()
    
    scene._textures[scene._skybox[3]].bind(GL_TEXTURE_2D)
    md = Matrix44.translation(0.0,-5.0,0.0)
    skbShader.setUniformMat4('mvpMatrix',mv*md )
    q.callDrawArrays()
    
    scene._textures[scene._skybox[4]].bind(GL_TEXTURE_2D)
    md = Matrix44.x_rotation(-math.pi*0.5) *Matrix44.translation(0.0,-5.0,0.0)
    skbShader.setUniformMat4('mvpMatrix',mv*md )
    q.callDrawArrays()
    
    scene._textures[scene._skybox[5]].bind(GL_TEXTURE_2D)
    md = Matrix44.z_rotation(-math.pi) * Matrix44.x_rotation(math.pi*0.5) *Matrix44.translation(0.0,-5.0,0.0)
    skbShader.setUniformMat4('mvpMatrix',mv*md )
    q.callDrawArrays()
    
    q._vbo.unBind()
    glBindTexture(GL_TEXTURE_2D,0)
    skbShader.unBind()
    glEnable(GL_DEPTH_TEST)

def near_callback(args,g1,g2):
    contacts = ode.collide(g1, g2)
    world,contactgroup = args
    for c in contacts:
        c.setBounce(0.1)
        c.setMu(50.)
        j = ode.ContactJoint(world, contactgroup, c)
        b1 = g1.getBody()
        b2 = g2.getBody()
        j.attach(b1, b2)
        '''if b1!=None and b2!=None:
            
            #print b1,b2
            pass
        else:
            #print b1,b2
            pass'''
    pass

def run():
    global cam
    cam = Camera()
    
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF|FULLSCREEN)
    
    resize(*SCREEN_SIZE)
    init()
    
    vbo = VertexBuffer()
    vbo.bind(GL_ARRAY_BUFFER);
    del vbo
    
    fbo = FrameBuffer()
    fbo.bind()
    fbo.unBind()
    del fbo
    
    ############## FONT LOAD
    fnt = Font('Content/Fonts/treb.fnt','Content/Fonts/treb.png','Content/Shaders/font.txt')
    ############## END FONT LOAD
    
    shader = Shader()
    shader.loadFromFile('Content/Shaders/bump.txt')
    
    global skbShader
    skbShader = Shader()
    skbShader.loadFromFile('Content/Shaders/skybox.txt')
    #ModelGen
    
    #print glInitVertexBufferObjectARB()
    #print glInitVertexArrayObjectARB()
    
    #vao = VertexArray()
    #print vao._vaoId
    
    clock = pygame.time.Clock()    
    
    glMaterial(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))    
    glMaterial(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))

    # This object renders the 'map' 
    
    v,c,n = ModelGen.genCube(1.0)
    cube = Model()
    cube.load(v,c,n)
    
    tex = Texture()
    tex.bind(GL_TEXTURE_2D)
    loadTexture2D('Content/Textures/brick_diffuse.jpg')
    tex.unBind()
    
    tex1 = Texture()
    tex1.bind(GL_TEXTURE_2D)
    loadTexture2D('Content/Textures/brick_normalmap.jpg')
    tex1.unBind()
    global scene
    scene = TestMap1()
    scene.load()
    scene.respawnBall()
   # print scene._models['quad']._mesh._nverts

    # Camera transform matrix
    camera_matrix = Matrix44()
    camera_matrix.translate = (10.0, .6, 10.0)

    # Initialize speeds and directions
    rotation_direction = Vector3()
    rotation_speed = radians(90.0)
    movement_direction = Vector3()
    movement_speed = 5.0
    look_around_speed = 0.01

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    pygame.mouse.get_rel() # clean relative movements
    
    lastFps = "Unknown"
    fpsCounter = 0
    timeCounter = 0.0
    
    lightpos = Vector3(5.0,5.0,5.0)
    angle = 0.0
    contactgroup = ode.JointGroup()
    clock.tick()
    look_mode = 1
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                #print shader._attribs
                return                
            
        # Clear the screen, and z-buffer
        
                        
        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.
        
        angle +=time_passed_seconds*0.6
        lightpos = Vector3(5.0+8.0*math.sin(angle),5.0,5.0+8.0*math.cos(angle))
        
        # count fps
        fpsCounter+=1
        timeCounter+=time_passed_seconds
        if timeCounter>=1.0:
            timeCounter = 0
            lastFps = fpsCounter
            fpsCounter = 0
        pressed = pygame.key.get_pressed()

        if look_mode == 0:
            movement_direction = 0.0
            strafe_direction = 0.0
   
            if pressed[K_w]:
                movement_direction = +1.0
            elif pressed[K_s]:
                movement_direction = -1.0
            if pressed[K_a]:
                strafe_direction = -1.0
            elif pressed[K_d]:
                strafe_direction = +1.0
            if pressed[K_RETURN]:
                look_mode+=1
                if look_mode>1:
                    look_mode=0
            cam.move(time_passed_seconds*movement_speed*movement_direction)
            cam.strafeRight(time_passed_seconds*movement_speed*strafe_direction)
        
            dx,dy = pygame.mouse.get_rel()
            cam.rotateHoriz(-dx*look_around_speed)
            cam.rotateVert(-dy*look_around_speed)
        if look_mode == 1:
            dx,dy = pygame.mouse.get_rel()
            cam.rotateHoriz(-dx*look_around_speed)
            cam.rotateVert(-dy*look_around_speed)
            x,y,z = scene._objects['sphere']._body.getPosition()
            cam._pos = Vector3(x,y,z)
            cam.move( -4.0)
            koef = 40.0

            x,y,z = cam._dir.as_tuple()
            if pressed[K_w]:
                scene._objects['sphere']._body.addForce( (x*koef,0.0,z*koef) )
            elif pressed[K_s]:
                scene._objects['sphere']._body.addForce( (-x*koef,0.0,-z*koef) )
            x,y,z = cam.getRight().as_tuple()
            if pressed[K_a]:
                scene._objects['sphere']._body.addForce( (-x*koef,0.0,-z*koef) )
            elif pressed[K_d]:
                scene._objects['sphere']._body.addForce( (x*koef,0.0,z*koef) )
            if pressed[K_SPACE]:
                scene._objects['sphere']._body.addForce( (0.0,5.0*koef,0.0) )

        # physics simulation
        #print 'brkp0'
        if time_passed_seconds>0.0:
            scene._space.collide( (scene._world,contactgroup) ,near_callback)
            #print 'brkp1 ',time_passed_seconds
            scene._world.step(0.01*0.0 + time_passed_seconds)
            #print 'brkp2'
            contactgroup.empty()
            #print 'brkp3'
        
        camMatrix = cam.getLookAtMatrix()
        
        # Upload the inverse camera matrix to OpenGL
        # glLoadMatrixd(camera_matrix.get_inverse().to_opengl())
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        renderSkyBox()
        #glClear(GL_DEPTH_BUFFER_BIT);
        
        glLoadMatrixd(camMatrix.to_opengl())        
        # Light must be transformed as well
        glLight(GL_LIGHT0, GL_POSITION,  (0, 1.5, 1, 0)) 
                
        # Render the map
        #map.render()
        
        #render cube
        pm = Matrix44.perspective_projection_fov(60.0/180.0*3.14159265358, float(SCREEN_SIZE[0])/SCREEN_SIZE[1], .1, 1000.)
        vi = camMatrix
        #vi = Matrix44.translation(0.0,0.0,-7.0) * Matrix44.xyz_rotation(0.0,0.0,0.0)
        sc = Matrix44.scale(1.0,-1.0,1.0)
        MVP = pm*vi
        #################
        shader.bind()
        shader.enableAttrArray('position',True)
        shader.enableAttrArray('texcoord',True)
        shader.enableAttrArray('normal'  ,True)
        shader.enableAttrArray('tangent',True)
        shader.enableAttrArray('binormal',True)
        shader.setUniformVec3('eyePos',cam._pos)
        shader.setUniformVec3('lightPos',lightpos)
        glUniform1i(shader.getUniformLocation('decalMap'),0)
        glUniform1i(shader.getUniformLocation('normalMap'),1)
        glUniform1i(shader.getUniformLocation('heightMap'),2)
        for obj in scene._objects:
            o = scene._objects[obj]
            dm = scene._textures[o._decalMap]
            nm = scene._textures[o._normalMap]
            hm = scene._textures[o._heightMap]
            glActiveTexture(GL_TEXTURE2)
            hm.bind(GL_TEXTURE_2D)
            glActiveTexture(GL_TEXTURE1)
            nm.bind(GL_TEXTURE_2D)
            glActiveTexture(GL_TEXTURE0)
            dm.bind(GL_TEXTURE_2D)
            #shader.setUniformMat4('mMatrix',o._modelMatrix)
            if o._body != None:
                 shader.setUniformMat4('mMatrix',getTransformMatrixFromBody(o._body))
                 shader.setUniformMat4('mvpMatrix',pm*vi*getTransformMatrixFromBody(o._body))
            else:
                 shader.setUniformMat4('mMatrix',o._modelMatrix)
                 shader.setUniformMat4('mvpMatrix',pm*vi*o._modelMatrix)
            #print o._modelMatrix
            shader.setUniformVec3('ambient',o._ambient)
            shader.setUniformVec3('diffuse',o._diffuse)
            shader.setUniformVec3('specular',o._specular)
            glUniform1f(shader.getUniformLocation('shininess'),o._shininess)
            glUniform1f(shader.getUniformLocation('scale'),o._scale)
            glUniform1f(shader.getUniformLocation('bias'),o._bias)
            m = scene._models[o._modelName]
            m._vbo.bind(GL_ARRAY_BUFFER)
            m.bindAttrPosition(shader.getAttribLocation('position'))
            m.bindAttrTexcoord(shader.getAttribLocation('texcoord'))
            m.bindAttrNormal(shader.getAttribLocation('normal'))
            m.bindAttrTangent(shader.getAttribLocation('tangent'))
            m.bindAttrBinormal(shader.getAttribLocation('binormal'))
            m.callDrawArrays()
            pass
            m._vbo.unBind()
        shader.unBind()
        #################
        #scene._models['sphere'].renderNormals()
        
        renderBasis(10.0)
        
        fnt.renderString("Alex Y. Taran presents: 3D Graphics Engine on python (v. 0.1a)",(-0.95,-0.95),(0.0,1.0,0.0,1.0),0.09, float(SCREEN_SIZE[0]) / SCREEN_SIZE[1] )
        fnt.renderString("FPS: "+str(lastFps) , (-0.95,0.9) , (0.0,1.0,0.0,1.0),0.09, float(SCREEN_SIZE[0]) / SCREEN_SIZE[1] )
        # Show the screen
        pygame.display.flip()
    
    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)

#run()
#raw_input()

from Maps.TestSpace import *

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF|FULLSCREEN)
    
    resize(*SCREEN_SIZE)
    init()
    
    space = TestSpace({'screenSize':SCREEN_SIZE})
    space.load()
    
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    pygame.mouse.get_rel() # clean relative movements
    
    clock = pygame.time.Clock()    
    clock.tick()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                return                                        
        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.0
        space.update(time_passed_seconds)
        space.render()
        # Show the screen
        pygame.display.flip()
    
    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)
    del space

main()
#raw_input()
