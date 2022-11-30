# Import javascript modules
from js import THREE, window, document, Object, console
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math

# Version mit gui slider at CURRENT_ITERATIONS

geom1_params=  {
        "x": 5,
        "angle1":1.5,
        "angle2":3,
        "translation_z":0,
        "moving_z": -2,
        "amountz": 2,
        "amountx": 4      
}

geom1_params = Object.fromEntries(to_js(geom1_params))

#-----------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM
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
    back_color = THREE.Color.new(0.1,0.1,0.1)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(1000, window.innerWidth/window.innerHeight, 0.6, 1000)
    camera.position.z = 10
    camera.position.y = -30
    camera.position.x = 30
    scene.add(camera)

    #colors

    global color1, color2

    color1 =  THREE.Color.new('rgb(600, 127, 64)')
    color2 = THREE.Color.new('rgb(0,0,255)')

    # defintion materials

    global line_material1, line_material2 

    line_material1 = THREE.LineBasicMaterial.new()
    line_material1.color = color2
    line_material1.transparent = True
    line_material1.opacity = 0.6

    line_material2 = THREE.LineBasicMaterial.new()
    line_material2.color = color1
    line_material2.transparent = True
    line_material2.opacity = 0.6

    


    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
    #-----------------------------------------------------------------------
    
    design()

    #update_draw_system((my_axiom_system), THREE.Vector3.new(0,0,0))

    #-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    # Set up GUI
    gui = window.dat.GUI.new()
    param_folder = gui.addFolder('Parameters')
    param_folder.add(geom1_params, 'x', 0,5,1)
    param_folder.add(geom1_params,'angle1', 1,2,0.1)
    param_folder.add(geom1_params, 'angle2', 2,3,0.1)
    param_folder.add(geom1_params, 'translation_z',0,0.06,0.01)
    param_folder.add(geom1_params, 'moving_z', -20, 0, 1)
    param_folder.add(geom1_params, 'amountz', 0, 10, 1)
    
   
    param_folder.open()
    
    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
#-----------------------------------------------------------------------

def design():

    # YOUR DESIGN / GEOMETRY GENERATION
    # Geometry Creation
    global max_iterations, moving_z, amountz
    max_iterations = geom1_params.x
    moving_z = geom1_params.moving_z
    amountz = geom1_params.amountz
   

    my_molecule_system = system(0, max_iterations, "X")   
    for i in range(amountz):
            draw_system((my_molecule_system), THREE.Vector3.new(0,moving_z*i,0))
           

# HELPER FUNCTIONS
# Define RULES in a function which takes one SYMBOL and applies rules generation
def generate(symbol):
    if symbol == "X":
        return "X+X-XX"

    elif symbol == "+":
        return "+"
    elif symbol == "-":
        return "-"

# A recursive fundtion, which taken an AXIOM as an inout and runs the generate function for each symbol

def draw_system(molecule, start_pt):

    global lines, angle1, angle2, translationvector
    translationvector = geom1_params.translation_z
    move_vec = THREE.Vector3.new(1,0,0)
    lines = []

    for symbol in molecule:

        if symbol == "X":
            old = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
            new_pt = THREE.Vector3.new(start_pt.x, start_pt.y, start_pt.z)
            new_pt = new_pt.add(move_vec)
            line = []
            line.append(old)
            line.append(new_pt)
            lines.append(line)
            start_pt = new_pt

        elif symbol == "+":
            angle1 = geom1_params.angle1

            move_vec.applyAxisAngle(THREE.Vector3.new(0,-1,translationvector), math.pi/-(angle1))
        
        elif symbol == "-":

            angle2 = geom1_params.angle2
            move_vec.applyAxisAngle(THREE.Vector3.new(0,-1,0), math.pi/(angle2))

    for points in lines:

        global geom, scene

        line_geom = THREE.BufferGeometry.new()
        points = to_js(points)
        geom = THREE.SphereGeometry.new(0.2,10, 10)
        geom.translate(points[0].x, points[0].y, points[0].z)
        sphere = THREE.Mesh.new(geom)
        
        
        edges = THREE.EdgesGeometry.new(sphere.geometry)
        edgeline = THREE.LineSegments.new(edges, line_material2)
        scene.add(edgeline)

        line_geom.setFromPoints( points ) 
        vis_line = THREE.Line.new( line_geom, line_material1 )       
        scene.add(vis_line)

        
def system(current_iteration, max_iterations, molecule):
    current_iteration += 1
    new_molecule = ""
    for symbol in molecule:
        new_molecule += generate(symbol)
    if current_iteration >= max_iterations:
        return new_molecule
    else:
        return system(current_iteration, max_iterations, new_molecule)


def update_system():
    global max_iterations, moving_z, amountz, scene

    if max_iterations != geom1_params.x or angle1 != geom1_params.angle1 or angle2 != geom1_params.angle2 or translationvector != geom1_params.translation_z or moving_z != geom1_params.moving_z or geom1_params.amountz != amountz:
        scene.clear()
        design()
    

# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    update_system()
    controls.update()
    composer.render()

# Graphical post-processing
def post_process():
    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)

    pixelRatio = window.devicePixelRatio

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * pixelRatio )
   
    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)

# Adjust display when window size changes
def on_window_resize(event):

    event.preventDefault()

    global renderer
    global camera
    
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()

    renderer.setSize( window.innerWidth, window.innerHeight )

    #post processing after resize
    post_process()
#-----------------------------------------------------------------------
#RUN THE MAIN PROGRAM
if __name__=='__main__':
    main()
