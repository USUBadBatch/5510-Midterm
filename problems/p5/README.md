# Initialize Problem

If you haven't already, run `pip install -r requirements.txt`.

# Running the Problem
1. Training your own model
   * Run `python problems/p5/train.py` to train a model for 200 epochs
      * Note that this does not save the model. It is only for demostration
2. The entire solution set for the problem is contained within the `problems/p5/solution.ipynb` notebook.
   * `problems/p5/solution.ipynb` runs 1 epoch of the pretrained model `policy_cnn.pt` to demonstrate the reinforcement learning model's success

# Output

Running the last cell in `problems/p5/solution.ipynb` will display a UI of a pretrained model balancing the pole on the cart until the pole falls to an irrecoverable angle or moves off of the screen. Running the `problems/p5/train.py` file will display a UI of a model being trained on 200 epochs to demonstrate the learning of the reinforcement model.