import cv2
from measurements import Measurements
import numpy as np
from object_detection.utils import visualization_utils as vis_util
from shapely import geometry
from scipy.spatial import Voronoi, ConvexHull
import xlsxwriter


class Drawing(object):
    def __init__(self,outcomes,image,copy_image,final_image,min_score,angle):
        self.image = image
        self.copy_image = copy_image
        self.final_image = final_image
        self.copy = self.image.copy()
        self.image_center = np.array([int(self.image.shape[0]/2),int(self.image.shape[1]/2)]) # (y,x)
        self.image_bottom = np.array([int(self.image.shape[0]),int(self.image.shape[1]/2)]) # (y,x)
        self.min_score = min_score
        self.max_length = np.maximum(self.image.shape[0],self.image.shape[1])
        self.measures = Measurements(outcomes)
        self.origin = np.array([0,0])
        self.angle = angle

    def Prepare_data(self,scores,boxes,classes):
        self.scores = scores
        self.boxes = boxes
        self.classes = classes

    def Draw_detections(self,n,H,h):
        print("------ DRAWING DETECTIONS AND OPTIMIZING PROJECTIONS ------")
        self.rec_points = []  # array of projections
        def Quadrant(y,x,beta,photo,caja,clase): # (y,x) centroid detection box

            if x<=self.image_bottom[1]:
                x_axis = np.arange(x,self.image_bottom[1]+1)
                x_axis = x_axis[::-1]
                y_axis = np.arange(y,self.image_bottom[0]+1)
                y_axis = y_axis[::-1]
            elif x>self.image_bottom[1]:
                x_axis = np.arange(self.image_bottom[1],x+1)
                y_axis = np.arange(y,self.image_bottom[0]+1)
                y_axis = y_axis[::-1]

            zlope = (y-self.image_bottom[0])/(x-self.image_bottom[1])

            x_f = x
            y_f = y
            if len(x_axis) >= len(y_axis):
                y_axis = []
                for x in x_axis:
                    y_axis.append((-1)*(zlope*(x_f-x)-y_f))

            else:
                x_axis = []
                for y in y_axis:
                    x_axis.append((-1)*((y_f-y)/zlope-x_f))

            # optimization points
            lim = 0
            beta*=(self.max_length/self.angle)
            coords = [-100,-100]
            for x_p,y_p in zip(x_axis,y_axis):
                bottom2Coord = np.linalg.norm(np.array([y_p,x_p])-self.image_bottom)
                #cv2.circle(photo,(int(x_p),int(y_p)),1,(255,255,0),-1)
                if bottom2Coord<=abs(beta):
                    if bottom2Coord>lim:
                        lim = bottom2Coord
                        coords = [y_p,x_p]

            # coords y,x
            #cv2.circle(photo,(int(coords[1]),int(coords[0])),3,(255,0,0),-1)
            geom_coords = geometry.Point([coords[1],coords[0]])
            if self.poly.contains(geom_coords):
                self.rec_points.append([int(coords[0]),int(coords[1])])
                vis_util.draw_bounding_box_on_image_array(photo,caja[0],caja[1],caja[2],caja[3],color='red',thickness=4,display_str_list=()) # HEADS
                cv2.circle(photo,(int(coords[1]),int(coords[0])),3,(255,0,0),-1)
                return(1)
            return(0)

        people = 0
        if n==1:
            photo = self.image
        elif n==0:
            photo = self.copy_image
        else:
            photo = self.final_image

        #cv2.circle(photo,(self.image_center[1],self.image_center[0]),7,(255,255,255),-1)
        for (puntaje,caja,clase) in zip(self.scores,self.boxes,self.classes):
            distance_x = caja[3] - caja[1]
            distance_y = caja[2] - caja[0]
            point = np.array([(caja[1]+distance_x/2.0)*photo.shape[1],(caja[0]+distance_y/2.0)*photo.shape[0]]) # (x,y)   centroid box
            if point[1]<0: point[1] = 0
            if point[0]<0: point[0] = 0

            if (puntaje>=self.min_score) and (clase==1.0 or clase==4.0):
                # pixel's distance to radians
                gamma = np.linalg.norm(np.array([point[1],point[0]])-self.image_bottom)
                gamma *= (self.angle/(self.max_length))

                d1_prima = np.tan(gamma)*H
                d1 = d1_prima - np.tan(gamma)*h
                alpha = np.arctan(d1/H)
                #beta = abs(gamma) - abs(alpha)
                beta = gamma - alpha
                people+=Quadrant(int(point[1]),int(point[0]),float(beta),photo,caja,clase)
        return(people)

    def Generate_Polygon(self, nameWindow):
        def draw_circle(event,x,y,flags,param):
            global mouseX,mouseY
            if event == cv2.EVENT_LBUTTONDBLCLK:
                cv2.circle(self.copy_image,(x,y),6,(0,255,255),-1)
                mouseX,mouseY = x,y

        cv2.namedWindow(nameWindow)
        cv2.setMouseCallback(nameWindow,draw_circle)
        points = []
        point_counter = 0
        while(1):
            cv2.imshow(nameWindow,self.copy_image)
            k = cv2.waitKey(20) & 0xFF
            if k == 27:
                break
            elif k == ord('a'):
                point_counter+=1
                points.append([mouseX,mouseY])
                cv2.circle(self.copy_image,(mouseX,mouseY),8,(0,0,0),3)
                cv2.putText(self.copy_image, str(point_counter), (mouseX,mouseY-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1)
            elif k == ord('r'):
                for i,c in zip(points,np.arange(1,point_counter+1)):
                    cv2.circle(self.copy_image,(i[0],i[1]),8,(255,255,255),-1)
                    cv2.line(self.copy_image,(i[0]-6,i[1]-6),(i[0]+6,i[1]+6),(0,0,0),2)
                    cv2.line(self.copy_image,(i[0]+6,i[1]-6),(i[0]-6,i[1]+6),(0,0,0),2)
                    cv2.putText(self.copy_image, str(c), (i[0],i[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
                points = []
                point_counter = 0
        cv2.destroyAllWindows()

        self.poly = geometry.Polygon(points)
        self.centroid = np.array(list(self.poly.centroid.coords)[0]) # x,y

        extended_points = []
        for punto in points:
            if (punto[0] <= self.centroid[0]) and (punto[1] <= self.centroid[1]):
                extended_points.append([punto[0]-10,punto[1]-10])
            elif (punto[0] <= self.centroid[0]) and (punto[1] > self.centroid[1]):
                extended_points.append([punto[0]-10,punto[1]+10])
            elif (punto[0] > self.centroid[0]) and (punto[1] <= self.centroid[1]):
                extended_points.append([punto[0]+10,punto[1]-10])
            elif (punto[0] > self.centroid[0]) and (punto[1] > self.centroid[1]):
                extended_points.append([punto[0]+10,punto[1]+10])

        self.poly_extended = geometry.Polygon(extended_points)

        self.image_bottom[1] = self.centroid[0]

        self.poly_points = points
        self.poly_points_shift = [ p for p in points[1:]]
        self.poly_points_shift.append(points[0])

        return(points)

    def Handcrafted(self,dec):
        self.drawing = False # True if mouse is pressed
        self.ix,self.iy = -1,-1

        def draw_square(event,x,y,flags,param):
            global xx,yy

            if x<0: x = 0
            if y<0: y = 0

            if event == cv2.EVENT_LBUTTONDOWN:
                self.drawing = True
                self.ix,self.iy = x,y
                cv2.line(self.copy_image,(self.ix-30,self.iy),(self.ix+30,self.iy),(0,0,0),2)
                cv2.line(self.copy_image,(self.ix,self.iy-30),(self.ix,self.iy+30),(0,0,0),2)
            elif event == cv2.EVENT_MOUSEMOVE:
                if self.drawing == True:
                    dif_x = x-self.ix
                    dif_y = y-self.iy
                    cv2.line(self.copy_image,(self.ix,self.iy),(self.ix+dif_x,self.iy),(0,0,0),2)
                    cv2.line(self.copy_image,(self.ix,self.iy),(self.ix,self.iy+dif_y),(0,0,0),2)
            elif event == cv2.EVENT_LBUTTONUP:
                self.drawing = False
                xx,yy = x,y
                end_point = np.array([xx,yy])
                if np.linalg.norm(end_point-self.origin)<np.linalg.norm([self.ix,self.iy]-self.origin):
                    cv2.rectangle(self.copy_image,(x,y),(self.ix,self.iy),(0,255,0),3)
                elif np.linalg.norm(end_point-self.origin)>np.linalg.norm([self.ix,self.iy]-self.origin):
                    cv2.rectangle(self.copy_image,(self.ix,self.iy),(x,y),(0,255,0),3)
        bx = []
        clss = []
        scr = []
        print(len(self.scores))
        while(dec=='y'):
            cv2.namedWindow('Handcrafted image')
            cv2.setMouseCallback('Handcrafted image',draw_square)
            cv2.imshow('Handcrafted image',self.copy_image)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
            elif k == ord('a'): # Add heads
                text = "Added head"
                cv2.rectangle(self.copy_image,(self.ix,self.iy),(xx,yy),(0,0,255),3)
                cv2.putText(self.copy_image, text, (self.ix , self.iy-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
                centr = np.array([int(abs(self.ix-xx)),int(abs(self.iy-yy))])
                xxx = np.minimum(xx,self.ix)
                yyy = np.minimum(yy,self.iy)
                bx.append([yyy/self.copy_image.shape[0],xxx/self.copy_image.shape[1],(yyy+centr[1])/self.copy_image.shape[0],(xxx+centr[0])/self.copy_image.shape[1]])
                clss.append([4.0])
                scr.append([0.99])
            elif k == ord('z'): # Remove heads
                for c,x in enumerate(self.boxes):
                    bb_gt = [x[1],x[0],x[3],x[2]]
                    bb_remove = [self.ix/self.copy_image.shape[1],self.iy/self.copy_image.shape[0],xx/self.copy_image.shape[1],yy/self.copy_image.shape[0]]
                    if self.measures.iou(bb_remove,bb_gt)>0.5:
                        text = "Detection removed"
                        cv2.rectangle(self.copy_image,(self.ix,self.iy),(xx,yy),(255,0,255),3)
                        cv2.putText(self.copy_image, text, (self.ix , self.iy-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 1)
                        self.classes[c]=3.0
        cv2.destroyAllWindows()
        try:
            bx = np.array(bx)
            self.boxes = np.concatenate((self.boxes,bx))
            clss = np.array(clss)
            self.classes = np.concatenate((self.classes,clss))
            scr = np.array(scr)
            self.scores = np.concatenate((self.scores,scr))
        except:
            self.scores = self.scores
            self.classes = self.classes
            self.boxes = self.boxes

    def Voronoi_diagram(self,image,output_variable,original_area):
        rec_points = np.array(self.rec_points)   # np array of projections

        polygon_number=0
        polygons = []
        polygon_area = 0
        if rec_points.shape[0] == 2:
            rec_points = np.flip(rec_points)
            t = rec_points[1] - rec_points[0]  # tangent
            t = t / np.linalg.norm(t)
            n = np.array([-t[1], t[0]]) # normal
            midpoint = rec_points.mean(axis=0)
            p_f = midpoint + np.sign(np.dot(midpoint-t, n))*n*1700
            p_i = np.array([midpoint[0],midpoint[1]])  # x,y     # vertices infinitos de voronoi
            line2 = np.vstack((p_f,p_i))
            continuacion_poly_points = []
            begin_end = []

            for (_0,_1) in zip(np.array(self.poly_points),np.array(self.poly_points_shift)):
                line1 = np.vstack((_0,_1))
                intersection = self.measures.line_intersection(line1,line2)

                continuacion_poly_points.append(_0)

                if self.poly_extended.contains(geometry.Point(intersection)):
                    continuacion_poly_points.append(intersection)
                    begin_end.append(intersection)

            polinomios = self.measures._2_voronoi(begin_end,continuacion_poly_points)

            for en,po in enumerate(polinomios):
                pts = np.array(po).reshape((-1,1,2))
                if en==0:
                    cv2.polylines(image,[pts],True,(0,255,0))
                else:
                    cv2.polylines(image,[pts],True,(0,0,255))

                hull = ConvexHull(po)

                cx = np.mean(hull.points[hull.vertices,0])
                cy = np.mean(hull.points[hull.vertices,1])
                polygons.append(hull.volume)
                polygon_area += hull.volume
                polygon_number+=1
                cv2.putText(image, str(polygon_number), (round(cx-10),round(cy+10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)

        elif rec_points.shape[0] > 2:
            rec_points = np.flip(rec_points)
            vor = Voronoi(rec_points)

            new_regions, new_vertices = self.measures.n_voronoi(vor)

            new_vertices = np.asarray(new_vertices)
            box = geometry.Polygon(self.poly_points)
            for region in new_regions:
                polygon = new_vertices[region]

                # Clipping polygon
                poly = geometry.Polygon(polygon)
                poly = poly.intersection(box)
                polygon = [[p[0],p[1]] for p in poly.exterior.coords]

                pts = np.array(polygon).reshape((-1,1,2))
                cv2.polylines(image,np.int32([pts]),True,(0,255,0))

                hull = ConvexHull(polygon)

                cx = np.mean(hull.points[hull.vertices,0])
                cy = np.mean(hull.points[hull.vertices,1])
                polygons.append(hull.volume)
                polygon_area += hull.volume
                polygon_number+=1
                cv2.putText(image, str(polygon_number), (int(round(cx-10)),int(round(cy+10))), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)


        avg_density = float(original_area/rec_points.shape[0])
        print('AVERAGE DENSITY =', avg_density, 'passengers/m2')

        cv2.imwrite(output_variable,image)
        workbook = xlsxwriter.Workbook(output_variable.split('.')[0]+'.xlsx')
        worksheet = workbook.add_worksheet()

        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 35)

        worksheet.write('A1', 'Polygon Areas in m2')
        worksheet.write('A2', 'Polygon Area = ')
        worksheet.write('A3', 'Average Density = ')
        worksheet.write('B2',str(original_area))
        worksheet.write('B3',str(avg_density))
        worksheet.insert_image('C2', output_variable)

        A = 4
        for c,p in enumerate(polygons):
            print('Polygon '+str(c+1)+ ' Area = ' + str(self.measures.Area_Voronoi(polygon_area,p))+' m2')
            worksheet.write('A'+str(A), 'Polygon '+str(c+1)+' Area = ')
            worksheet.write('B'+str(A),str(self.measures.Area_Voronoi(polygon_area,p)))
            A+=1

        workbook.close()
        cv2.imshow('Area selection',image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
