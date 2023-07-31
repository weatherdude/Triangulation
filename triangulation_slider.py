import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider
import math
import random
import numpy as np
import matplotlib as mpl

c = 0.4 # distance between both cameras (m)
A = [0,0,0]   # fisheye coordinates
B = [c,0,0]   # PTF (or 2nd fisheye) coordinates
object_coordinates = [1,50,1000] # x,y,z coordinates (m)
alpha1_unc = 0.02   # error in alpha1 (°)
beta1_unc = 0.02    # error in beta1 (°)

# Initial coordinates of the triangle
x0, y0, z0 = 0.0, 0.0, 0.0  # fisheyes
x1, y1, z1 = c, 0, 0        # PTF (or 2nd fisheye)
x2, y2, z2 = object_coordinates[0], object_coordinates[1], object_coordinates[2]

# Get the monitor screen size
default_dpi = mpl.rcParams['figure.dpi']
monitor_size = (1920, 1080)  # Replace this with your monitor's resolution if necessary
fig_width = monitor_size[0] * 0.75 / default_dpi
fig_height = monitor_size[1] * 0.75 / default_dpi
print(fig_width)
# Create the 3D plot
fig = plt.figure(figsize=(fig_width, fig_height))
fig.canvas.set_window_title("Object triangulation calculator")  # Set the window title
ax = fig.add_subplot(221, projection='3d')
ax2 = fig.add_subplot(222)
# Function to update the plot based on the slider values
def update(val):
    global x0, y0, z0, x1, y1, z1, x2, y2, z2
    x1 = slider_dist.val
    x2, y2, z2 = slider_x.val, slider_y.val, slider_z.val
    alpha1_unc = slider_alpha_unc.val
    beta1_unc = slider_beta_unc.val

    # Clear previous plot and create the updated triangle
    ax.clear()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    # ax.set_title('Object triangulation calculator')
    triangle = [[(x0, y0, z0), (x1, y1, z1), (x2, y2, z2)]]
    ax.add_collection3d(Poly3DCollection(triangle, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))
    ax.scatter([x0, x1, x2], [y0, y1, y2], [z0, z1, z2], color='r', s=50)
    ax.set_xlim(min([x0, x1, x2])-5, max([x0, x1, x2])+5)
    ax.set_ylim(min([y0, y1, y2])-5, max([y0, y1, y2])+5)
    ax.set_zlim(min([z0, z1, z2])-5, max([z0, z1, z2])+5)

    c = x1 # distance between both cameras (m)
    B = [c,0,0]   # PTF coordinates
    object_coordinates = [x2,y2,z2] # x,y,z coordinates (m)
    dx = object_coordinates[0]
    dy = object_coordinates[1]
    dz = object_coordinates[2]

    #d = math.sqrt(object_coordinates[2]**2 + object_coordinates[1]**2)
    b1 = math.sqrt((object_coordinates[0]-A[0])**2+(object_coordinates[1]-A[1])**2+
                (object_coordinates[2]-A[2])**2) # distance between fisheye and object
    a1 = math.sqrt((object_coordinates[0]-B[0])**2+(object_coordinates[1]-B[1])**2+
                (object_coordinates[2]-B[2])**2) # distance between PTF and object
    b = math.sqrt(b1**2 - dz**2)
    a = math.sqrt(a1**2 - dz**2)
    beta1 = math.asin(dz/b1) * 180/math.pi
    alpha1 = math.acos(dx/b) * 180/math.pi
    alpha2 = math.acos((c-dx)/a) * 180/math.pi

    # now calculate uncertainty in distance calc based on assumed error in the determined angles
    # we assume that the error is normally distributed with a chance of 3 standard dev. that the given error is exceeded
    mean = 0
    stdev = alpha1_unc/3
    alpha1_unc_list = [random.gauss(mean, stdev) for _ in range(100)]

    stdev = beta1_unc/3
    beta1_unc_list = [random.gauss(mean, stdev) for _ in range(100)]

    dist_list = []
    for i in range(0,len(alpha1_unc_list)):
        alpha_unc = alpha1+alpha1_unc_list[i]
        for j in range(0,len(beta1_unc_list)):
            beta_unc=beta1+beta1_unc_list[j]
            alpha3 = 180 - alpha_unc - alpha2
            b = math.sin(alpha2*math.pi/180) * c/math.sin(alpha3*math.pi/180) # horizontal distance Fisheye - Object
            b1_unc = b/math.cos(beta_unc*math.pi/180) # distance Fisheye - object
            dist_list.append(b1_unc)
    
    ax2.clear()
    ax2.hist(dist_list, density=False, bins=100)  # density=False would make counts
    ax2.set_xlabel('Distance uncertainty (m)')
    ax2.set_ylabel('Count')
    # ax2.ylabel('Counts')
    # ax2.xlabel('Distances')
    # Add the annotation box
    ax.text2D(0.00, -0.40, "Distance Fisheye-Object = "+str(round(b1,2))+" m", transform=ax.transAxes, fontsize=12,
              bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax.text2D(2.25, -0.40, "Uncertainty range = "+str(round(max(dist_list)-min(dist_list),2))+" m", transform=ax.transAxes, fontsize=12,
              bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    fig.canvas.draw_idle()

# Create sliders for each coordinate
ax_dist = plt.axes([0.25, 0.02, 0.45, 0.03], facecolor='lightgoldenrodyellow')
ax_x = plt.axes([0.25, 0.07, 0.45, 0.03], facecolor='lightgoldenrodyellow')
ax_y = plt.axes([0.25, 0.12, 0.45, 0.03], facecolor='lightgoldenrodyellow')
ax_z = plt.axes([0.25, 0.17, 0.45, 0.03], facecolor='lightgoldenrodyellow')
ax_alpha_unc = plt.axes([0.25, 0.22, 0.45, 0.03], facecolor='lightgoldenrodyellow')
ax_beta_unc = plt.axes([0.25, 0.27, 0.45, 0.03], facecolor='lightgoldenrodyellow')

slider_dist = Slider(ax_dist, 'Distance cameras (m)', 0.1, 100.0, valinit=c)
slider_x = Slider(ax_x, 'Object x pos. (m)', -100.0, 100.0, valinit=object_coordinates[0])
slider_y = Slider(ax_y, 'Object y pos. (m)', -100.0, 100.0, valinit=object_coordinates[1])
slider_z = Slider(ax_z, 'Object height (m)', 0, 10000.0, valinit=object_coordinates[2])
slider_alpha_unc = Slider(ax_alpha_unc, 'Azimuth uncertainty (°)', 0.01, 1, valinit=alpha1_unc)
slider_beta_unc = Slider(ax_beta_unc, 'Elevation uncertainty (°)', 0.01, 1, valinit=beta1_unc)

# Call the update function when the slider values change
slider_dist.on_changed(update)
slider_x.on_changed(update)
slider_y.on_changed(update)
slider_z.on_changed(update)
slider_alpha_unc.on_changed(update)
slider_beta_unc.on_changed(update)

plt.show()
