Make sure to check latest updates if edgetpu fails: 

https://www.tensorflow.org/lite/guide/python#install_just_the_tensorflow_lite_interpreter 

----------- install steps ------------

Cd coral  

Coral$ pip3 install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl 

 

mkdir coral && cd coral git clone https://github.com/google-coral/tflite.git  

Download the bird classifier model, labels file, and a bird photo: 
----------------------------------------
cd tflite/python/examples/classification  

bash install_requirements.sh 

 

Test if same will work: 
--------------------------------

cd tflite/python/examples/classification

python3 classify_image.py --model /home/pi/projects/NewRover/all_models/niranjan_model_edgetpu.tflite --labels /home/pi/projects/NewRover/all_models/niranjan_labels.txt --input /home/pi/projects/NewRover/all_models/Niranjan/65.jpg 

Working image: 

pi@raspberrypi:~/projects/NewRover/tflite/python/examples/classification $ 
python3 classify_image.py --model /home/pi/projects/NewRover/all_models/niranjan_model_edgetpu.tflite --labels /home/pi/projects/NewRover/all_models/niranjan_labels.txt --input /home/pi/projects/NewRover/all_models/Niranjan/65.jpg  

----INFERENCE TIME---- 

Note: The first inference on Edge TPU is slow because it includes loading the model into Edge TPU memory. 

5.3ms 

2.1ms 

2.1ms 

5.9ms 

2.3ms 

-------RESULTS-------- 

Niranjan: 0.98438 

 

-------RESULTS-------- 

Niranjan: 0.98438 