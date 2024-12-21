#In order to work this code needs run with the .ma file named "CityEngine.ma"
import random
import maya.cmds as cmds


# Function to update the grid parameters
def update_grid_params():
    
    global grid_size, cell_size, min_levels, max_levels, building_width, building_depth

    grid_size = cmds.intSliderGrp(gridSizeSlider, query=True, value=True)
    cell_size = cmds.intSliderGrp(cellSizeSlider, query=True, value=True)
    min_levels = cmds.intSliderGrp(minLevelsSlider, query=True, value=True)
    max_levels = cmds.intSliderGrp(maxLevelsSlider, query=True, value=True)
    building_width = cmds.intSliderGrp(buildingWidthSlider, query=True, value=True)
    building_depth = cmds.intSliderGrp(buildingDepthSlider, query=True, value=True)

# Define grid parameters
grid_size = 2  # Number of cells in the grid
cell_size = 6    # Size of each grid cell

# Define building parameters
min_levels = 4  # Minimum number of building levels 
max_levels = 14  # Maximum number of building levels
building_width = 2  # Width of the building
building_depth = 2  # Depth of the building
instances=[]

# Function to create a random building
def create_building(x, z, initial_geometries, intermediate_geometries, final_geometries):
    levels = random.randint(min_levels, max_levels)
    group_name = cmds.group(em=True, name='Building')
    for level in range(levels):
        level_height = (level + 1) * cell_size
        
        if level == 0:
            random_geometry = random.choice(initial_geometries)
        elif level == levels - 1:
            random_geometry = random.choice(final_geometries)
        else:
            random_geometry = random.choice(intermediate_geometries)
        
        if random_geometry == 'level_01':
            randy= random.randint(0,4000000)
            instance_name = cmds.instance(random_geometry, name=random_geometry + "_inst1%d" % randy)
        elif random_geometry == 'level_02':
            randy= random.randint(0,5000000)
            instance_name = cmds.instance(random_geometry, name=random_geometry + "_inst2%d" % randy)
        elif random_geometry == 'level_03':
            randy= random.randint(0,6000000)
            instance_name = cmds.instance(random_geometry, name=random_geometry + "_inst3%d" % randy)
        elif random_geometry == 'level_04':
            randy= random.randint(0,7000000)
            instance_name = cmds.instance(random_geometry, name=random_geometry + "_inst4%d" % randy)
        elif random_geometry == 'level_05':
            randy= random.randint(0,8000000)
            instance_name = cmds.instance(random_geometry, name=random_geometry + "_inst5%d" % randy)
        elif random_geometry == 'level_06':
            randy= random.randint(0,9000000)
            instance_name = cmds.instance(random_geometry, name=random_geometry + "_inst6%d" % randy)
        elif random_geometry == 'level_07':
            randy= random.randint(0,3000000)
            instance_name = cmds.instance(random_geometry, name=random_geometry + "_inst4%d" % randy)
        elif random_geometry == 'level_08':
            randy= random.randint(0,2000000)
            instance_name = cmds.instance(random_geometry, name=random_geometry + "_inst5%d" % randy)
        elif random_geometry == 'level_09':
            randy= random.randint(0,1000000)
            instance_name = cmds.instance(random_geometry, name=random_geometry + "_inst6%d" % randy)
        elif random_geometry == 'level_10':
            randy= random.randint(0,4000000)
            instance_name = cmds.instance(random_geometry, name=random_geometry + "_inst4%d" % randy)
        elif random_geometry == 'level_11':
            randy= random.randint(0,6000000)
            instance_name = cmds.instance(random_geometry, name=random_geometry + "_inst5%d" % randy)
        elif random_geometry == 'level_12':
            randy= random.randint(0,8000000)
            instance_name = cmds.instance(random_geometry, name=random_geometry + "_inst6%d" % randy)
        elif random_geometry == 'level_13':
            randy= random.randint(0,7000000)
            instance_name = cmds.instance(random_geometry, name=random_geometry + "_inst6%d" % randy)
           
        cmds.move(x, level_height-8, z, instance_name)
        cmds.rotate(0,90*(random.randint(1,3)),0,instance_name)        
        instances.append(instance_name)
        cmds.parent(instance_name,group_name)
    return group_name  

# Create buildings on the grid
def create_block():
    group_name = cmds.group(em=True, name='Block')
    for i in range(grid_size):
        for j in range(grid_size):
            x = i * cell_size
            z = j * cell_size
            
            initial_geometries = ['level_01', 'level_02', 'level_03', 'level_04']
            intermediate_geometries = ['level_12','level_06','level_05',]
            final_geometries = ['level_07', 'level_09', 'level_08', 'level_10', 'level_11', 'level_13']
            
            buildingname= create_building(x, z, initial_geometries, intermediate_geometries, final_geometries)
            cmds.parent(buildingname,group_name)
    return group_name 
     

def city():
    group_name= cmds.group(em=True,name='City')
    for i in range(building_width):
        for j in range(building_depth):
            x = i * grid_size*10
            z = j * grid_size*10
            
            blockname= create_block()
            cmds.move(x, 0, z, blockname)
            cmds.parent(blockname,group_name) 

# Create UI window
window = cmds.window(title='City Engine', widthHeight=(300, 200))

# Create main layout
main_layout = cmds.columnLayout(adjustableColumn=True)

# Grid size slider
gridSizeSlider = cmds.intSliderGrp(label='Grid Size', field=True, minValue=1, maxValue=20, value=grid_size,
                                   columnAlign=(1, 'right'), columnWidth=(1, 100),
                                   changeCommand=lambda x: update_grid_params())
# Cell size slider
cellSizeSlider = cmds.intSliderGrp(label='Cell Size', field=True, minValue=1, maxValue=20, value=cell_size,
                                   columnAlign=(1, 'right'), columnWidth=(1, 100),
                                   changeCommand=lambda x: update_grid_params())
# Min levels slider
minLevelsSlider = cmds.intSliderGrp(label='Min Levels', field=True, minValue=2, maxValue=10, value=min_levels,
                                    columnAlign=(1, 'right'), columnWidth=(1, 100),
                                    changeCommand=lambda x: update_grid_params())
# Max levels slider
maxLevelsSlider = cmds.intSliderGrp(label='Max Levels', field=True, minValue=4, maxValue=15, value=max_levels,
                                    columnAlign=(1, 'right'), columnWidth=(1, 100),
                                    changeCommand=lambda x: update_grid_params())
# Building width slider
buildingWidthSlider = cmds.intSliderGrp(label='Width City', field=True, minValue=2, maxValue=8,
                                        value=building_width, columnAlign=(1, 'right'), columnWidth=(1, 100),
                                        changeCommand=lambda x: update_grid_params())
# Building depth slider
buildingDepthSlider = cmds.intSliderGrp(label='Depth City', field=True, minValue=2, maxValue=8,
                                        value=building_depth, columnAlign=(1, 'right'), columnWidth=(1, 100),
                                        changeCommand=lambda x: update_grid_params())
# Create city button
cmds.button(label='Create City', command='city()')
# Show the UI window
cmds.showWindow(window)
