
import numpy as np
import math, random
from js import THREE, window, document, Object, console
from pyodide.ffi import create_proxy, to_js
from random import uniform
import math




def main():

    #-----------------------------------------------------------------------
    # VISUAL SETUP
    # Declare the variables
    global renderer, scene, camera, controls,composer,console

    #Test THREE.MeshLine

    
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
        "fractal": buttonfunctionfractal1, 
        "fractal1":buttonfunctionfractal2,
        "walkerdesign":buttonfunctionwalker,
        "reset":buttonfunctionresetbutton,
    
        
        #attractorfunctions
        "attractorA": buttonattractorA,
        "attractorB": buttonattractorB,
        "attractorC": buttonattractorC,
        "attractorD":  buttonattractorD,
        
        #triangles
        "triangles":buttonfunction3,
        "finish it!": buttonfunctionfin,
        
        #visibility surface
        "surfacevisible": buttonsceneaddsurface,
        "surfaceunvisible": buttonfunctionremovesrf,

        #walkerstepsizes
        "stepsizea": 1,
        "stepsizeb": 2,

        #attractor2densities
        "densityregionA": 400,
        "numberiterationsfractal":4,
        
        #fractalangles
        "maxiterations":4,

        #fractal1
        "fractalangle":1,
        "branch1":45,
        "numberiterationsfirstfractal": 4,

        #triangle
        "maximumiterationstriangle":3,

        #fielddimensions
        "fieldsize": 40,

        #presentation
        "transparencysurface": 0.05, 
        "transparentlines": 0.3
        

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


    #list
    global surfaces, linesa, visgeometries
   

    visgeometries = []

    surfaces = []


    global iteration_count

    iteration_count = 0


    #variables 
    global transparency, transparentlines, fractalanglefactor, fractalangle1
    global fractal2iterations, transparency
    global densityregionA
    global numberiterationsfirstfractal, maxiterationstriangle

    #numberiterations
    fractalanglefactor = geom_params.fractalangle


    #variables for the fractal1
    fractalangle1 = geom_params.branch1

    numberiterationsfirstfractal = geom_params.numberiterationsfirstfractal

    
    #variables for fractal2
    fractal2iterations = geom_params.maxiterations

    
    #walkersstepsize
    global stepsizewalker, stepsizewalkerB
    
    stepsizewalker = geom_params.stepsizea

    stepsizewalkerB = geom_params.stepsizeb
    


    #attractor2variables
    densityregionA = geom_params.densityregionA


    #iterationstriangle
    maxiterationstriangle = geom_params.maximumiterationstriangle

    #presentation
    transparency = geom_params.transparencysurface

    transparentlines = geom_params.transparentlines

    
 
    global attractor_x, attractor_y, grid_length, grid_width
    attractor_x, attractor_y = 0, 0

    # Define grid size
    grid_length, grid_width = 40, 40


    # Define number of points
    global num_points
    num_points = 60

    # Initialize points

    global points
    points = np.zeros((num_points, 2))

    # Set strength of attraction
    global k
    k = 3



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
    linematerialfinal.linewidht = 0.003

    linematerialfinal.transparent = True
    linematerialfinal.opacity = 0.3
    linematerialfinal.side = 2
    linematerialfinal.alphaToCoverage=True
    linematerialfinal.vertexColors= True


    global new_material

    new_material = THREE.LineMaterial.new()
    new_material.color =  THREE.Color.new(0xff0000 )
    new_material.linewidth= 0.005
    new_material.transparent = True
    new_material.opacity = 0.6
    new_material.vertexColors= True
    new_material.dashed= False
    new_material.alphaToCoverage=True

    #-----------------------------------------------------------------------------------------------
   
    global field_length, field_width

    #fieldimensions
    
    field_length = geom_params.fieldsize
    field_width = geom_params.fieldsize


    global pointsA, pointsB
    global last_point, last_point2, last_point3, last_point4

    
    last_point = np.array([0, 40])
    last_point2= np.array([40, 40])
    last_point3 = np.array([40, 0])
    last_point4 = np.array([0, 0])
    
  
    global walkerA, walkerB
    
    walkerA = (20,20) 
    walkerB = (0,0)
   
    pointsA = [np.array(walkerA)]
    pointsB = [np.array(walkerB)]
    
    basicsurface(transparency)

    guifunction()

    
    # Graphic Post Processing
    global composer
    post_process()

    controls = THREE.OrbitControls.new(camera, renderer.domElement)
    controls.target.set( 20, 0, 20 )
    controls.damping = 0.2
    controls.enablePan = False
    controls.enableDamping = True

    controls.maxDistance = 200


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

    on_dragging_changed_proxy = create_proxy(on_dragging_changed)
    transform_controls.addEventListener( 'dragging-changed', on_dragging_changed_proxy) 

    on_pointer_down_proxy = create_proxy(on_pointer_down)
    #on_pointer_up_proxy = create_proxy(on_pointer_up)
    on_pointer_move_proxy = create_proxy(on_pointer_move)

    on_double_click_proxy = create_proxy(on_double_click)
    document.addEventListener( 'dblclick', on_double_click_proxy )

    document.addEventListener( 'pointerdown', on_pointer_down_proxy )
    #document.addEventListener( 'pointerup', on_pointer_up_proxy )co
    document.addEventListener( 'pointermove', on_pointer_move_proxy )


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

    global pointsA, fractal2iterations

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
            angle = -math.pi/7
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
    global pointsA, pointsB
    threecurrentline = []
    baseshapelines = []


    threecurrentline2 = []
    baseshapelines2 = []


    for id in range(len(pointsA)):
        pairpoints = []
        j = pointsA[id]  
        j = j.tolist()


        j_threevec = THREE.Vector3.new(j[0],0, j[1])
      
        threecurrentline.append(j_threevec)

        if id < len(pointsA)-1:
            pairpoints.append(id)
            pairpoints.append(id+1)

            baseshapelines.append(pairpoints)


    cleaned_baseshapelines = []
    
    for points in baseshapelines:
        
        threee_points = to_js([threecurrentline[points[0]], threecurrentline[points[1]]])

        dist = threee_points[0].distanceTo(threee_points[1])
    
        if dist < 6:
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
      
        if dist < 6:
            cleaned_baseshapelines2.append(points)
    

    baseshapelines2 = cleaned_baseshapelines2




def guifunction():

    global geometry_mesh

    #gui creation
    global folder1, folder2, folder3, folder4, folder5, gui

    gui = window.lil.GUI.new()
    gui.title('CREATE YOUR OWN STRUCTURE !')


    #fractal1

    folder1 = gui.addFolder('1st way - design with fractals')
    folder1.add(geom_params, "numberiterationsfirstfractal",0,5,1).name('lenght of the branch')
    folder1.add(geom_params, 'fractal').name('create fractal !')
    folder1.close()

    #fractal2

    folder2 = gui.addFolder('Fractal2').title('2nd - design a tree')
    folder2.add(geom_params, 'maxiterations', 1, 4, 1).name('lenght of branches')
    folder2.add(geom_params, 'fractal1').name('create a tree !')
    folder2.close()

    
    #walker

    folder3 = gui.addFolder('3rd - let a walker design')
    folder3.add(geom_params, 'stepsizea', 0,5,1).name('step size walker 1')
    folder3.add(geom_params, 'stepsizeb', 0,5,1).name('step size walker 2')
    folder3.add(geom_params, 'walkerdesign').name('create path !')
    folder3.close()


    folder4 = gui.addFolder('5th - zone attractos')
    folder4.add(geom_params, 'attractorA').name('attractorA ')
    folder4.add(geom_params, 'attractorB').name(' attractorB')
    folder4.add(geom_params, 'attractorC').name('attractorC')
    folder4.add(geom_params, 'attractorD').name('attractorD')
    folder4.close()

    #TRIANGLES

    folder5= gui.addFolder('6th - Sierpinski-triangle')
    folder5.add(geom_params, "triangles", 0,5,1).name('create a triangle fractal !')
    folder5.close()

    
    gui.add(geom_params, 'reset')
    
    surfacegui()
        
    gui.close()




def buttonfunctionfractal1():

    global fractalanglefactor, iteration_count, fractalangle1, numberiterationsfirstfractal 

    for geometries in visgeometries:
        scene.remove(geometries)

    visgeometries.clear()

    if fractalanglefactor != geom_params.fractalangle or fractalangle1 != geom_params.branch1 or numberiterationsfirstfractal != geom_params.numberiterationsfirstfractal:

        fractalanglefactor = geom_params.fractalangle

        fractalangle1 = geom_params.branch1

        numberiterationsfirstfractal = geom_params.numberiterationsfirstfractal


        if fractalanglefactor == geom_params.fractalangle and  fractalangle1 == geom_params.branch1:



            generate_l_system_fractal(numberiterationsfirstfractal)

            draw_systemA()

            update_linesa_on_surface(transparentlines)

           

    else:

    
        generate_l_system_fractal(numberiterationsfirstfractal)

        draw_systemA()

        update_linesa_on_surface(transparentlines)

     



def buttonfunctionfractal2():

    global iteration_count, pointsA, fractal2iterations

    iteration_count += 1

    if fractal2iterations != geom_params.maxiterations:
        fractal2iterations = geom_params.maxiterations

        for geometries in visgeometries:
            scene.remove(geometries)


        my_axiom_system = system(0, fractal2iterations, "X")

        firstfractal((my_axiom_system), np.array([0,0,0]), np.array([40,0,0]), np.array([40,40,0]), np.array([0,40,0]))

        draw_systemA()

        update_linesa_on_surface(transparentlines)

    
            
    else:
        

        my_axiom_system = system(0, fractal2iterations, "X")

        firstfractal((my_axiom_system), np.array([0,0,0]), np.array([40,0,0]), np.array([40,40,0]), np.array([0,40,0]))

        draw_systemA()

        update_linesa_on_surface(transparentlines)


      


def buttonfunctionwalker():

    global stepsizewalker, stepsizewalkerB


    for geometries in visgeometries:
        scene.remove(geometries)

    visgeometries.clear()

    visgeometries.clear()

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

    global pointsA, iteration_count, maxiterationstriangle

    iteration_count += 1

    if iteration_count <= 6:

        points = [np.array([0, 0]), np.array([0, 40]), np.array([40, 40]), np.array([40, 0])]
        
        triangle(points, iteration_count)

        triangle2(points, iteration_count)
        
        draw_systemA()

        update_linesa_on_surface(transparentlines)

    else:

        pass
    


def buttonattractorA():

    global pointsA, densityregionA


    attractors = [np.array([0, 0])]
    
    density = [densityregionA]

    last = None
   
    pointsA, last = attractor2(pointsA, last, attractors, density)
    
    draw_systemA()

    update_linesa_on_surface(transparentlines)



def buttonattractorB():

    global  pointsB

    attractors = [np.array([40, 0])]

    density = [densityregionA]

    last = None
   
    pointsB, last = attractor2(pointsB, last, attractors, density)
    
    draw_systemA()

    update_linesa_on_surface(transparentlines)



def buttonattractorC():

    global pointsB

    attractors = [np.array([40, 40])]

    density = [densityregionA]

    last = None
   
    pointsB, last = attractor2(pointsB, last, attractors, density)
    
    draw_systemA()

    update_linesa_on_surface(transparentlines)




def buttonattractorD():

    global pointsB

    attractors = [np.array([0, 40])]

    density = [densityregionA]

    last = None
   
    pointsB, last = attractor2(pointsB, last, attractors, density)
    
    draw_systemA()

    update_linesa_on_surface(transparentlines)



def buttonfunctionremovesrf():

    global geometry_mesh, folder7
  
    scene.remove(geometry_mesh)
    
    geometry_mesh.visible = False
    
    for handles in curve_handles:
        for point in handles:
            point.visible = False

    for curve_line in list_of_curves:
        curve_line.visible = False

    folder7.destroy()
    surfacegui()



def surfacegui():
    global folder7

    folder7 = gui.addFolder('visibility')
   

    if geometry_mesh.visible == False:
        folder7.add(geom_params, 'surfacevisible')
    
    if geometry_mesh.visible == True:
        folder7.add(geom_params, "surfaceunvisible")



def buttonsceneaddsurface():

    global geometry_mesh

    scene.add(geometry_mesh)

    geometry_mesh.visible =True

    for curve_line in list_of_curves:
        curve_line.visible = True

    for handles in curve_handles:
        for point in handles:
            point.visible = True

    folder7.destroy()
    surfacegui()
    



def buttonfunctionresetbutton():

    global pointsA, pointsB, iteration_count

    pointsA.clear()

    pointsB.clear()

    iteration_count = 0

    for geometries in visgeometries:
        scene.remove(geometries)

    geometry_mesh.visible = True

    scene.add(geometry_mesh)


    for handles in curve_handles:
        for handle in handles:
            handle.visible = True
    
    for curve_line in list_of_curves:
        curve_line.visible = True

    transform_controls.visible = True

    folder7.destroy()
    surfacegui()


def buttonfunctionfin():
    global points, folder1, folder2, folder3, folder4, folder5, gui

    geometry_mesh.visible = False

    for handles in curve_handles:
        for handle in handles:
            handle.visible = False

    for curve_line in list_of_curves:
        curve_line.visible = False

    transform_controls.visible = False

    folder7.destroy()

    surfacegui()
   

def on_dragging_changed(event):

    global controls 
    controls.enabled = not event.value

def on_double_click(event):
    global scene, action
    event.preventDefault()
    action = ACTION_NONE
    scene.remove(transform_controls)


def on_pointer_down(event):
    global action, ACTION_SELECT, mouse, window
    action = ACTION_SELECT
    mouse.x = ( event.clientX / window.innerWidth ) * 2 - 1
    mouse.y = - ( event.clientY / window.innerHeight ) * 2 + 1


def on_pointer_move(event):
    global action, ACTION_SELECT, ACTION_NONE, transform_controls, raycaster, mouse, camera, curve_handles, scene
    global target
   
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

    #update fieldattractor-------------------------------------------------------------------------------------------------------------------


    
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

    global threecurrentline, baseshapelines
    global scene, linematerial

    global pointsA


    #updatelinesAonsurface-------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    if len(visgeometries) != 0:
        for l in visgeometries:
            scene.remove(l)

    

    for pairs in baseshapelines:
        curve_pts = []

        for id in pairs:

            j = pointsA[id]
            j = j.tolist()

            j_threevec = THREE.Vector3.new(mapFromTo(j[0], 0, 40,0,1),0,mapFromTo(j[1], 0,40,0,1))

            target = THREE.Vector3.new()
            surface.getPoint( j_threevec.x,  j_threevec.z, target)

            curve_pts.append(target)

       

        
        color = THREE.Color.new()
        POS = []
        COLS = []  

        for points in curve_pts:
            
            POS.extend([points.x, points.y, points.z])
            color.setHSL( 0.4, 0.65, 0.8 )
            COLS.extend([color.r, color.g, color.b])

        
        geometry2 = THREE.LineGeometry.new()
        geometry2.setPositions( to_js(POS) )
        geometry2.setColors(to_js(COLS))
        
       
        line2 = THREE.Line2.new(geometry2, new_material)

        visgeometries.append(line2)
        scene.add(line2)
    
    


    #updatelinesBonsurface-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    
    for pairs in baseshapelines2:
        curve_pts2 = []
        for id in pairs:

            j = pointsB[id]
            j = j.tolist()

            j_threevec = THREE.Vector3.new(mapFromTo(j[0], 0, 40,0,1),0,mapFromTo(j[1], 0,40,0,1))

            target = THREE.Vector3.new()
            surface.getPoint( j_threevec.x,  j_threevec.z, target)

            curve_pts2.append(target)


        color2 = THREE.Color.new()
        POS2 = []
        COLS2 = []  

        for points in curve_pts2:
            
            POS2.extend([points.x, points.y, points.z])
            color2.setHSL( 0.1, 0.7, 0.3 )
            COLS2.extend([color2.r, color2.g, color2.b])

        geometry3 = THREE.LineGeometry.new()
        geometry3.setPositions(to_js(POS2))
        geometry3.setColors(to_js(COLS2))

        line3 = THREE.Line2.new(geometry3, new_material)
        visgeometries.append(line3)

        scene.add(line3)
        
    

def render(*args):

    global list_of_curves, scene

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