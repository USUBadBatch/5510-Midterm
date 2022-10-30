# Initalize Problem
1. `git submodule init`
2. `git submodule update`
3. `pip install -r algorithms/yolov5/requirements.txt`
# To run the problem with the pretrained (pretrained and untrained -> prepretrained/pretrained) models
1. `python a.py`
2. `python b.py`
3. `python c.py`
# To train the models yourself
1. Using powershell or cmd, run
    * `c-retrain-yolo.bat` for the model for c
    * `b-train-yolo-fresh.bat` for the model for b
    * `` for the model for a
2. Run
    1. `python a.py`
    2. `python b.py`
    3. `python c.py`

# Output
* Output classified images are in `output/<problem letter>-<algorithm name>-<model context>`
* The 10 original images are in `dataset/test/images`