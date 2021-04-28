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
