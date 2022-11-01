# To run the problem with our pretrained models for the pretrained(c) and untrained(a,b) problems aka prepretrained/pretrained models
1. `python a.py`
2. `python b.py`
3. `python c.py`
# To train the models yourself
*If you want to train the models uyou will need a nvidia cuda capable gpu and then pytorch with cuda, tensorflow 2.10.0, Nvidia CUDA 11.X, Nvidia CuDnn 8.X for CUDA 11.X*
1. Using powershell or cmd, run
    * `c-retrain-yolo.bat` for the model for c
    * `b-train-yolo-fresh.bat` for the model for b
    * `python a-train-imageai.py` for the model for a
2. Run
    1. `python a.py`
    2. `python b.py`
    3. `python c.py`

# Output
* For b and c
    * Output classified images are in `output/<problem letter>-<algorithm name>-<model context>`
    * The 10 original images are in `dataset/test/images`
* For a
    * The image classes are displayed in the output of `python a.py`