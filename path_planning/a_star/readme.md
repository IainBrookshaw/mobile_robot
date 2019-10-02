# A* Path Planner

This is the implementation of the popular A* path planner for the grid-map
context

## Conventions

As this is intended for a gridmap, we exploit the following conventions:
1. maps are represented my `numpy.array`s
2. because of this, data is organized in `[row, col]` order, _not_ `[x,y]` order
    - [rows, cols] start at the top left and continue to bottom right
3. gridmap cells are floats [0,1], with 0.0 == open space and 1.0 == fully closed obstacle