# Running the Problem
## To run with the pretrained model
* Run the notebook `problems/p5/solution.ipynb`
## To train your own model
* Run `python problems/p5/train.py` to train a model for 200 epochs
   * Note that this does not save the model. It is only for demostration
* Run the notebook `problems/p5/solution.ipynb`


# Output

Running the last cell in `problems/p5/solution.ipynb` will display a UI of a pretrained model balancing the pole on the cart until the pole falls to an irrecoverable angle or moves off of the screen. Running the `problems/p5/train.py` file will display a UI of a model being trained on 200 epochs to demonstrate the learning of the reinforcement model.