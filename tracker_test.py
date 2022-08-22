import cv2
import sys
from random import randint

#(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

if __name__ == '__main__' :

    tracker = cv2.TrackerCSRT_create()

    # Read video
    #video = cv2.VideoCapture("D:\git\PostStabilUI\MLS/Main(2)_2022_08_10_18_55_21.mp4")
    video = cv2.VideoCapture("C:/Users/4Dreplay/Downloads/Main(2)_2022_08_19_20_13_00.mp4")
    
    start = 240
    
    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()


    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print('original size: %d, %d' % (width, height))


    video.set(cv2.CAP_PROP_POS_FRAMES, start)
    
    ok, frame = video.read()
    frame = cv2.resize(frame, (1920,1080), fx =0, fy=0, interpolation=cv2.INTER_AREA)
    
    
    
    if not ok:
        print('Cannot read video file')
        sys.exit()
    
    # Define an initial bounding box
    bboxes=[]
    colors=[]
    
    while True:
        bbox = cv2.selectROI('MultiTracker', frame)
        bboxes.append(bbox)
        colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
        print("Press q to quit selecting boxes and start tracking")
        print("Press any other key to select next object")
        k = cv2.waitKey(0) & 0xFF
        if (k == 113):  # q is pressed
            break

    print('Selected bounding boxes {}'.format(bboxes))
    
    multiTracker = cv2.MultiTracker_create()
    
   
    
    #multiTracker.add(algorithms, frame,objects)
    for bbox in bboxes:
        print (bbox)
        multiTracker.add(cv2.TrackerCSRT_create(), frame, bbox)
        
        
    while video.isOpened():
        success, frame = video.read()
        frame = cv2.resize(frame, (1920,1080), fx =0, fy=0, interpolation=cv2.INTER_AREA)
        if not success:
            break

        # get updated location of objects in subsequent frames
        success, boxes = multiTracker.update(frame)
     
        # draw tracked objects
        for i, newbox in enumerate(boxes):
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
            

        # show frame
        cv2.imshow('MultiTracker', frame)

        # quit on ESC button
        if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
            break
        
    
    
    
    
    
    
    
    
    # bbox = (287, 23, 86, 320)

    # # Uncomment the line below to select a different bounding box
    # bbox = cv2.selectROI(frame, False)

    # # Initialize tracker with first frame and bounding box
    # ok = tracker.init(frame, bbox)

    # while True:
    #     # Read a new frame
    #     ok, frame = video.read()
    #     if not ok:
    #         break
        
    #     # Start timer
    #     timer = cv2.getTickCount()

    #     # Update tracker
    #     ok, bbox = tracker.update(frame)

    #     # Calculate Frames per second (FPS)
    #     fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

    #     # Draw bounding box
    #     if ok:
    #         # Tracking success
    #         p1 = (int(bbox[0]), int(bbox[1]))
    #         p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    #         cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
    #     else :
    #         # Tracking failure
    #         cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    #     # Display tracker type on frame
    #     cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
    
    #     # Display FPS on frame
    #     cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

    #     # Display result
    #     cv2.imshow("Tracking", frame)

    #     # Exit if ESC pressed
    #     k = cv2.waitKey(1) & 0xff
    #     if k == 27 : break
