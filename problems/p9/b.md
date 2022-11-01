(5 points) Isaac Asimov listed 3 laws of robotics, comment on the algorithmic com-
plexity of implementing these into working intelligence. Define a scenario and write
Psuedo code to implement these rules.

The three rules of robotics and given by Isaac Asimov as stated in ```Asimov’s “Three Laws of Robotics” and Machine Metaethics```
 by Susan Leigh Anderson 
1. A robot may not injure a human being, or,
through inaction, allow a human being to come to
harm.
2. A robot must obey the orders given it by human
beings except where such orders would conflict
with the First Law.
3. A robot must protect its own existence as long as
such protection does not conflict with the First or
Second Law. (Asimov 1984) 

In order for a robot to follow these rules there would need to be some sort of model in place to give the go-ahead or to inhibit certain behaviors.  The complexity for training this model would need to be very large as to incorporate the various scenarios where the same action could be determined to be proper or improper.  However, once that model was trained the complexity of running that model would only be as complex as taking in the inputs of the surroundings and predicting if a behavior would comply with these robotic laws.  

A scenario where the robot would need to follow the first rule would be if the robot were cutting potatoes.  In order to not hurt anyone, motions would need to be small as to not danger anyone in the direct vicinity but large enough to cut the potatoe.  The robot would also need to know that large chunks of food can be a choking hazard, especially to small children and would need to prepare the food accordingly.  This way the robot would not injure anyone through acts of commission or omission. 

A case where the robot would need to disobey an order if it would cause harm would be in the case of a family with multiple children.  As most older children like to tease and scare their little siblings.  Under most circumstances the robot would be inclined to follow the orders of the children.  However, if the robot was told to pick up small child and place them on the road of a busy street, the robot would need to know that this would cause harm and that order would need to be disobeyed in order to comply with these laws.  

A possible situation where the robot would need to have self preserving behaviors would be in the ocean.  The robot would need to know to avoid certain animals and boats alike.  If the robot knows a boat is coming in its direction it would need to know that it should move.  However, if doing this would cause a forceful collision with an individual, or the robot was ordered not to move, the robot would need to have the awareness to not move.

Psuedo Code:


while true

    detect_surroundings
    if order given by human
        if order safe to all humans
            perform action to comply with order
        else
            reject order
    else if dangerous element in environment
        if any human in danger
            perform action to save human
        else if self in immediate danger
            calculate possible action
            while possible action puts human in danger
                get new possible action
            end while loop
            perform action
        else
            monitor dangerous element
        end else if 
    else
        maintain current action until completion
        if task and action completed
            wait/rest
        end if
    end else if 
end while loop

