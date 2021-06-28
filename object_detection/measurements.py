import numpy as np

class Measurements(object):
    def __init__(self,gt_pol):
        self.gt_pol = gt_pol

    def iou(self,bb_test,bb_gt):
        xx1 = np.maximum(bb_test[0], bb_gt[0])
        yy1 = np.maximum(bb_test[1], bb_gt[1])
        xx2 = np.minimum(bb_test[2], bb_gt[2])
        yy2 = np.minimum(bb_test[3], bb_gt[3])
        w = np.maximum(0., xx2 - xx1)
        h = np.maximum(0., yy2 - yy1)
        wh = w * h
        o = wh / ((bb_test[2]-bb_test[0])*(bb_test[3]-bb_test[1])
          + (bb_gt[2]-bb_gt[0])*(bb_gt[3]-bb_gt[1]) - wh)
        return(o)

    def Area_Voronoi(self,hull_pol,hull_pol_mini):
        return(float(self.gt_pol*hull_pol_mini/hull_pol))

    def line_intersection(line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return(a[0] * b[1] - a[1] * b[0])

        div = det(xdiff, ydiff)
        if div == 0:
           return([-100,-100])

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return([x, y])
