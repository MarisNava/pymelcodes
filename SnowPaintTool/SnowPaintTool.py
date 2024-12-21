#In roder to get a well function of the script, a mesh needs to be created and then start to use de Snow Paint tool
import maya.cmds as cmds
import maya.mel as mel

def snow_tool():
    #Delete previous window
    if cmds.window("Snow particle tool", ex=True):
        cmds.deleteUI("Snow particle tool", window=True)
    #Create new window	
    window = cmds.window("Snow particle tool", title="Snow Particle Pool", widthHeight=(400, 400))
    cmds.columnLayout( adjustableColumn=True )

    #Create widgets
    makeLiveWidget()
    paintParticlesWidget()
    tesellateWidget()
    geometryAttributesWidget()

    cmds.showWindow( window )

#Widgets
def makeLiveWidget():
    cmds.text(label='1: Make selected geometry live')
    cmds.button(label='Make Selected Geometry Live', c=makeLive)
    cmds.separator()

def paintParticlesWidget():
    cmds.text(label='2: Paint Particles')
    cmds.button(label='Paint Particles (Press 'Q' when finish)', c=paintParticles)
    cmds.separator()

def tesellateWidget():
    cmds.text(label='3: Tesellate Particles')
    cmds.button(label='Tesellate Particles', c=tesellate)
    cmds.separator()

def geometryAttributesWidget():
    cmds.text(label='4: Play with the attributes')
    createFloatSliderGrp(key='threshold', label='Threshold:', minValue=0.00, maxValue=1.0, step = 0.01, dragCommand=set_threshold, value=0.5 )
    createFloatSliderGrp(key='blobby_radius_scale', label='Blobby Radius Scale:', minValue=0.1, maxValue=5, step = 0.1, dragCommand=set_blobby_radius_scale, value=1.0 )
    createFloatSliderGrp(key='mesh_triangle_size', label='Mesh Triangle Size:', minValue=0.01, maxValue=1.0, step = 0.01, dragCommand=set_mesh_triangle_size, value=0.1 )
    cmds.text(label="Mesh Method")
    cmds.optionMenu("meshMethodMenu", changeCommand=set_mesh_method)
    cmds.menuItem(label="Triangle Mesh")
    cmds.menuItem(label="Tetrahedra")
    cmds.menuItem(label="Acute Tetrahedra")
    cmds.menuItem(label="Quad Mesh")
    createFloatSliderGrp(key='smoothing_iterations', label='Smoothing Iterations:', minValue=0, maxValue=10, step = 1, dragCommand=set_smoothing_iterations, value=0 )
    cmds.separator()

#Create sliders
def createFloatSliderGrp(key, label, minValue, maxValue, value, dragCommand, step =1, field=True):
        name = cmds.floatSliderGrp (field=field, label=label, minValue=minValue, maxValue=maxValue, step=step, dragCommand=dragCommand, value=value)
        return name

#Buttons Functions
def makeLive(*args):
    selection = cmds.ls(sl=True)
    for object in selection:
        cmds.makeLive( object )

def paintParticles(*args):
    cmds.dynParticleCtx('dynParticleContext', nc=True, e=True, nj=5, jr=1.5, sk=True)
    cmds.setToolTo("dynParticleContext")
    #mel.eval('dynSketchCB dynParticleContext 1')

def tesellate(*args):
    mel.eval("particleToPoly")

#Snow Attributes
def set_threshold(value):
    set_particle_attribute("threshold", value)

def set_blobby_radius_scale(value):
    set_particle_attribute("blobbyRadiusScale", value)

def set_mesh_triangle_size(value):
    set_particle_attribute("meshTriangleSize", value)

def set_mesh_method(value):
    mapping = {"Triangle Mesh": 0, "Tetrahedra": 1, "Acute Tetrahedra": 2, "Quad Mesh": 3}
    set_particle_attribute("meshMethod", mapping[value])

def set_smoothing_iterations(value):
    set_particle_attribute("meshSmoothingIterations", value)

def set_particle_attribute(attr_name, value):
    print("set_particle_attribute")
    particle_node = cmds.ls(type="nParticle")
    if not particle_node:
        cmds.warning("No nParticle node found. Ensure particles are created and converted.")
        return

    particle_node = particle_node[0]

    if cmds.attributeQuery(attr_name, node=particle_node, exists=True):
        cmds.setAttr(f"{particle_node}.{attr_name}", value)
        print(f"Set {attr_name} to {value} on {particle_node}")
    else:
        cmds.warning(f"Attribute {attr_name} not found on {particle_node}.")

#Call Function
snow_tool()