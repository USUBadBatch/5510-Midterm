To run this program you can simply give the command `python a.py` from inside this directory.  The output will be shown in RESULTS.md

The questions are answered here in this README

•Which planner provided a path with the lowest cost on average?
The path with the lowest peak memory cost was RRT-Star.

•Which one found a path the fastest on average?
The fastest on average was Dijkstra's algorithm.

•After comparing your planner to these five other ones is there anything you
would change in your planner to help it converge faster or find a path with a
better cost?
Yes, there is a lot of optimization to be done on our algorithm.  It performs very slow in comparison with the other algorithms.  I'm sure that there is a way to cut down the number of FLOPS among other things to get this to run faster.

•Which planner appears to be the best overall? Which planner would you use
for a robot in a complex environment?
We would have to say the Bidirectional A* performed the best.  It had a pretty low time and the max memory was better than the standard A*.  We really like this one because it's quite fast and we don't have to provide a lot of memory. Whereas the Dijkstra algoritm is omnicient and may try more than is necessary.