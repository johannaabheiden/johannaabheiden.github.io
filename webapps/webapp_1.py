# Import javascript modules
from js import THREE, window, document, Object
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math

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
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 1000)
    camera.position.z = 50
    scene.add(camera)


    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
    #-----------------------------------------------------------------------
  
    # Geometry Creation
    global geom1_params, rings, ring_lines
    rings = []
    ring_lines = []
    
    geom1_params = {
            "size":5,
            "y":-50, 
            "x":50,
            "rotation":160,
            "innerRadius":0.5,
            "outerRadius":1.0,
            "thetaSegments":100,
            "z": -0.04
    }

   
    geom1_params = Object.fromEntries(to_js(geom1_params))

    global material, line_material
    color = THREE.Color.new(255,255,255)
    material = THREE.MeshBasicMaterial.new()
   
    #material.color = color

    line_material = THREE.LineBasicMaterial.new()
    line_material.color = THREE.Color.new("rgb(80%, 50%, 50%)")


    for i in range(geom1_params.y, geom1_params.x):
        geom = THREE.RingGeometry.new(geom1_params.innerRadius,geom1_params.outerRadius,geom1_params.thetaSegments)
        geom.translate(geom1_params.innerRadius*i, geom1_params.outerRadius*i,((geom1_params.innerRadius+geom1_params.outerRadius)*i)/geom1_params.x) 
        geom.rotateY(math.radians(geom1_params.rotation)/geom1_params.x*i)
        geom.scale(geom1_params.z*geom1_params.x, geom1_params.z*geom1_params.x, geom1_params.z*geom1_params.x)  

        ring = THREE.Mesh.new(geom, material)
        rings.append(ring)
        scene.add(ring) 

    
        edges = THREE.EdgesGeometry.new( ring.geometry )
        line = THREE.LineSegments.new( edges, line_material)
        ring_lines.append(line)
        scene.add( line )

    #-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    # Set up GUI
    gui = window.dat.GUI.new()
    param_folder = gui.addFolder('Parameters')
    param_folder.add(geom1_params, 'innerRadius', 0,20,0.1)
    param_folder.add(geom1_params, 'outerRadius', 0,10,0.1)
    param_folder.add(geom1_params, 'rotation', 160,300,1)
    param_folder.add(geom1_params, 'x', 0,50,1)
    param_folder.add(geom1_params, 'y', -50, -2, 1)
    param_folder.add(geom1_params, 'z', -0.6,0.6,0.01)
    param_folder.open()
    
    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS
# Update rings
def update_rings():
    global rings, ring_lines, material, line_material
    if len(rings) != 0:
        
        if len(rings) != geom1_params.x:
            for ring in rings: scene.remove(ring)
            for line in ring_lines: scene.remove(line)
            rings = []
            ring_lines = []
            
            for i in range(geom1_params.y, geom1_params.x):
                geom = THREE.RingGeometry.new(geom1_params.innerRadius,geom1_params.outerRadius,geom1_params.thetaSegments)

                geom.translate(geom1_params.innerRadius*i, geom1_params.outerRadius*i,(geom1_params.innerRadius+geom1_params.outerRadius)*i/geom1_params.x)
                geom.rotateY(math.radians(geom1_params.rotation)/geom1_params.x*i)
                geom.scale(geom1_params.z*geom1_params.x, geom1_params.z*geom1_params.x, geom1_params.z*geom1_params.x)
                geom.scale(geom1_params.z*geom1_params.y, geom1_params.z*geom1_params.y, geom1_params.z*geom1_params.y)

                ring  = THREE.Mesh.new(geom, material)
                rings.append(ring)

                scene.add(ring)

                edges = THREE.EdgesGeometry.new( ring.geometry )
                line = THREE.LineSegments.new( edges, line_material)
                ring_lines.append(line)
                scene.add( line )
                
        else:
            for i in range(len(rings)): 
                ring = rings[i]
                line = ring_lines[i]
                

                geom = THREE.RingGeometry.new(geom1_params.innerRadius,geom1_params.outerRadius,geom1_params.thetaSegments)

                geom.translate(geom1_params.innerRadius*i, geom1_params.outerRadius*i,(geom1_params.innerRadius+geom1_params.outerRadius)*i/geom1_params.x)
                geom.rotateY(math.radians(geom1_params.rotation)/geom1_params.x*i)
                geom.scale(geom1_params.z*geom1_params.x, geom1_params.z*geom1_params.x, geom1_params.z*geom1_params.x)
                geom.scale(geom1_params.z*geom1_params.y, geom1_params.z*geom1_params.y, geom1_params.z*geom1_params.y)
                
                ring.geometry = geom

                edges = THREE.EdgesGeometry.new( ring.geometry )
                line.geometry = edges

               

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
