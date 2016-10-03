import uvc
import logging
import cv2
logging.basicConfig(level=logging.DEBUG)
from time import time,sleep
from datetime import datetime
import os
import numpy as np

# print (uvc.is_accessible(0))
dev_list = uvc.device_list()
print "Compatible devices found:\n\t" + str(dev_list)
cam_uid = ''
for d in dev_list:
    if d['name'] == "USB 2.0 Camera":
        cam_uid = d['uid']
if cam_uid == '':
    print "No compatible cameras found, exiting :("
    exit()
cap = uvc.Capture(cam_uid)
for c in cap.controls:
    # if 'Focus' in c.display_name:
    #     c.value = c.def_val
    if 'Auto Exposure Mode' in c.display_name:
        c.value = c.def_val
    # if 'Absolute Exposure Time' in c.display_name:
    #     c.value = c.def_val
    print "{} = {} {} (def:{}, min:{}, max:{})".format(c.display_name, str(c.value), str(c.unit), str(c.def_val), str(c.min_val), str(c.max_val))
print cap.name + " has the following available modes:\n\t" + str(cap.avaible_modes)
cap.print_info()

modes = []
for m in cap.avaible_modes:
    if m[2] == 60:
        modes.append(m)
cap.frame_mode = modes[0]  # Choose biggest size with 60fps
cap.frame_mode = cap.avaible_modes[np.argwhere(np.array(cap.avaible_modes)[:,2]>=60)[0]]

VIDEO_FOLDER = "img_test"
if os.path.exists(VIDEO_FOLDER):
    for f in os.listdir(VIDEO_FOLDER): os.remove(os.path.join(VIDEO_FOLDER, f))
else:
    os.makedirs(VIDEO_FOLDER)

tt = datetime.now()
for x in range(100):
    # frame = cap.get_frame_robust()

    for a in range(4):
        try:
            frame = cap.get_frame_robust()
        except uvc.CaptureError as e:
            # print 'DEBUG - Could not get Frame. Error: "%s". Tried %s time(s).'%(e.message,a+1)
            pass
        else:
            # print 'DEBUG - Successfully got frame {:d} after {:d} tries'.format(frame.index, a+1)
            break

    # cv2.imshow("img", frame.bgr)
    # y,u,v = frame.yuv422
    # cv2.imshow("u",u)
    # cv2.imshow("v",v)
    t = datetime.now()
    # cv2.waitKey(1)
    cv2.imwrite(os.path.join(VIDEO_FOLDER, "test_" + str(frame.index) + ".jpg"), frame.img)
    # cv2.imwrite(os.path.join(VIDEO_FOLDER, "test_" + str(frame.index) + ".jpg"), cv2.resize(frame.img, None, fx=0.5, fy=0.5))
    t2 = datetime.now()
    print "At t={} ({}) picture #{:03d} was taken; deltaT={:6.2f}ms ({:6.2f}ms + {:6.2f}ms)".format(t, frame.timestamp, frame.index, (datetime.now()-tt).total_seconds()*1000, (t2-t).total_seconds()*1000, (t-tt).total_seconds()*1000)
    tt = datetime.now()
#       # print frame.img.shape,x
    # cap.frame_mode = (1280,720,30)
#   for x in range(3):
#       frame = cap.get_frame_robust()
#       frame.img
#       cv2.imshow("img",frame.gray)
#       # cv2.imshow("u",u)
#       # cv2.imshow("v",v)
#       # sleep(.1)
#       cv2.waitKey(1)
#       # print frame.img.shape,x

cap = None
exit()

