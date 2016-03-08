import GliderV2



# The point of this program is to see how a glider itself would react in air. It works by taking a list of all the arguments and then updating them by piece by piece.

# Variables to be updated : velocity in all three dimensions.

# We have three forces acting on our glider - weight, lift and drag. For convenience, we ignore how the
# components influence each other aerodynamically - we just pretend they are are stuck together and independent
# of each others airstream.

# for now, We are only taking the moment of force.

def update(i):

    
