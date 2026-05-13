class Folow_Point:

    def __init__(self,horitzonal_PID,vertical_PID):
        self.verticalKP = vertical_PID[0]
        self.verticalKI = vertical_PID[1]
        self.verticalKD = vertical_PID[2]

        self.horitzonalKP = horitzonal_PID[0]
        self.horitzonalKI = horitzonal_PID[1]
        self.horitzonalKD = horitzonal_PID[2]
        self.vertical_error = 0
        self.past_vertical_error = 0
        self.horitzonal_error = 0
        self.past_horitzonal_error = 0
        self.total_error = 0

    def follow(self,desired_point,ROI):
        """
        0,0  0,1  0,2  0,3  0,4
        1,0  1,1  1,2  1,3  1,4
        2,0  2,1  2,2  2,3  2,4 .  .  .
        3,0  3,1  3,2  3,3  3,4
        4,0  4,1  4,2  4,3  4,4
                   .
                   .
                   .
        """
        #calculate center of ROI
        centerofROI = ((ROI[0] + ROI[2]) / 2), ((ROI[1] + ROI[3]) / 2)
        #calculate horitzonal and vertical error
        self.vertical_error = desired_point[0] - centerofROI[0] #if value "+" up , if value "-" go down
        self.horitzonal_error = desired_point[1] - centerofROI[1] #if value "+" left , if value "-" go right


        #calculate vertical speed
        ver_P = self.vertical_error * self.verticalKP
        ver_I = self.vertical_error * self.verticalKI
        ver_D = (self.past_vertical_error - self.vertical_error) * self.verticalKD

        #another part
        self.past_vertical_error = self.vertical_error
        
        vertical_speed = ver_P + ver_I + ver_D

        #calculate horitzonal speed
        hor_P = self.horitzonal_error * self.horitzonalKP
        hor_I = self.horitzonal_error * self.horitzonalKI
        hor_D = (self.past_horitzonal_error - self.horitzonal_error) * self.horitzonalKD

        #another part
        self.past_vertical_error = self.vertical_error
        
        vertical_speed = ver_P + ver_I + ver_D