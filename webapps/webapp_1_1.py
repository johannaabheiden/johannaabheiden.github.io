# Import javascript modules
from js import THREE, window, document, Object, console
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math


global geom1_params, rings, ring_lines
rings = []
ring_lines = []
lines = []

geom1_params = {

        "x":10,
        "y":10,
        "s":10,
        "rotation1":160,
        "rotation2":-160,
        "distance":5
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
    camera = THREE.PerspectiveCamera.new(100, window.innerWidth/window.innerHeight, 0.1, 500)
    camera.position.z = 400
    camera.position.x = 100
    camera.position.y = 300

    scene.add(camera)


    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
    #-----------------------------------------------------------------------
  
    # Geometry Creation
    generate_ring()

     #-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    # Set up GUI
    gui = window.dat.GUI.new()
    param_folder = gui.addFolder('Parameters')
    
    param_folder.add(geom1_params, 'x', 0,50,1)
    param_folder.add(geom1_params, 'y', 0,50,1)
    param_folder.add(geom1_params, 'rotation1', 0,200,1)
    param_folder.add(geom1_params, 'distance', 0,20,1)
   
    param_folder.open()

    global material, line_material
    
    material = THREE.MeshBasicMaterial.new()
    material.transparency = True
    material.opactity =0.2
    material.color = THREE.Color.new("rgb(80%, 50%, 50%)")

    line_material = THREE.LineBasicMaterial.new()
    line_material.color = THREE.Color.new("rgb(80%, 50%, 50%)")
    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
   
    #material.color = color

   
   
def generate_ring(): 

    global rotation1, rotation2, distance

    rotation1 = geom1_params.rotation1
    rotation2 = geom1_params.rotation2
    distance = geom1_params.distance

   
    lines = []


    for i in range(geom1_params.x):
      
        geom = THREE.RingGeometry.new(5,2.5,100)
        geom.translate(distance*i, distance *i,(distance)*i/geom1_params.x)   
        geom.rotateY(math.radians(rotation1)/geom1_params.x*i)

        geom3 = THREE.BufferGeometry.new()
        geom3.copy(geom)
        geom3.translate(-1*distance*i, -1*distance *i,-1*(distance)*i/geom1_params.x) 
        geom3.rotateY(math.radians(rotation1)/geom1_params.x*i) 

        
        for j in range(geom1_params.y):

            geom2 = THREE.BufferGeometry.new()
            geom2.copy(geom)
            geom2.translate(distance*i, distance*i*j,(distance)*j*i/geom1_params.x) 
            geom2.rotateY(math.radians(rotation1)/geom1_params.x*i*j)

            geom4 = THREE.BufferGeometry.new()
            geom4.copy(geom3)
            geom4.translate(-1*distance*i, -1*distance *i*j,-1*(distance)*j*i/geom1_params.x) 
            geom4.rotateY(math.radians(rotation1)/geom1_params.x*i*j)
            

            material = THREE.MeshBasicMaterial.new()
            material.transparency = True
            material.opactity =0.2
           
            
          

            line_material = THREE.LineBasicMaterial.new()
           

            ring = THREE.Mesh.new(geom, material)
            ring2 = THREE.Mesh.new(geom2, material)
            ring3 = THREE.Mesh.new(geom3, material)
            ring4 = THREE.Mesh.new(geom4, material)
           
            

            """console.log(pos)"""
            group = THREE.Group.new(ring, ring2, ring3, ring4)
            scene.add(group)
            rings.append(group)

            edges = THREE.EdgesGeometry.new( ring.geometry )
            line = THREE.LineSegments.new( edges, line_material)
            ring_lines.append(line)
            scene.add( line )

            edges = THREE.EdgesGeometry.new( ring2.geometry )
            line = THREE.LineSegments.new( edges, line_material)
            ring_lines.append(line)
            scene.add( line )

            edges = THREE.EdgesGeometry.new( ring3.geometry )
            line = THREE.LineSegments.new( edges, line_material)
            ring_lines.append(line)
            scene.add( line )

            edges = THREE.EdgesGeometry.new( ring4.geometry )
            line = THREE.LineSegments.new( edges, line_material)
            ring_lines.append(line)
            scene.add( line )


    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS
# Update rings
def update_rings():
    global rings, ring_lines, material, line_material, vis_line, lines
    if len(rings) != 0:
        
        if len(rings) != geom1_params.x * geom1_params.y or geom1_params.rotation1 != rotation1 or geom1_params.rotation2 != rotation2 or geom1_params.distance !=distance :
            for group in rings: scene.remove(group)
            for line in ring_lines: scene.remove(line)
            
            rings = []
            ring_lines = []
            #lines = []
            
            generate_ring()
            
                    

# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    update_rings()
    controls.update()
    #renderer.render(scene, camera)
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
