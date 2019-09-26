# Readme: Differential Drive Robot Odometry

## Summary
    This is a simple example of a Differential Drive Robot odometry. The motion 
of the differential drive robot is modeled accurately for the ground truth data,
then modeled with noisy wheel velocity readings to illustrate the real-world
limitations of this approach.

The simulation is via Python & Matplotlib and allows for user interactions to 
"drive" the robot around the 2D simulation plane 

For full mathematical background, see `report`
    - you will need LaTeX to build this; `pdflatex` or `xelatex` are recommended

# Install
You will need:
    - python-3.5 or higher
    - virtualenv or similar

```bash
virtualenv -p python3 /tmp/diff-drive-sim # or whichever path suits :)
source /tmp/diff-drive-sim/bin/activate

python3 -m pip install diff_sim
diff_simulation.py # use '--help' for more information
```
