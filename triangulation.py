import math
import numpy as np 

## calculate distance to object from azimuth and elevation angles
alpha1 = 45     # fisheye azimuth (°)
beta1 = 60      # fisheye elevation (°)
alpha2 = 45     # PTF azimuth (°)
beta2 = 60      # PTF elevation (°)
c = 0.4         # distance between both cameras (m)
A = [0,0,0]     # fisheye coordinates
B = [c,0,0]     # PTF coordinates

alpha3 = 180 - alpha1 - alpha2
b = math.sin(alpha2*math.pi/180) * c/math.sin(alpha3*math.pi/180)   # horizontal distance Fisheye - Object
b1 = b/math.cos(beta1*math.pi/180)                                  # distance Fisheye - object
dx = b * math.cos(alpha1*math.pi/180)                               # x coordinate of object
dy = b * math.sin(alpha1*math.pi/180)                               # y coordinate of object
dz = b1 * math.sin(beta1*math.pi/180)                               # z coordinate of object
object_coordinates = [dx,dy,dz]

## back calculation 
b1 = math.sqrt((object_coordinates[0]-A[0])**2+(object_coordinates[1]-A[1])**2+
               (object_coordinates[2]-A[2])**2) # distance between fisheye and object
b = math.sqrt(b1**2 - dz**2)
beta1 = math.asin(dz/b1) * 180/math.pi
alpha1 = math.acos(dx/b) * 180/math.pi

# calculate distance to object with object coordinates
c = 100         # distance between both cameras (m)
B = [c,0,0]     # PTF coordinates
object_coordinates = [1,50,100] # x,y,z coordinates (m)
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

# print("beta1 ="+ str(beta1))
# print("alpha1 ="+ str(alpha1))
# print("alpha2 ="+ str(alpha2))

# now calculate uncertainty in distance calc based on assumed error of 0.1° in alpha1 and beta1
dist_list = []
for i in np.linspace(-0.1,0.1,1000):
    alpha_unc = alpha1+i
    for j in np.linspace(-0.1,0.1,1000):
        beta_unc=beta1+j
        alpha3 = 180 - alpha_unc - alpha2
        b = math.sin(alpha2*math.pi/180) * c/math.sin(alpha3*math.pi/180)   # horizontal distance Fisheye - Object
        b1 = b/math.cos(beta_unc*math.pi/180)                               # distance Fisheye - object
        dist_list.append(b1)

# plot histogram
import matplotlib.pyplot as plt
plt.hist(dist_list, density=False, bins=1000)  # density=False would make counts
plt.ylabel('Counts')
plt.xlabel('Distances')
plt.show()