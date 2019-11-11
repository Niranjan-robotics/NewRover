# NewRover
1. For rover main script : run roverMainscript.py

	This listens to distance channel and controls rover.
	It keeps moving rove rforward alway until distance is less then x(20mm etc).Stops and turns right and move forward.
	Servoe also activated to look up/down.
2.make sure to run distance.py. as input to step 1.
3.snowboy hotward detection:
	3.1.python2 :go to : /home/pi/projects/NewRover/snowboy (this is alway running to listen hotward and call publisher)
		run hotwordTest.py - this works only on python2 due to snoboy limitation.
	3.2.python3: On detection of hotward -> it launches publishMsg.py under "/home/pi/projects/NewRover"
		This will just publish voice true message to voice mqtt channel and closes.
	3.3.python3: continus running of voiceClient under "/home/pi/projects/NewRover".
		This keeps listening to voice mqt channel for hotword detection.
		If true - this should launch speech_To_Text.py under "/home/pi/projects/NewRover/snowboy/SpeechToText"
		The returned text is re published to voice mqtt channel that will be listend by mainscript step1.
		step1 should get (left/right/stop/back/go/followme/get something etc ) messages and control the rover.
		since snowboy is in python2 and mqtt and subprocess.run in python3,unable to simplify 3.1/2/3 steps.
	Notes: make sure during 3.2 true - any other hotwords should be skipped. led should tun on saysing that it is busy with current job.
	       When speechtotext is ready -blink 2nd led on- and block all other messages until job is done.
	       Published message should also reset all leds and flags to default for next voice command.
