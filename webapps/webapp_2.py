# Import javascript modules
from js import THREE, window, document, Object, console
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math

global geom_params   

geom_params = {
    "x": 1,
    "division":0.5
}

geom_params = Object.fromEntries(to_js(geom_params))

# meherere Copien dazumachen
# bessere Auflösung


def main():

    #-----------------------------------------------------------------------
    # VISUAL SETUP
    # Declare the variables
    global renderer, scene, camera, controls,composer
    
    #Set up the renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    # Set up the scene
    scene = THREE.Scene.new()
    back_color = THREE.Color.new()
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(50, window.innerWidth/window.innerHeight, 0.6, 50)
    camera.position.z = 0
    camera.position.y = 1
    camera.position.x = -4

    # Set up lighting
    amb_light = THREE.AmbientLight.new(0xf0f0f0)
    scene.add(amb_light)
    light = THREE.SpotLight.new(0xffffff, 1.5 )
    light.position.set( 0, 1500, 200 )
    light.angle = math.pi * 0.3
    light.castShadow = True
    light.shadow.camera.near = 200
    light.shadow.camera.far = 2000
    light.shadow.bias = - 0.000222
    light.shadow.mapSize.width = 1024
    light.shadow.mapSize.height = 1024
    scene.add( light )

    scene.add(camera)

    global line_material2, meshmaterial

    line_material2 = THREE.LineBasicMaterial.new()
    line_material2.color = THREE.Color.new('rgb(0, 0, 128)')

    meshmaterial = THREE.MeshBasicMaterial.new()
    #meshmaterial.color = THREE.Color.new('rgb(240, 248, 255)')
    meshmaterial.transparent = True
    meshmaterial.opacity = 0.8
    meshmaterial.side = 2

    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy)

    # programming user interface----------------------------------------------------------------------------------------------
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)


    # Set up GUI
    gui = window.lil.GUI.new()
    gui.add( geom_params, 'x', 0,5,1)
    gui.add( geom_params, 'division', 0,1,0.1)

    #gui.add( params, 'tension',0,1).step( 0.01 ).onChange(on_changed(params.tension))
    
    gui.open()
    

    global max_iterations, division
    max_iterations= geom_params.x
    division = geom_params.division

   
    #defintion of the system
    my_element_system = system(0,max_iterations,"X")
    draw_system(my_element_system)
    
    render()

def system(current_iteration, max_iterations ,element):
    current_iteration += 1
    new_element = ""
    for symbol in element:
        new_element += generate(symbol)
    if current_iteration > max_iterations:
        return new_element
    else:
        return system(current_iteration, max_iterations, new_element)

def generate(symbol):
    if symbol == "X":
        return "F[X]"
    elif symbol == "F":
        return "FF"
    elif symbol == "[":
        return "["
    elif symbol == "]":
        return "]"


def draw_system(element):
    #creating basic start_points
    
    geometries = []
    
    start_pt = THREE.Vector3.new(0,0,0)
    move_vec2 = THREE.Vector3.new(0,0,1)
    move_vec3 = THREE.Vector3.new((3**(1/2))/2,0,0.5)
    move_vec4 = THREE.Vector3.new((1/3)*(3**(1/2))/2, 1*((2/3)**(1/2)),0.5)

    start_pt2 = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
    start_pt2.add(move_vec2)
    start_pt3 = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
    start_pt3.add(move_vec3)
    start_pt4 = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
    start_pt4.add(move_vec4)

    start_points = []
    start_points.append(start_pt)
    start_points.append(start_pt2)
    start_points.append(start_pt3)
    start_points.append(start_pt4)

    triangular1 = [start_points[0], start_points[1], start_points[3], start_points[0]]
    triangular2 = [start_points[1], start_points[2], start_points[3], start_points[1]]
    triangular3 = [start_points[2], start_points[0], start_points[3], start_points[3]]

    triangular1 = to_js( triangular1 )
    triangular2 = to_js( triangular2)
    triangular3 = to_js( triangular3)
    
    TRIANUGLAR1 = THREE.BufferGeometry.new().setFromPoints(triangular1)
    TRIANULAR1_MESH = THREE.Line.new(TRIANUGLAR1, line_material2)
    #TRIANGULAR1_SURFACE = THREE.Mesh.new(TRIANUGLAR1, meshmaterial)
    scene.add( TRIANULAR1_MESH)
    #scene.add(TRIANGULAR1_SURFACE)
    geometries.append(TRIANULAR1_MESH)

    TRIANUGLAR2 = TRIANUGLAR1.clone().setFromPoints(triangular2)
    TRIANUGLAR2_MESH = THREE.Line.new(TRIANUGLAR2, line_material2)
    #TRIANGULAR2_SURFACE = THREE.Mesh.new(TRIANUGLAR2, meshmaterial)
    scene.add( TRIANUGLAR2_MESH )
    #scene.add(TRIANGULAR2_SURFACE)
    geometries.append(TRIANUGLAR2_MESH)

    TRIANUGLAR3 = TRIANUGLAR1.clone().setFromPoints(triangular3)
    TRIANUGLAR3_MESH = THREE.Line.new(TRIANUGLAR3, line_material2)
    #TRIANGULAR3_SURFACE = THREE.Mesh.new(TRIANUGLAR3, meshmaterial)

    scene.add( TRIANUGLAR3_MESH )
    #scene.add(TRIANGULAR3_SURFACE)
    geometries.append(TRIANUGLAR3_MESH)

    #basic triangles FACE1

    mid_points=[]

    line0_1= THREE.LineCurve.new(start_points[0],start_points[1])
    midpoint0_1 = THREE.Vector3.new()
    line0_1.getPoint(0.5, midpoint0_1)
    line0_3= THREE.LineCurve.new(start_points[0],start_points[3])
    midpoint0_3 = THREE.Vector3.new()
    line0_3.getPoint(0.5, midpoint0_3)
    line1_2= THREE.LineCurve.new(start_points[1],start_points[2])
    midpoint1_2= THREE.Vector3.new()
    line1_2.getPoint(0.5, midpoint1_2)
    line1_3= THREE.LineCurve.new(start_points[1],start_points[3])
    midpoint1_3 = THREE.Vector3.new()
    line1_3.getPoint(0.5, midpoint1_3)
    line2_0= THREE.LineCurve.new(start_points[2],start_points[0])
    midpoint2_0= THREE.Vector3.new()
    line2_0.getPoint(0.5, midpoint2_0)
    line2_4= THREE.LineCurve.new(start_points[2],start_points[3])
    midpoint2_4 = THREE.Vector3.new()
    line2_4.getPoint(0.5, midpoint2_4)

    mid_points.append(midpoint0_1)   
    mid_points.append(midpoint0_3)   
    mid_points.append(midpoint1_2)   
    mid_points.append(midpoint1_3)   
    mid_points.append(midpoint2_0)   
    mid_points.append(midpoint2_4) 


    FACE1 = []
    FACE1.append(start_points[0])
    FACE1.append(start_points[1])
    FACE1.append(start_points[3])
    FACE1.append(mid_points[0])
    FACE1.append(mid_points[3])
    FACE1.append(mid_points[1])


    face1_middle =[FACE1[3], FACE1[4], FACE1[5], FACE1[3]]
    face1_middle = to_js(face1_middle)
    FACE1_mid = THREE.BufferGeometry.new().setFromPoints(face1_middle)

    FACE1_mid_mesh= THREE.Line.new(FACE1_mid, line_material2)
    scene.add(FACE1_mid_mesh)
    
    geometries.append(FACE1_mid_mesh)

    face1_1_start1 = start_points[0]
    face1_1_start2 = midpoint0_1
    face1_1_start3 = midpoint0_3
    
    face2_1_start1 =  midpoint0_1 
    face2_2_start2 = midpoint1_3
    face2_3_start3 = midpoint0_3
    
    face3_1_start1 = midpoint1_3
    face3_2_start2 = start_points[3]
    face3_3_start3 =  midpoint0_3


    face4_1_start1 = midpoint0_1
    face4_2_start2 = start_points[1]
    face4_3_start3 =  midpoint1_3
    
    for symbol in element:
    
       
        if symbol == "F" or symbol == "X":

            

            face1_1line_points = [face1_1_start1, face1_1_start2, face1_1_start3, face1_1_start1]
            face1_1line_points = to_js(face1_1line_points)

            face1_1line_geom = THREE.BufferGeometry.new()
            face1_1line_geom.setFromPoints(face1_1line_points)
            face1_1line_mesh = THREE.Line.new( face1_1line_geom, line_material2)
            scene.add(face1_1line_mesh)

            geometries.append( face1_1line_mesh)

            face1_1_1 = THREE.LineCurve.new(face1_1_start1, face1_1_start2 )
            face1_1mid = THREE.Vector3.new()
            face1_1_1.getPoint(division, face1_1mid)
            face1_1_2 = THREE.LineCurve.new(face1_1_start2,face1_1_start3 )
            face1_1_2mid = THREE.Vector3.new()
            face1_1_2.getPoint(division,face1_1_2mid)
            face1_1_3 = THREE.LineCurve.new(face1_1_start3,face1_1_start1 )
            face1_1_3mid = THREE.Vector3.new()
            face1_1_3.getPoint(division, face1_1_3mid)
            
            face1_1_start1 = face1_1mid
            face1_1_start2 = face1_1_2mid
            face1_1_start3 = face1_1_3mid

            #face2---------------------------------------------------------------------------------------------------------------------------
            
            face2_1line_points = [face2_1_start1, face2_2_start2, face2_3_start3, face2_1_start1]
            face2_1line_points = to_js(face2_1line_points)

            face2_1line_geom = THREE.BufferGeometry.new()
            face2_1line_geom.setFromPoints(face2_1line_points)
            face2_1line_mesh = THREE.Line.new( face2_1line_geom, line_material2)
            scene.add(face2_1line_mesh)

            geometries.append(face2_1line_mesh)

            face2_1_1 = THREE.LineCurve.new(face2_1_start1, face2_2_start2 )
            face2_1mid = THREE.Vector3.new()
            face2_1_1.getPoint(division, face2_1mid)
            face2_1_2 = THREE.LineCurve.new(face2_2_start2,face2_3_start3 )
            face2_1_2mid = THREE.Vector3.new()
            face2_1_2.getPoint(division,face2_1_2mid)
            face2_1_3 = THREE.LineCurve.new(face2_3_start3,face2_1_start1 )
            face2_1_3mid = THREE.Vector3.new()
            face2_1_3.getPoint(division, face2_1_3mid)

            
            face2_1_start1 = face2_1mid
            face2_2_start2 = face2_1_2mid
            face2_3_start3 = face2_1_3mid


            #face3---------------------------------------------------------------------------------------------------------------------------

            face3_1line_points = [face3_1_start1, face3_2_start2, face3_3_start3, face3_1_start1]
            face3_1line_points = to_js(face3_1line_points)

            face3_1line_geom = THREE.BufferGeometry.new()
            face3_1line_geom.setFromPoints(face3_1line_points)
            face3_1line_mesh = THREE.Line.new( face3_1line_geom, line_material2)
            scene.add(face3_1line_mesh)

            geometries.append(face3_1line_mesh)

            face3_1_1 = THREE.LineCurve.new(face3_1_start1, face3_2_start2 )
            face3_1mid = THREE.Vector3.new()
            face3_1_1.getPoint(division, face3_1mid)
            face3_1_2 = THREE.LineCurve.new(face3_2_start2,face3_3_start3 )
            face3_1_2mid = THREE.Vector3.new()
            face3_1_2.getPoint(division,face3_1_2mid)
            face3_1_3 = THREE.LineCurve.new(face3_3_start3,face3_1_start1 )
            face3_1_3mid = THREE.Vector3.new()
            face3_1_3.getPoint(division, face3_1_3mid)

            
            face3_1_start1 = face3_1mid
            face3_2_start2 = face3_1_2mid
            face3_3_start3 = face3_1_3mid   

            #face4----------------------------------------------------------------------------------------------------------------------------

            face4_1line_points = [face4_1_start1, face4_2_start2, face4_3_start3, face4_1_start1]
            face4_1line_points = to_js(face4_1line_points)

            face4_1line_geom = THREE.BufferGeometry.new()
            face4_1line_geom.setFromPoints(face4_1line_points)
            face4_1line_mesh = THREE.Line.new( face4_1line_geom, line_material2)
            scene.add(face4_1line_mesh)

            geometries.append(face4_1line_mesh)


            face4_1_1 = THREE.LineCurve.new(face4_1_start1, face4_2_start2 )
            face4_1mid = THREE.Vector3.new()
            face4_1_1.getPoint(division, face4_1mid)
            face4_1_2 = THREE.LineCurve.new(face4_2_start2,face4_3_start3 )
            face4_1_2mid = THREE.Vector3.new()
            face4_1_2.getPoint(division,face4_1_2mid)
            face4_1_3 = THREE.LineCurve.new(face4_3_start3,face4_1_start1 )
            face4_1_3mid = THREE.Vector3.new()
            face4_1_3.getPoint(division, face4_1_3mid)

            
            face4_1_start1 = face4_1mid
            face4_2_start2 = face4_1_2mid
            face4_3_start3 = face4_1_3mid   


            #geometries.position.set(THREE.Vector3.new(0,0,1))

            for geometry in geometries:
                
                geometry2 = geometry.clone().translateZ(1)
                scene.add(geometry2)
                console.log(geometry2)

                geometry3 = geometry.clone().translateZ(-1)
                scene.add(geometry3)
   
       

# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    controls.update()
    composer.render()
    update()

def update():

    global max_iterations, scene, division

    if max_iterations != geom_params.x or division != geom_params.division:
    
       scene.clear()
       max_iterations = geom_params.x
       division = geom_params.division

       my_element_system = system(0,max_iterations,"X")
       draw_system(my_element_system)
       

# Graphical post-processing
def post_process():
    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)

    pixelRatio = window.devicePixelRatio

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * 5000*pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * 4000* pixelRatio )
   
    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)

def on_window_resize(event):

    event.preventDefault()

    global renderer
    global camera
    
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()

    renderer.setSize( window.innerWidth, window.innerHeight )

    #post processing after resize
    post_process()

    #RUN THE MAIN PROGRAM
if __name__=='__main__':
    main()
