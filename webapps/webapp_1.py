import typing
import numpy as np
import math, random
from js import THREE, window, document, Object, console
from pyodide.ffi import create_proxy, to_js
from scipy import interpolate
from scipy.interpolate import interp1d
from scipy.interpolate import splrep, splev
import matplotlib.pyplot as plt

import json 
import time
from time import *
import datetime
from typing import Iterator
from datetime import timedelta
from random import uniform





def main():

    #-----------------------------------------------------------------------
    # VISUAL SETUP
    # Declare the variables
    global renderer, scene, camera, controls,composer,console
    
    #Set up the renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    # Set up the scene
    scene = THREE.Scene.new()
    back_color = THREE.Color.new("rgb(160,160,160)")
    scene.background = back_color
    fog_color = THREE.Color.new("rgb(0,0,0)")
    scene.fog = THREE.Fog.new(fog_color, 150,700)
    camera = THREE.PerspectiveCamera.new(50, window.innerWidth/window.innerHeight, 1, 500)
    camera.position.set(-60,80,-60)
    scene.add(camera)

    #Set up Studio Scene
    groundGeo = THREE.PlaneGeometry.new(5000,5000)
    groundMat = THREE.MeshBasicMaterial.new ()
    groundMat.color = THREE.Color.new("rgb(250,250,250)")

    ground = THREE.Mesh.new(groundGeo, groundMat)
    ground.position.y = - 33
    ground.rotation.x = - math.pi / 2
    ground.receiveShadow = True
    scene.add( ground )

    
    #Lighting
    hemiLight = THREE.HemisphereLight.new( 0xffffff, 0x444444 )
    hemiLight.position.set( 0, 100, 0 )
    scene.add( hemiLight )

    dirLight = THREE.DirectionalLight.new( 0xffffff )
    dirLight.position.set( - 0, 40, 50 )
    dirLight.castShadow = True
    dirLight.shadow.camera.top = 50
    dirLight.shadow.camera.bottom = - 25
    dirLight.shadow.camera.left = - 25
    dirLight.shadow.camera.right = 25
    dirLight.shadow.camera.near = 0.1
    dirLight.shadow.camera.far = 200
    dirLight.shadow.mapSize.set( 1024, 1024 )
    scene.add( dirLight )

    global geom_params

    #basic paramteres gui
    
    geom_params=  {
       
        #buttonfunctions

        "fractal": buttonfunction, 
        "fractal1":buttonfunction1,
        "walkerdesign":buttonfunction2,
        "reset":buttonfunctionclear,
        "Attractor": buttonfunction4,
        "Attractor2": buttonfunctionattractor2,
        "triangles":buttonfunction3,
        "finish it!": buttonfunctionfin,
    
        #walkerstepsizes

        "stepsizea": 1,
        "stepsizeb": 2,

        #attractordensities

        "density1": 0.03,
        "density2": 0.06,
        "density3": 0.1,

        #attractor2densities

        "densityregionA": 120,
        "densityregionB": 110,
        "densityregionC": 100,
        "densityregionD": 130,

        "numberiterationsfractal":4,
        
        #fractalangles

        "fractalangle":1,
        "fractal2angle1":6,

        "branch1":45,

        #fielddimensions

        "fieldsize": 40,

        #presentation

        "transparencysurface": 0.05, 
        "transparentlines": 0.3,

    }

    geom_params = Object.fromEntries(to_js(geom_params))

    #surfacedegrees
    global degree1, degree2, knots1, knots2
    degree1 = 4
    degree2 = 4
    knots1 = [0,0,0,0,0,1,1,1,1,1]
    knots1 = to_js(knots1)
    knots2 = [0,0,0,0,0,1,1,1,1,1]
    knots2 = to_js(knots2)

    #gui creation
    global folder1, folder2, folder3, folder4, folder5, folder6, gui

    gui = window.lil.GUI.new()
    gui.title('CREATE YOUR OWN STRUCTURE !')


    #fractal1

    folder1 = gui.addFolder('1st way - design with fractals')
    folder1.add(geom_params, 'fractalangle',0,15,1).name('angle of twigs')
    folder1.add(geom_params, 'branch1',0,50,1).name('angle of the branch')
    folder1.add(geom_params, 'fractal').name('create fractal !')
    folder1.close()

    #fractal2

    folder2 = gui.addFolder('Fractal2').title('2nd - design a tree')
    folder2.add(geom_params, 'fractal2angle1', 6, 8, 1).name('angle of the brachnes')
    folder2.add(geom_params, 'fractal1').name('create a tree !')
    folder2.close()

    
    #walker

    folder3 = gui.addFolder('3rd - let a walker design')
    folder3.add(geom_params, 'stepsizea', 0,5,1).name('step size walker 1')
    folder3.add(geom_params, 'stepsizeb', 0,5,1).name('step size walker 2')
    folder3.add(geom_params, 'walkerdesign').name('create path !')
    folder3.close()


    #attractor1

    folder4 = gui.addFolder('4th - layer attractors')
    folder4.add(geom_params, 'density1', 0, 0.1, 0.01).name('density in middle')
    folder4.add(geom_params, 'density2', 0,0.1,0.01).name('density on edges')
    folder4.add(geom_params, 'density3', 0,0.1, 0.01).name('density in middle')
    folder4.add(geom_params, 'Attractor').name('create from attractors !')
    folder4.close()

    #attractor2

    folder5 = gui.addFolder('5th - zone attractos')
    folder5.add(geom_params, "densityregionA", 0, 150, 10).name('region A')
    folder5.add(geom_params, "densityregionB", 0, 150, 10).name('region B')
    folder5.add(geom_params, "densityregionC", 0, 150, 10).name('region C')
    folder5.add(geom_params, "densityregionD", 0, 150, 10).name('region D')
    folder5.add(geom_params, 'Attractor2').name('create from attractors !')
    folder5.close()

    #TRIANGLES

    folder6 = gui.addFolder('6th - Sierpinski-triangle')
    folder6.add(geom_params, "triangles", 0,10,1).name('create a triangle fractal !')
    folder6.close()

    
    gui.add(geom_params, 'reset')
    gui.add(geom_params, 'finish it!')
    


    gui.close()


    #list
    global vislines, surfaces
   
    vislines= []
  
    surfaces = []

    global iteration_count

    iteration_count = 0


    #variables 
    global transparency, transparentlines, numberiterations, fractalanglefactor, fractalangle1
    global fractal2angle1
    global density1, density2, density3, densityregionA, densityregionB, densityregionC, densityregionD


    #numberiterations
    
    numberiterations = geom_params.numberiterationsfractal

    fractalanglefactor = geom_params.fractalangle


    #variables for the fractal1

    fractalangle1 = geom_params.branch1

    
    #variables for fractal2

    fractal2angle1 = geom_params.fractal2angle1

    
    #walkersstepsize

    global stepsizewalker, stepsizewalkerB
    
    stepsizewalker = geom_params.stepsizea

    stepsizewalkerB = geom_params.stepsizeb
    


    #variables for attractors

    density1 = geom_params.density1

    density2 =  geom_params.density2

    density3 = geom_params.density3


    #attractor2variables

    densityregionA = geom_params.densityregionA

    densityregionB = geom_params.densityregionB

    densityregionC = geom_params.densityregionC

    densityregionD = geom_params.densityregionD


    #presentation
    transparency = geom_params.transparencysurface

    transparentlines = geom_params.transparentlines


    #-----------------------------------------------------------------------------------------------
    #define Colors / Materials

    global meshplane

    meshplane = THREE.MeshPhongMaterial.new()
    meshplane.color = THREE.Color.new("rgb(0,50,100)")
    meshplane.side = 2
    meshplane.transparent = True
    meshplane.opacity = transparency

    #Sphere Color Proporties
    global spheredef
    spheredef = THREE.MeshPhongMaterial.new()
    spheredef.color = THREE.Color.new("rgb(50,50,50)")
    spheredef.side = meshplane.side
    spheredef.transparent = meshplane.transparent
    spheredef.opacity = transparency*2.5


    global linematerial
    linematerial = THREE.LineBasicMaterial.new()
    linematerial.color = THREE.Color.new("rgb(20,20,20)")
    linematerial.transparent = True
    linematerial.opacity = transparency*2.5
    linematerial.side = 2

    global linematerialfinal

    linematerialfinal = THREE.LineBasicMaterial.new()
    linematerialfinal.color = THREE.Color.new("rgb(40,40,40)")
    linematerialfinal.transparent = True
    linematerialfinal.opacity = transparentlines
    linematerialfinal.side = 2


    #-----------------------------------------------------------------------------------------------
   
    global field_length, field_width

    #fieldimensions
    
    field_length = geom_params.fieldsize
    field_width = geom_params.fieldsize


    global pointsA, pointsB, pointsC, pointsD, pointsE
    global last_point, last_point2, last_point3, last_point4

    
    last_point = np.array([0, 40])
    last_point2= np.array([40, 40])
    last_point3 = np.array([40, 0])
    last_point4 = np.array([0, 0])
    
  
    global walkerA, walkerB, walkerC, walkerD, walkerE
    
    walkerA = (20,20) 
    walkerB = (0,0)
    walkerC = (0,40)
    walkerD = (39,39)
    walkerE = (39,0)


    
    pointsA = [np.array(walkerA)]
    pointsB = [np.array(walkerB)]
    pointsC = [np.array(walkerC)]
    pointsD = [np.array(walkerD)]
    pointsE = [np.array(walkerE)]


    
    basicsurface(transparency)
    
    # Graphic Post Processing
    global composer
    post_process()

    controls = THREE.OrbitControls.new(camera, renderer.domElement)
    controls.damping = 0.2

    #chnanginghandles of the surface
    global ACTION_SELECT, ACTION_NONE, action
    ACTION_SELECT = 1
    ACTION_NONE = 0
    action = ACTION_NONE

    gridHelper = THREE.GridHelper.new( 60,60 )

    gridHelper.position.set(20,0,20)
    gridHelper.material.transparent = True
    gridHelper.material.opacity = 0.2
    scene.add(gridHelper)
    

    
    global transform_controls, raycaster

    raycaster = THREE.Raycaster.new()
    transform_controls = THREE.TransformControls.new(camera, renderer.domElement)
    

    #diplay interaction functions

    on_object_changed_proxy = create_proxy(on_object_changed)
    transform_controls.addEventListener( 'objectChange', on_object_changed_proxy)

    #update_linesa_on_surface()
    
    on_dragging_changed_proxy = create_proxy(on_dragging_changed)
    transform_controls.addEventListener( 'dragging-changed', on_dragging_changed_proxy) 

    on_pointer_down_proxy = create_proxy(on_pointer_down)
    #on_pointer_up_proxy = create_proxy(on_pointer_up)
    on_pointer_move_proxy = create_proxy(on_pointer_move)

    document.addEventListener( 'pointerdown', on_pointer_down_proxy )
    #document.addEventListener( 'pointerup', on_pointer_up_proxy )co
    document.addEventListener( 'pointermove', on_pointer_move_proxy )


    #update_linesa_on_surface()

    render()



def basicsurface(transparency):

    global initial_points, curve_handles, mouse, raycaster

    initial_points =[

    [
        THREE.Vector3.new( 0, 0, 0),
        THREE.Vector3.new( 0, 15, 10),
        THREE.Vector3.new( 0, 30, 20),
        THREE.Vector3.new( 0,15, 30 ),
        THREE.Vector3.new(0, 0, 40)
        
    ],     

    [
        THREE.Vector3.new( 10, 15, 0),
        THREE.Vector3.new( 10, 15, 10),
        THREE.Vector3.new( 10, 15, 20 ),
        THREE.Vector3.new( 10, 15, 30 ),
        THREE.Vector3.new(10, 15, 40)
        
    ], 
    [

        THREE.Vector3.new( 20, 30, 0),
        THREE.Vector3.new(  20, 0, 10),
        THREE.Vector3.new( 20, 30, 20 ),
        THREE.Vector3.new( 20, 0, 30 ),
        THREE.Vector3.new(20, 30, 40)
        
    ], 
    [
        THREE.Vector3.new( 30, 15, 0),
        THREE.Vector3.new( 30, 15, 10 ),
        THREE.Vector3.new( 30, 15, 20 ),
        THREE.Vector3.new( 30, 15, 30 ),
        THREE.Vector3.new(30, 15, 40)
        
    ], 
    [
        THREE.Vector3.new( 40, 0,0),
        THREE.Vector3.new( 40,15, 10),
        THREE.Vector3.new( 40, 30, 20 ),
        THREE.Vector3.new( 40, 15, 30 ),
        THREE.Vector3.new(40, 0, 40)
        
    ]
    ]

    
    global surface, geometry_mesh
    initial_points_js = to_js(initial_points)
    surface = THREE.NURBSSurface.new(degree1, degree2, knots1, knots2, initial_points_js)


   #baseparamtericsurface---------------------------------------------------------
    
     
 
    geometry = THREE.ParametricGeometry.new(getPoints, 30,30)
    geometry_mesh = THREE.Mesh.new(geometry, meshplane)
    scene.add(geometry_mesh)

   
    surfaces.append(geometry_mesh)

    

    #define handles of the surface-------------------------------------------------
    global curve_handles, handles
    curve_handles = []
    mouse = THREE.Vector2.new()
    sphere_geometry = THREE.SphereGeometry.new(0.5, 30, 30 )
 
    
    for points in initial_points:
        handles = []
        
        for curve_handle in points:
            
            handle = THREE.Mesh.new( sphere_geometry, spheredef )

            handle.position.copy(curve_handle)

            h = handle.position

            handles.append(handle)
            scene.add(handle)
        
        curve_handles.append(handles)

    #define curves--------------------------------------------------------------------
    
    global curve, curve_line, target, second_target, CURVE_SEGMENTS

    global list_of_curves
    list_of_curves = []
    target = None
    second_target = None
    
    CURVE_SEGMENTS = 50

    for points in initial_points:
        curve = THREE.CatmullRomCurve3.new(to_js(points))
        curve.curveType = 'catmullrom'
        points = curve.getPoints( CURVE_SEGMENTS )


        geometry_curve = THREE.BufferGeometry.new()
        geometry_curve.setFromPoints(points)
        curve_line = THREE.Line.new(geometry_curve, linematerial)
        list_of_curves.append(curve_line)
        scene.add(curve_line)  


def mapFromTo(x,a,b,c,d):
    y = (x-a)/(b-a)*(d-c)+c
    return y

def get_time():
    return datetime.datetime.now()


def getPoints(u,v,t):
    global surface
    point = THREE.Vector4.new()
    point = surface.getPoint(u,v,t)
    point = (point)
    return surface.getPoint(u,v,t)


    
def attractor2(points, last, attractors, density):

    if last is None:
        last = attractors.copy()
    
    for i in range(len(attractors)):
        x, y = last[i]
        for j in range(density[i]):
            # Using NumPy's random library
            move_vec = np.random.uniform(-1, 1, size=(2,))
            move_vec /= np.linalg.norm(move_vec)
            x += move_vec[0]
            y += move_vec[1]
            if x >= 1 and x <= 39 and y >= 1 and y <= 39:
                pointsA.append(np.array([x, y]))
                last[i] = np.array([x, y])
                
    return points, last



def attractor1(length, width, density_factors, scales, attractor_points, max_iterations=1):

    global pointsA
    attractor = np.array([length/2, width/2])
    iteration = 0

    while iteration < max_iterations:
        for i in range(len(density_factors)):
            attractor = attractor_points[i] if iteration == 0 else new_points[-1]
            scale = scales[i]
            density_factor = density_factors[i]
            new_points = [np.array(p) for p in np.random.normal(loc=attractor, scale=scale, size=(int(length*width*density_factor), 2))]
            pointsA += new_points

            for point in new_points:
                point[0] = min(max(point[0], 0), length)
                point[1] = min(max(point[1], 0), width)
        
        iteration += 1

  

def basicWalkerA(startingpoint = (20,20), starting_pointsB = (25,25)):

    global stepsizewalker, stepsizewalkerB, pointsB

    
    if not pointsA:
        walkerA = startingpoint
        pointsA.append(np.array(walkerA))
    else:
        walkerA = pointsA[-1]

    
    if not pointsB:
        walkerB = starting_pointsB
        pointsB.append(np.array(walkerB))
    else:
        walkerB = pointsB[-1]

   
    num_steps = 20


    for i in range(num_steps):

        direction = random.randint(0, 3)
    
        if direction == 0:
            walkerA = (pointsA[-1][0], pointsA[-1][1] - stepsizewalker) 
        elif direction == 1:
            walkerA = (pointsA[-1][0] + stepsizewalker, pointsA[-1][1]) 

        elif direction == 2:
            walkerA= (pointsA[-1][0], pointsA[-1][1] + stepsizewalker)  
        else:
            walkerA = (pointsA[-1][0] - stepsizewalker, pointsA[-1][1])  

        if any(np.array_equal(np.array(pos),np.array(walkerA)) for pos in pointsB):
            walkerA = pointsA[-1]
           
        
        
        if walkerA[0] < 0 or walkerA[0] >= field_length or walkerA[1] < 0 or walkerA[1] >= field_width:
            
            walkerA= (random.randint(0, field_length), random.randint(0, field_width))
            
        pointsA.append(np.array(walkerA))



        direction = random.randint(0, 3)

        if direction == 0:
            walkerB = (pointsB[-1][0], pointsB[-1][1] - stepsizewalkerB) 
        elif direction == 1:
            walkerB = (pointsB[-1][0] + stepsizewalkerB, pointsB[-1][1])  
        elif direction == 2:
            walkerB = (pointsB[-1][0], pointsB[-1][1] + stepsizewalkerB) 
        else:
            walkerB = (pointsB[-1][0] - stepsizewalkerB, pointsB[-1][1])  
        
        if walkerB[0] < 0 or walkerB[0] >= field_length or walkerB[1] < 0 or walkerB[1] >= field_width:
           
            walkerB = (random.randint(0, field_length), random.randint(0, field_width))


        pointsB.append(np.array(walkerB))




def generate(symbol):
    if symbol == "X":
        return "F[+X]F[-X]+X"
    elif symbol == "F":
        return "FF"
    elif symbol == "+":
        return "+"
    elif symbol == "-":
        return "-"
    elif symbol == "[":
        return "["
    elif symbol == "]":
        return "]"
    

def system(current_iteration, max_iterations, axiom):

    current_iteration += 1
    new_axiom = ""
    for symbol in axiom:
        new_axiom += generate(symbol)
    if current_iteration >= max_iterations:
        return new_axiom
    else:
        return system(current_iteration, max_iterations, new_axiom)
    

def triangle(points,iterations):

    global pointsA
    
    for i in range(iterations):
        new_points = []
        for point in points:

            new_points.append(point + np.array([40, 0]) / 2**(i+1))
            new_points.append(point + np.array([0, 40]) / 2**(i+1))
            new_points.append(point + np.array([40, 40]) / 2**(i+1))

        points = new_points
    for point in points:
        if point[0] < 0 or point[0] > field_length or point[1] < 0 or point[1] > field_width:
            continue
        pointsA.append(point)



def triangle2(points, iterations):

    global pointsA

    for i in range(iterations):
        new_points = []
        for point in points:

            new_points.append(point + np.array([40, 0]) / 2**(i+1))
            new_points.append(point + np.array([0, 40]) / 2**(i+1))
            new_points.append(point + np.array([0, 0]) / 2**(i+1))

        points = new_points
    for point in points:
        if point[0] < 0 or point[0] > field_length or point[1] < 0 or point[1] > field_width:
            continue
        pointsA.append(point)

 

def firstfractal(axiom, start_pt, start_pt2, start_pt3, start_pt4):

    global pointsA, fractal2angle1

    move_vec = np.array([1,1,1])
    move_vec2 = np.array([-1,1,-1])
    move_vec3 = np.array([-1,-1,-1])
    move_vec4 = np.array([1, -1, 1])

    old_states = []
    old_states2 = []
    old_states3 = []
    old_states4 = []

    old_move_vecs = []
    old_move_vecs2 = []
    old_move_vecs3 = []
    old_move_vecs4 = []
    

    for symbol in axiom:
        if symbol == "F" or symbol == "X":
            old = np.array(start_pt)
            new_pt = np.array(start_pt)

            old2 = np.array(start_pt2)
            new_pt2 = np.array(start_pt2)

            old3 = np.array(start_pt3)
            new_pt3 = np.array(start_pt3)

            old4 = np.array(start_pt4)
            new_pt4 = np.array(start_pt4)


            new_pt = new_pt + move_vec
            new_pt2 = new_pt2 + move_vec2
            new_pt3 = new_pt3 + move_vec3
            new_pt4 = new_pt4 + move_vec4
            line = []


            console.log(to_js(old3))
            
            pointsA.append(old)
            pointsA.append(new_pt)

            pointsA.append(old2)
            pointsA.append(new_pt2)

            pointsA.append(old3)
            pointsA.append(new_pt3)

            pointsA.append(old4)
            pointsA.append(new_pt4)

        
            start_pt = new_pt
            start_pt2 = new_pt2
            start_pt3 = new_pt3
            start_pt4 = new_pt4


        elif symbol == "+": 
            angle = math.pi/7
            c, s = np.cos(angle), np.sin(angle)
            R = np.array(((c, -s, 0), (s, c, 0), (0, 0, 1)))
            move_vec = np.dot(R, move_vec)
            move_vec2 = np.dot(R, move_vec2)
            move_vec3 = np.dot(R, move_vec3)
            move_vec4 = np.dot(R, move_vec4)
            
        
        elif symbol == "-":
            angle = -math.pi/fractal2angle1
            c, s = np.cos(angle), np.sin(angle)
            R = np.array(((c, -s, 0), (s, c, 0), (0, 0, 1)))
            move_vec = np.dot(R, move_vec)
            move_vec2 = np.dot(R, move_vec2)
            move_vec3 = np.dot(R, move_vec3)
            move_vec4 = np.dot(R, move_vec4)



        elif symbol == "[":
            old_state = np.array(start_pt)
            old_state2 = np.array(start_pt2)
            old_state3 = np.array(start_pt3)
            old_state4 = np.array(start_pt4)



            old_move_vec = np.array(move_vec)
            old_move_vec2 = np.array(move_vec2)
            old_move_vec3 = np.array(move_vec3)
            old_move_vec4 = np.array(move_vec4)



            old_states.append(old_state)
            old_states2.append(old_state2)
            old_states3.append(old_state3)
            old_states4.append(old_state4)


            old_move_vecs.append(old_move_vec)
            old_move_vecs2.append(old_move_vec2)
            old_move_vecs3.append(old_move_vec3)
            old_move_vecs4.append(old_move_vec4)


        elif symbol == "]":
            start_pt = np.array(old_states[-1])
            start_pt2 = np.array(old_states2[-1])
            start_pt3 = np.array(old_states3[-1])
            start_pt4 = np.array(old_states4[-1])

            move_vec = np.array(old_move_vecs[-1])
            move_vec2 = np.array(old_move_vecs2[-1])
            move_vec3 = np.array(old_move_vecs3[-1])
            move_vec4 = np.array(old_move_vecs4[-1])
            
            old_states.pop(-1)
            old_states2.pop(-1)
            old_states3.pop(-1)
            old_states4.pop(-1)

            old_move_vecs.pop(-1)
            old_move_vecs2.pop(-1)
            old_move_vecs3.pop(-1)
            old_move_vecs4.pop(-1)



def generate_l_system_fractal(iterations):


    global last_point, last_point2, last_point3, last_point4, fractalangle1

    global pointsA
    point_stack = []
    angle_stack = []

   
    rules = {"F": "F[+F]F[-F]F", "B": "F[+B]F[-B]F", "C":"F[+C]F[-C]F" }
   
   
    axiom = "FBC"

    l_system = axiom
    for i in range(iterations):
        new_string = ""
        for char in l_system:
            if char in rules:
                new_string += rules[char]
            else:
                new_string += char
        l_system = new_string

   
    points = [last_point, last_point2, last_point3, last_point4]
    angles = [275+ fractalangle1, 165+fractalangle1, 105+fractalangle1, -10 + fractalangle1]

  
    step = 1
    angle_change = 30* fractalanglefactor

   
    for i in range(4):
        point = points[i]
        angle = angles[i]
        for char in l_system:
            if char == "F":
                
                point = point + np.array([np.cos(np.deg2rad(angle)), np.sin(np.deg2rad(angle))]) * step
                if point[0] < 0 or point[0] > 40 or point[1] < 0 or point[1] > 40:
                    continue
                pointsA.append(np.array([point[0], point[1]]))

            elif char == "B":
          
                point = point + np.array([np.cos(np.deg2rad(angle)), np.sin(np.deg2rad(angle))]) * step
                if point[0] < 0 or point[0] > 40 or point[1] < 0 or point[1] > 40:
                    continue
                pointsA.append(np.array([point[0], point[1]]))

            elif char == "C":
           
                point = point + np.array([np.cos(np.deg2rad(angle)), np.sin(np.deg2rad(angle))]) * step
                if point[0] < 0 or point[0] > 40 or point[1] < 0 or point[1] > 40:
                    continue

                
                pointsA.append(np.array([point[0], point[1]]))
            
            elif char == "+":
                
                angle += angle_change
            elif char == "-":
               
                angle -= angle_change
            elif char == "[":
                
                point_stack.append(point)
                angle_stack.append(angle)
            elif char == "]":
                
                point = point_stack.pop()
                angle = angle_stack.pop()



        last_point,last_point2, last_point3, last_point4 = points
                



def draw_systemA():

    #cleanded lines pointsA----------------------------------------------------------------------------------------------------------------------------------------------------------

    global threecurrentline, baseshapelines, threecurrentline2, baseshapelines2
    global pointsA, pointsB, pointsC, pointsD, pointsE
    threecurrentline = []
    baseshapelines = []


    threecurrentline2 = []
    baseshapelines2 = []


    for id in range(len(pointsA)):
        pairpoints = []
        j = pointsA[id]  
        j = j.tolist()


        j_threevec = THREE.Vector3.new(j[0],0,  j[1])
        console.log(j_threevec)

        
        threecurrentline.append(j_threevec)
        if id < len(pointsA)-1:
            pairpoints.append(id)
            pairpoints.append(id+1)

            baseshapelines.append(pairpoints)



    cleaned_baseshapelines = []
    
    for points in baseshapelines:
        
        threee_points = to_js([threecurrentline[points[0]], threecurrentline[points[1]]])

        dist = threee_points[0].distanceTo(threee_points[1])
    
        if dist < 3:
            cleaned_baseshapelines.append(points)
    

    baseshapelines = cleaned_baseshapelines

    
    
    #cleanded lines pointsB----------------------------------------------------------------------------------------------------------------------------------------------------------

    for id in range(len(pointsB)):
        pairpoints = []
        j = pointsB[id]  
        j = j.tolist()

        j_threevec = THREE.Vector3.new(j[0],0,  j[1])
        
        
        threecurrentline2.append(j_threevec)
        if id < len(pointsB)-1:
            pairpoints.append(id)
            pairpoints.append(id+1)

            baseshapelines2.append(pairpoints)



    cleaned_baseshapelines2 = []
    
    for points in baseshapelines2:
        
        threee_points = to_js([threecurrentline2[points[0]], threecurrentline2[points[1]]])

        dist = threee_points[0].distanceTo(threee_points[1])
      
        if dist < 3:
            cleaned_baseshapelines2.append(points)
    

    baseshapelines2 = cleaned_baseshapelines2




#buttonfunctionsinterface

def buttonfunction():

    global fractalanglefactor, iteration_count, fractalangle1

    for lines in vislines:
        scene.remove(lines)

    vislines.clear()

    if fractalanglefactor != geom_params.fractalangle or fractalangle1 != geom_params.branch1:

        fractalanglefactor = geom_params.fractalangle

        fractalangle1 = geom_params.branch1

        iteration_count = 0

        if fractalanglefactor == geom_params.fractalangle and  fractalangle1 == geom_params.branch1:

           
            iteration_count += 1

            if iteration_count <= 5:

                generate_l_system_fractal(iteration_count)

                draw_systemA()

                update_linesa_on_surface(transparentlines)

            else:

                pass

    else:

        iteration_count += 1

        if iteration_count <= 5:

            generate_l_system_fractal(iteration_count)

            draw_systemA()

            update_linesa_on_surface(transparentlines)

        else:
            pass




def buttonfunction1():

    global iteration_count, pointsA

    iteration_count += 1

    if fractal2angle1 != geom_params.fractal2angle1:
        fractal2angle1 != geom_params.fractal2angle1

        iteration_count = 0

        if iteration_count <= 4:

            my_axiom_system = system(0, iteration_count, "X")

            firstfractal((my_axiom_system), np.array([0,0,0]), np.array([40,0,0]), np.array([40,40,0]), np.array([0,40,0]))

            draw_systemA()

            update_linesa_on_surface(transparentlines)

        else:
            pass

            
    else:
        
        if iteration_count <= 4:

            my_axiom_system = system(0, iteration_count, "X")

            firstfractal((my_axiom_system), np.array([0,0,0]), np.array([40,0,0]), np.array([40,40,0]), np.array([0,40,0]))

            draw_systemA()

            update_linesa_on_surface(transparentlines)

        else:
            pass

      


def buttonfunction2():

    global stepsizewalker, stepsizewalkerB


    for lines in vislines:
        scene.remove(lines)

    vislines.clear()



    if  stepsizewalker != geom_params.stepsizea or stepsizewalkerB != geom_params.stepsizeb:

        stepsizewalker = geom_params.stepsizea

        stepsizewalkerB = geom_params.stepsizeb

        basicWalkerA(startingpoint = (20,20), starting_pointsB = (25,25))
        
        draw_systemA()

        update_linesa_on_surface(transparentlines)

   
   
    else:

        basicWalkerA(startingpoint = (20,20), starting_pointsB = (25,25))

        draw_systemA()

        update_linesa_on_surface(transparentlines)



def buttonfunction3():

    global pointsA, iteration_count

    iteration_count += 1

    if iteration_count <= 6:

        points = [np.array([0, 0]), np.array([0, 40]), np.array([40, 40]), np.array([40, 0])]
        
        triangle(points, iteration_count)

        triangle2(points, iteration_count)
        
        draw_systemA()

        update_linesa_on_surface(transparentlines)

    else:

        pass
    


def buttonfunction4():

    global density1, density2, density3, pointsA, field_length, field_width

    for visline in vislines:
        scene.remove(visline)

    vislines.clear()

    attractors = [
    np.array([field_length/2, field_width/2]),
    np.array([0,0]),
    np.array([0,40]),
    np.array([40,40]),
    np.array([40,0]),
    np.array([10,10]),
    np.array([10,30]),
    np.array([30,30]),
    np.array([30,10]),]

    
    
    scales = [10,8, 8,8, 8, 10, 10, 10, 10]
    densities = [density1, density2, density2, density2, density2, density3, density3, density3, density3]
   


    if density1 != geom_params.density1 or density2 != geom_params.density2 or density3 != geom_params.density3:

        density1 = geom_params.density1

        density2 = geom_params.density2

        density3 = geom_params.density3

        attractor1(field_length, field_width, densities, scales, attractors, max_iterations=2)

        

        draw_systemA()

        update_linesa_on_surface(transparentlines)

  
    else:
        

        attractor1(field_length, field_width, densities, scales, attractors, max_iterations=2)
        
        draw_systemA()

        update_linesa_on_surface(transparentlines)



def buttonfunctionattractor2():

    global pointsA, densityregionA, densityregionB, densityregionC, densityregionD


    attractors = [np.array([0, 0]), np.array([0, 40]), np.array([40, 40]), np.array([40, 0]),
                  
              np.array([10, 10]), np.array([10, 30]), np.array([30, 30]), np.array([30, 10]),
              
              np.array([20, 0]), np.array([40, 20]), np.array([20, 40]), np.array([0,20]),

              np.array([20, 20])]
    
   

    density = [densityregionA, densityregionA, densityregionA, densityregionA, densityregionB, densityregionB, densityregionB, densityregionB, densityregionD, densityregionD, densityregionD, densityregionD,densityregionC]
    
    last = None
   
    pointsA, last = attractor2(pointsA, last, attractors, density)
    
    draw_systemA()

    update_linesa_on_surface(transparentlines)




def buttontransparencysurface():

    for surface in surfaces:
            scene.remove(surface)

    for handles in curve_handles:
        for point in handles:
            scene.remove(point)


def buttonsceneaddsurface():

    for surface in surfaces:
            scene.add(surface)

    for handles in curve_handles:
        for point in handles:
            scene.add(point)


def buttonfunctionclear():

    global pointsA, pointsB, vislines, iteration_count

    pointsA.clear()

    pointsB.clear()

    iteration_count = 0

    for visline in vislines:
        scene.remove(visline)

    scene.add(geometry_mesh)

    for handles in curve_handles:
        for handle in handles:
            handle.visible = True
    
    for curve_line in list_of_curves:
        curve_line.visible = True

    transform_controls.visible = True

def buttonfunctionfin():
    global points, folder1, folder2, folder3, folder4, folder5, folder6, gui

    scene.remove(geometry_mesh)
    for handles in curve_handles:
        for handle in handles:
            handle.visible = False

    for curve_line in list_of_curves:
        curve_line.visible = False

    transform_controls.visible = False

    folder1.close()
    folder2.close()
    folder3.close()
    folder4.close()
    folder5.close()
    folder6.close()
    gui.close()
    


def on_dragging_changed(event):

    global controls 
    controls.enabled = not event.value


def on_pointer_down(event):
    global action, ACTION_SELECT, mouse, window
    action = ACTION_SELECT
    mouse.x = ( event.clientX / window.innerWidth ) * 2 - 1
    mouse.y = - ( event.clientY / window.innerHeight ) * 2 + 1


def on_pointer_move(event):
    global action, ACTION_SELECT, ACTION_NONE, transform_controls, raycaster, mouse, camera, curve_handles, scene
    global target
    global sphere_A_Mesh

    t1 = get_time()

    event.preventDefault()
    if action == ACTION_SELECT:
        raycaster.setFromCamera( mouse, camera )
        action = ACTION_NONE
        flat_handles =[]
        for handles in curve_handles:
            for h in handles:
                flat_handles.append(h)
        intersects = raycaster.intersectObjects( to_js(flat_handles), False )
        
        if len(intersects) != 0:
            target = intersects[ 0 ].object
            transform_controls.attach( target )

            id_a = None
            id_b = None

            for handles in curve_handles:
                if target in handles:
                    id_a = curve_handles.index(handles)
                    id_b = handles.index(target)

            curve_handles[id_a][id_b] = target

            scene.add( transform_controls )

            t2 = get_time()
            timestep = timedelta.total_seconds(t2-t1)
           

def on_object_changed(event):

    # handles---------------------------------------------------------------------------------------------------------------
    global target, curve, curve_line, curve_handles, CURVE_SEGMENTS
    global list_of_curves, linematerial, console
    id_a = None
    id_b = None

    

    for handles in curve_handles:
        if target in handles:
            id_a = curve_handles.index(handles)
            id_b = handles.index(target)


    curve_handles[id_a][id_b].position.copy(target.position)

    handles = curve_handles[id_a]

    #curve-------------------------------------------------------------------------------------------------------------------

    points = [h.position for h in handles]

    curve = THREE.CatmullRomCurve3.new(to_js(points))
    curve.curveType = 'catmullrom'
    c_points = curve.getPoints( CURVE_SEGMENTS )

    list_of_curves[id_a].geometry.setFromPoints(c_points)

    global new_srf_points
    new_srf_points = []

    for handles in curve_handles:
        new_points = [h.position for h in handles]

        new_srf_points.append(new_points)

  
    new_srf_points = to_js(new_srf_points)


    #surface---------------------------------------------------------------------------------------------------------------------
    
    updatesurface(transparency)

    #lineupdate----------------------------------------------------------------------------------------------------------------------
   
    update_linesa_on_surface(transparentlines)

  
    
def updatesurface(transparency ):

    global geometry_mesh, surface


    surface2 = THREE.NURBSSurface.new(degree1, degree2, knots1, knots2, new_srf_points)
    surface = surface2
    geometry2 = THREE.ParametricGeometry.new(getPoints, 30,30)

    
    new_geometry_mesh = THREE.Mesh.new(geometry2, meshplane)
    scene.remove(geometry_mesh)
    geometry_mesh = new_geometry_mesh
    surfaces.append(geometry_mesh)
    scene.add(geometry_mesh)

    

def update_linesa_on_surface(transparentlines):

    global vislines
    global threecurrentline, baseshapelines
    global scene, linematerial

    global pointsA


    #updatelinesAonsurface-------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    if len(vislines) != 0:
        for l in vislines:
            scene.remove(l)

        

    for pairs in baseshapelines:
        curve_pts = []
        for id in pairs:

            #console.log(id)

            j = pointsA[id]
            j = j.tolist()

            j_threevec = THREE.Vector3.new(mapFromTo(j[0], 0, 40,0,1),0,mapFromTo(j[1], 0,40,0,1))

            target = THREE.Vector3.new()
            surface.getPoint( j_threevec.x,  j_threevec.z, target)

            curve_pts.append(target)


        buffer = THREE.BufferGeometry.new()
        #console.log(buffer)
        buffer.setFromPoints(to_js(curve_pts))
        buffermesh = THREE.Line.new(buffer, linematerialfinal)
        vislines.append(buffermesh)
        scene.add(buffermesh)  


    #updatelinesBonsurface-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    
    for pairs in baseshapelines2:
        curve_pts2 = []
        for id in pairs:

            #console.log(id)

            j = pointsB[id]
            j = j.tolist()

            j_threevec = THREE.Vector3.new(mapFromTo(j[0], 0, 40,0,1),0,mapFromTo(j[1], 0,40,0,1))

            target = THREE.Vector3.new()
            surface.getPoint( j_threevec.x,  j_threevec.z, target)

            curve_pts2.append(target)


        buffer = THREE.BufferGeometry.new()
        #console.log(buffer)
        buffer.setFromPoints(to_js(curve_pts2))
        buffermesh = THREE.Line.new(buffer, linematerialfinal)
        vislines.append(buffermesh)
        scene.add(buffermesh) 




def update():

    global  transparency, translatey, translatex, field_length, field_width, transparentlines, density1, density2, density3
        
    
    if transparency != geom_params.transparencysurface:
        
        for surface in surfaces:
            scene.remove(surface)

        for handles in curve_handles:
            for point in handles:
                scene.remove(point)

        transparency = geom_params.transparencysurface
        #basicsurface(transparency)
        update_linesa_on_surface(transparentlines)
    

    
    if transparentlines != geom_params.transparentlines:

        for lines in vislines:
            scene.remove(lines)

        transparentlines = geom_params.transparentlines

        update_linesa_on_surface(transparentlines)



    

def render(*args):

    global list_of_curves, scene


    update()


    for c in  list_of_curves:
        scene.add(c)

    
    window.requestAnimationFrame(create_proxy(render))
    controls.update()
    composer.render()

    


# Graphical post-processing
def post_process():
    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)

    pixelRatio = window.devicePixelRatio

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth* 1000* pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight *1000* pixelRatio )

    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)


#adjust display size change window

def on_window_resize(event):

    event.preventDefault()

    global renderer
    global camera
    
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()

    renderer.setSize( window.innerWidth, window.innerHeight )

    #post processing after resize
    post_process()

if __name__=='__main__':
    main()
