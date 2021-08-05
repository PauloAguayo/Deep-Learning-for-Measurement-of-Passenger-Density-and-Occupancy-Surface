import numpy as np
import random
from scipy.spatial import Voronoi, ConvexHull,voronoi_plot_2d
import matplotlib.pyplot as plt


coords = np.array([[random.randint(1,10), random.randint(1,14)] for _ in range(10)])
print(coords)
vor = Voronoi(coords)

print('REGIONES')
print(vor.regions) # se componen de los vertices

################# SECCION DE POLINOMIO CERRADOS ####################3
ind = 0

regiones_abiertas = []

for r in vor.regions:
    if (np.array(r)>=0).all() and len(r)>0:
        ind+=1
        print('REGION',str(ind))
        # polinomio = []
        # for i in r:
        #     polinomio.append(vor.vertices[i])
        #
        # pts = np.array(polinomio).reshape((-1,1,2))
        # #cv2.polylines(image,[pts],True,(0,255,0))
        #
        # hull = ConvexHull(polinomio)

        # cx = np.mean(hull.points[hull.vertices,0])
        # cy = np.mean(hull.points[hull.vertices,1])
        # polygons.append(hull.volume)
        # polygon_area += hull.volume

#########################################################################
    elif (np.array(r)<0).any() and len(r)>0:
        reg = [vor.vertices[j] for j in r if j>=0]
        if len(reg)>1:
            for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
                simplex = np.asarray(simplex)
                if np.any(simplex < 0) and simplex[simplex >= 0][0] == :
                    i = simplex[simplex >= 0][0] # finite end Voronoi vertex
                    t = rec_points[pointidx[1]] - rec_points[pointidx[0]]  # tangent
                    t = t / np.linalg.norm(t)
                    n = np.array([-t[1], t[0]]) # normal
                    midpoint = rec_points[pointidx].mean(axis=0)
                    p_f = vor.vertices[i] + np.sign(np.dot(midpoint - t, n)) * n * 1700
                    p_i = np.array([round(vor.vertices[i,0]),round(vor.vertices[i,1])])  # x,y     # vertices infinitos de voronoi

                    line2 = np.vstack((p_f,p_i))

                    for (_0,_1) in zip(np.array(self.poly_points),np.array(self.poly_points_shift)):
                        line1 = np.vstack((_0,_1))
                        intersection = self.measures.line_intersection(line1,line2)

                        continuacion_poly_points.append(_0)

                        if self.poly_extended.contains(geometry.Point(intersection)):
                            continuacion_poly_points.append(intersection)
                            begin_end.append(intersection)

        else:
            




fig = voronoi_plot_2d(vor)
plt.show()
