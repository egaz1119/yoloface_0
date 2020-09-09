while true	
do
python3 take-photo.py
	for i in `seq 1  11`
	do
	python3 yoloface-edit.py --image /home/pi/workspace/yoloface-master/inputs/$i.jpg --output-dir outputs/
	python3 aws-upload.py 
	done
done
