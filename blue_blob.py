import cv2
import numpy as np

CONF_THRESH = 1 


def blob_detection(frame):
    # Convert the frame to grayscale
    x = 0
    y = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    params = cv2.SimpleBlobDetector_Params()
 
    # Filter by circularity
    params.filterByCircularity = True
    params.minCircularity = 0.2

    # params.filterByInertia = False; 
    # params.filterByConvexity = False; 
 
    detector = cv2.SimpleBlobDetector_create(params)
 
    # Um not sure how to only pick out one blob or the "relevant blob"
    keypoints = detector.detect(gray)


    for keypoint in keypoints:
        # print(keypoint.response, keypoint.size)
        # if keypoint.response > CONF_THRESH:
        x, y = map(int, keypoint.pt)
        # else: 
        #     x = 0
        #     y = 0
 
    print(x,y)
 
    # Draw circles around detected blobs
    result_frame = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow("Blob Detection", result_frame)
 
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    # cap.release()
    # cv2.destroyAllWindows()
 
    return x,y
 
# if __name__ == "__main__":
#     cap = cv2.VideoCapture(0)
 
#     while True:
#         ret, frame = cap.read()
 
#         if not ret:
#             break
 
#         result_frame = blob_detection(frame)
 
#         cv2.imshow("Blob Detection", result_frame)
 
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
        
#     cap.release()
#     cv2.destroyAllWindows()
 