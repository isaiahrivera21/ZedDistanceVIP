import cv2
import pyzed.sl as sl
import math 
from blue_blob import blob_detection

def main():
    init = sl.InitParameters()
    cam = sl.Camera()
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print("Camera Open : "+repr(status)+". Exit program.")
        exit()
    
    runtime = sl.RuntimeParameters()
    image = sl.Mat() 
    depth = sl.Mat()
    point_cloud = sl.Mat()
    win_name = "Camera Control"
    cv2.namedWindow(win_name)
    key = ''
    while key != 113:  # for 'q' key
        err = cam.grab(runtime) 
        if err == sl.ERROR_CODE.SUCCESS: # Check that a new image is successfully acquired
            cam.retrieve_image(image, sl.VIEW.LEFT) # Retrieve left image
            cam.retrieve_measure(depth,sl.MEASURE.DEPTH)
            cam.retrieve_measure(point_cloud,sl.MEASURE.XYZRGBA)
            # cvImage = mat.get_data() # Convert sl.Mat to cv2.Mat
            cvImage = image.get_data()
            cvDepth = depth.get_data()
            cvPoint = point_cloud.get_data()

            x,y = blob_detection(cvImage)

            err, pointCloudVal = point_cloud.get_value(x,y)

            x_p = pointCloudVal[0]
            y_p = pointCloudVal[1]
            z_p = pointCloudVal[2]

            #Find distance using Euclidean distance (in mm)
            distance = math.sqrt(x_p * x_p +
                     y_p * y_p +
                     z_p * z_p)


            center_coords = (x,y)
            radius = 1
            color = (255,0,0)
            thickness = 8
            cvPoint2 = cv2.circle(cvPoint, center_coords, radius, color, thickness)





            # point cloud returns 4 values 
            # x,y,z,color
            # 

            
            # print(distance) 
            text = str(distance)
            text2 = "STOP"
  
            # font 
            font = cv2.FONT_HERSHEY_SIMPLEX 
            
            # org 
            org = (00, 185) 
            
            # fontScale 
            fontScale = 1
            
            # Red color in BGR 
            color = (255, 0, 0) 
            
            # Line thickness of 2 px 
            thickness = 2

            cvPoint2 = cv2.putText(cvPoint2, text, org, font, fontScale, 
                  color, thickness, cv2.LINE_AA, False)
            if(distance < 600):
                cvImage = cv2.putText(cvImage, text2, (300,500), font, 12, 
                  (0,0,255), 6, cv2.LINE_AA, False)
                print("STOP")


            cv2.imshow("IMAGEE", cvImage) #Display image
            # cv2.imshow(win_name, cvDepth) #Display image
            cv2.imshow(win_name, cvPoint2)
        else:
            print("Error during capture : ", err)
            break
        
        key = cv2.waitKey(5)
        # Change camera settings with keyboard
        # update_camera_settings(key, cam, runtime, mat)
    cv2.destroyAllWindows()

    cam.close()


if __name__ == "__main__":
    main()
