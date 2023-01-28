# Import javascript modules
from js import THREE, window, document, Object, console
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math
import numpy as np



geom1_params = {
        "innerRadius":0.6,
        "outerRadius": 0.1,
        "scale": 5,
        "width": 10,
        "lenght": 20,
        "wave": 82
}

   
geom1_params = Object.fromEntries(to_js(geom1_params))

extrudeSettings = {
                        "steps": 1,
                        "depth": 0.1,
                        "bevelEnabled": True,
                        "bevelThickness": 0.1,
                        "bevelSize": 0.1,
                        "bevelOffset": 0.1,
                        "bevelSegments": 0.1
                    }

extrudeSettings = Object.fromEntries(to_js(extrudeSettings))

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
    camera = THREE.PerspectiveCamera.new(-100, window.innerWidth/window.innerHeight, 0.4, 100)
    camera.position.z = -3
    camera.position.x = -4
    camera.position.y = -4

    scene.add(camera)

    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
    #-----------------------------------------------------------------------
  
    # Geometry Creation

   

    global material

    material = THREE.MeshBasicMaterial.new()
    material.transparent = True
    material.opacity = 0.6
    material.color = THREE.Color.new("rgb(163, 59, 37)")
    
    global line_material
    
    line_material = THREE.LineBasicMaterial.new()
    line_material.color = THREE.Color.new("rgb(163, 59, 37)")
    line_material.transparent = True
    line_material.opacity = 0.5

    axeshelper = THREE.AxesHelper.new()
    scene.add(axeshelper)

    generate_ring()
    

    #-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    # Set up GUI
    gui = window.lil.GUI.new()
    gui.add(geom1_params, 'innerRadius', 0,0.5,0.1)
    #ui.add(geom1_params, 'outerRadius', 0,0.5,0.1)
    gui.add(geom1_params, 'width', 0, 60, 1)
    gui.add(geom1_params, 'lenght', 0, 60, 1)
    gui.add(geom1_params, 'wave', -100, 100, 1)
    gui.add(extrudeSettings, "depth",0,0.5, 0.1)
   
    gui.open()
   
    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
   
    #material.color = color

   
   
def generate_ring(): 

    global innerRadius, outerRadius, widht, lenght, wave

    
    innerRadius = geom1_params.innerRadius
    outerRadius = geom1_params.outerRadius
    widht = geom1_params.width
    lenght = geom1_params.lenght
    wave = geom1_params.wave


    rings2 = THREE.RingGeometry.new(innerRadius, outerRadius, 10)
    normals = rings2.getAttribute("position")
       
    vector0 = THREE.Vector3.new()
    vector0.fromBufferAttribute(normals,0 )
    
    vector1 = THREE.Vector3.new()
    vector1.fromBufferAttribute(normals,1)

    vector2 = THREE.Vector3.new()
    vector2.fromBufferAttribute(normals,2)

    vector3 = THREE.Vector3.new()
    vector3.fromBufferAttribute(normals,3)

    vector4 = THREE.Vector3.new()
    vector4.fromBufferAttribute(normals,4)

    vector5 = THREE.Vector3.new()
    vector5.fromBufferAttribute(normals,5)

    vector6 = THREE.Vector3.new()
    vector6.fromBufferAttribute(normals,6)

    vector7 = THREE.Vector3.new()
    vector7.fromBufferAttribute(normals,7)

    vector8 = THREE.Vector3.new()
    vector8.fromBufferAttribute(normals,8)

    vector9 = THREE.Vector3.new()
    vector9.fromBufferAttribute(normals,9)

    shape = THREE.Shape.new()
    shape.moveTo(vector0.x, vector0.y)
    shape.lineTo(vector1.x, vector1.y)
    shape.lineTo(vector2.x, vector2.y)
    shape.lineTo(vector3.x, vector3.y)
    shape.lineTo(vector4.x, vector4.y)
    shape.lineTo(vector5.x, vector5.y)
    shape.lineTo(vector6.x, vector6.y)
    shape.lineTo(vector7.x, vector7.y)
    shape.lineTo(vector8.x, vector8.y)
    shape.lineTo(vector9.x, vector9.y)

    global extrude_lenght
    extrude_lenght = extrudeSettings.depth
    
    
    Shape_extusion = THREE.ExtrudeGeometry.new(shape, extrudeSettings)
    


    for i in range(widht):


        rings2.translate(i, math.sin(i*wave),0)
        Shape_extusion.translate(i, math.sin(i*wave),0)
    

        for j in range(lenght):

            rings3 = rings2.clone().translate(0,math.sin(j*wave),j)
            shape2 = Shape_extusion.clone().translate(0, math.sin(j*wave),j)
        

            ring_lines = THREE.EdgesGeometry.new(rings3)
            ring_lines_mesh = THREE.LineSegments.new(ring_lines, line_material)

            normals = THREE.BufferAttribute.new()

            shape_mesh = THREE.Line.new(shape2, line_material)
            scene.add(shape_mesh)

            scene.add(ring_lines_mesh)

#-----------------------------------------------------------------------
# HELPER FUNCTIONS
# Update rings
def update_rings():
    global material, line_material, extrude_lenght
    
        
    if geom1_params.outerRadius != outerRadius or geom1_params.innerRadius != innerRadius or widht != geom1_params.width or lenght != geom1_params.lenght or wave != geom1_params.wave or extrude_lenght != extrudeSettings.depth:
        scene.clear()
        
        generate_ring()
        extrude_lenght = extrudeSettings.depth
                     

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

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth*2000 * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight*2000 * pixelRatio )
   
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
