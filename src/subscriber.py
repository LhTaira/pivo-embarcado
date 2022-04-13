from paho.mqtt import client as mqtt_client
import random
import time
import lanes
import cv2
import threading
import copy
import sys

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Connected to MQTT Broker!')
        else:
            print('Failed to connect, return code %d\n', rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def mainOffroad():
  global keep_running_video
  cap = cv2.VideoCapture(filename)

  fourcc = cv2.VideoWriter_fourcc(*'mp4v')

  result = cv2.VideoWriter(output_filename, fourcc, output_frames_per_second, file_size) 

  while cap.isOpened():
    success, frame = cap.read()
    if success and keep_running_video:
      print(keep_running_video)
      width = int(frame.shape[1] * scale_ratio)
      height = int(frame.shape[0] * scale_ratio)
      #x,y,h,w = 50, 350, height-600, (width-150)
      #frame = frame[y:y+h, x:x+w]
      #frame = cv2.resize(frame, (width-150, height-600))
      #blur = cv2.blur(frame, (20, 15))

      original_frame = frame.copy()

      lane_obj = lanes.Lane(orig_frame=original_frame)
      lane_line_markings = lane_obj.get_line_markings()
      lane_obj.plot_roi(plot=False)

      warped_frame = lane_obj.perspective_transform(plot=False)

      histogram = lane_obj.calculate_histogram(plot=False)	
     
      left_fit, right_fit = lane_obj.get_lane_line_indices_sliding_windows(
        plot=False)

      lane_obj.get_lane_line_previous_window(left_fit, right_fit, plot=False)
      frame_with_lane_lines = lane_obj.overlay_lane_lines(plot=False)
      lane_obj.calculate_curvature(print_to_terminal=False)
      lane_obj.calculate_car_position(print_to_terminal=False)
      frame_with_lane_lines2 = lane_obj.display_curvature_offset(
        frame=frame_with_lane_lines, plot=False)
      result.write(frame_with_lane_lines2)

      #cv2.imshow('Frame', frame_with_lane_lines) 
      print('sok')

      if (cv2.waitKey(25) & 0xFF == ord('q')) or not keep_running_video: 
        print('fok1')
        break
    else:
      print('fok2')
      break
	
  cv2.destroyAllWindows()
  cap.release()
  result.release()


def on_message(client, userdata, msg):
  global keep_running_video
  #global vision_thread
  message = msg.payload.decode()
  vision_thread = threading.Thread(target=mainOffroad)
  print(f"Received `{message}` from `{msg.topic}` topic")
  if message == 'sthap':
    keep_running_video = False
    vision_thread = threading.Thread(target=mainOffroad)

  if message == 'goh':
    if not keep_running_video:
      keep_running_video = True
      vision_thread.start()


filename = '../Mazda CX-30 Off-Road_ Soapstone Basin Drive (dashcam clips).mp4'
file_size = (1920,1080) 
scale_ratio = 1 

output_filename = 'orig_lane_detection_1_lanes.mp4'
output_frames_per_second = 60.0 

broker = 'broker.emqx.io'
port = 1883
topic = '/python/fokson'
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'

keep_running_video = False

#vision_thread = threading.Thread(target=mainOffroad)

mqtt_client = connect_mqtt()

mqtt_client.subscribe(topic)
mqtt_client.on_message = on_message
    
mqtt_client.loop_forever()
