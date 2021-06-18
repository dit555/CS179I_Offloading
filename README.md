# CS179I_Offloading
## Abstract:
In our project we focus on offloading a hardware intensive task to a server with powerful hardware. This allows us to do tasks which would require a powerful computer on a weaker device such as a mobile phone. We use this to make tasks such as deep learning work in real time.  
## Introduction:
We created an application which will find a human face in a video feed and overlay a filter on the face. To do this, we first need to find a face in the frame of a video. This is a computationally intensive task which requires powerful hardware to work in real time. However, most of our users do not have powerful hardware to run the program without major slowdowns.  
To deal with this we take a frame from the video and send it to a server with powerful hardware. Then we run our facial recognition algorithm and send back the superimposed image to the user.
## Related Works:
  * Snapchat
  * Facebook
  * Instagram  
 
The applications mentioned above all use some type of computer vision to identify objects and obstacles. Snapchat, for example, uses image processing which transforms an image by performing mathematical operations. First, they do face detection, which we also do. For a given video frame, we detect human faces and output the coordinates of the faces. Second, they do facial landmarks, which we also did, but we extracted the face, rather than other components such as nose, eyes, lips. Basically, this step is to extract facial features. The last step is the image processing part. However, in addition to image processing, Snapchat also uses an active shape model. It is a model that has been trained by manual marking of the facial feature borders on hundreds and thousands of images. For our project, we used a different model. The difference between our product and Snapchat is that we did the heavy computing in the web server, as well as storing data. Facebook, on the other hand, uses cloud computing. People can update and access photos anywhere in the globe as long as they have a connection to the Internet. As for Instagram, they also use cloud computing, The photos and profiles are stored in the cloud as well as photo editing options. Our solution is similar to Facebook and Snapchat, even though we weren’t able to completely deploy our application. Instead of using the http module, we used plain socket programming for the communication between client and server.   
## Design:
![Design](https://user-images.githubusercontent.com/56750709/122493549-c01e6f80-cf9c-11eb-8711-1cf0290afdfb.png)  
### Ideal Conditions:
Our system works the best when the user has a fast internet connection. This increases the file transfer rate which lowers the latency when sending and receiving data from the cloud.  
## Milstones:
|  Features | Justifications |
|---|---|
|  Camera | We needed the camera to capture the images so that it could be sent to the server  |
|  Dataset | We acquire and label our data set for training the model.  |
| Training the model  | We use our labeled dataset to train our facial detection model.  |
| Sending data to cloud (client and server)  | We needed this feature to send the data to the cloud, so that face recognition engine could run those images.   |
|  Sending data from cloud (client and server) | We needed this feature to return the resulted data to the client machine  |
| Superimpose  | We need to apply the filter to the location of the user’s face.  |
## Testing and Results:
![Superimposed image](https://user-images.githubusercontent.com/56750709/122495374-c57cb980-cf9e-11eb-9e4c-37e017e381e3.PNG)  
In this project our goal is to offload the findface process onto the cloud. We had some difficulties creating a fully functioning server and had to use sockets instead. Unfortunately, this came with the side effect of being unable to send the overlaid images on the server back to the user. This is because exposing an ip address on windows is non trivial, so we could not run a server on the local machine to receive the results.  
As a result, the only way to see the overlaid images from the server is to upload them to an external service and download them on our local machine to view the images one at a time. In this respect we failed to fully offload the task. However, we were still able to run these programs on the cloud and benchmark them.
|   | Average fps  | Total Run time (1000 iterations)  |
|---|---|---|
| Local  | 16  | 56 s  |
| Offloading  | 61  | 16 s  |

Based on these results findface took approximately 4 times longer to run on a local machine <sup>1</sup> verses the cloud machine <sup>2</sup>.. When the local machine is a cell phone the increase in speed will be even higher. To achieve the results for the local machine we run findfaceBenchmark.py on our local machine. We run it multiple times with 0,1, and 2 faces in the image.  
We also had some issues with the overlaying process. When the user is within the bounds of the webcam frame it overlays the image onto the user's face. We can see on the image above that there are borders on the filter even though the borders of the face should be transparent.  
This is because the numpy (the library we were using to store the image) cannot understand transparent images. Fixing this would require complex algorithms which are outside of the current scope of the project.

<sup>1</sup> : Local Machine is using only an Intel i7-8550U @2.0 GHz processor and has no gpu resources.  
<sup>2</sup> : Cloud Machine using: two ten-core (8 threads/core) IBM POWER8NVL CPUs at 2.86 GHz and 	
Two NVIDIA GP100GL (Tesla P100 SMX2 16GB) GPUs  

## Implementation:
We accomplished this by using opencv-python to capture webcam footage, find the user’s face, and overlay the image onto the video feed. We also used Cloudlab as our server to enable us to do the hardware intensive tasks. To send frames to and from the cloud we used simple socket programming.  
### File descriptions (path from github directory home):
#### Me_gusta_filter.jpg:
* The facial recognition model.
#### Data.xml:
* Opens a webcam
* Reads a frame from the webcam
* Uses facial recognition model to face coordinates
* Overlays filter onto user’s face(s)
* Press ‘q’ to terminate program
#### FindFace.py:
* Runs 100 iterations of FindFace.py then terminates.
* Prints fps each iteration (one iteration is a cycle of reading a frame, finding the face, then overlaying it).
* Prints time to run and average fps upon termination.
#### FindFaceBenchmark.py:
* Runs 100 iterations of FindFace.py then terminates.
* Prints fps each iteration.
* Prints time to run and average fps upon termination.
#### Benchmark_cloud/findface_cloud.py:
* Finds most recent frame in the folder with frames
* Reads most recent frame
* Runs FindFaceBenchmark on most recent frame
#### Benchmark_cloud/new_server.py:
* Creates server that receives files from client
* Saves received frames to a folder.
#### Benchmark_cloud/new_client.py:
* Reads frames from webcam
* Sends frames to Benchamrk_cloud/new_server.py

#### cloud/client.py:
* Reads frames from webcam
* Sends frames to Benchamrk_cloud/new_server.py
* Creates server that receives files from client
* Saves received frames to a folder.
#### cloud/server.py:
* Reads most recent file received by server
* Runs findFace on recent file
* Overlays image and writes it to a new file
#### cloud/findface_cloud.py:
* Reads most recent file received by server
* Runs findFace on recent file
* Overlays image and writes it to a new file
#### cloud/send_client.py:
* Sends overlaid image file to server on users machine
#### cloud/recieved_server.py:
* Receives overlaid image from send_client
* Saves image to a folder

