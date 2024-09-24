Build and train notebook can be used to setup the model in an .h5 file, already trained.
This will work given the dataset is stored in the folder TestDataset/handsign_#, with all the videos for that handsign stored there, and all handsigns containing the same ammount of videos.
Also, the parameters on the first section of the notebook need to be adjusted accordingly before executing anything. The number of frames indicate the number of equidistant frames to be taken from the dataset videos (not the number of frames the videos have). This number should not be longer than the number of frames the videos have.

In the Landmark visualization folder you will find a scrit that takes the landmarks extracted from the dataset videos and shows you in an .mp4 file output how any one video's landmarks look like. 
This is to manually ensure the landmarks are being captured correctly before training on a big dataset.


dataset we are currently using was obtained from here: https://facundoq.github.io/datasets/lsa64/

PYTHON VERSION INSTALLED NEEDS TO BE 3.12 FOR THIS TO WORK


How to set up:
-
download dataset from https://facundoq.github.io/datasets/lsa64/ 
put them in the TestDataset folder following the structure
    
TestDateset (folder)
-
        -handsign_1 (subfolder)
        -handsign_2 (subfolder)
        -handsign_3 (subfolder)
and so on

Also dont forget to modify the data shape parameters on the first cell of the building-and-training.ipynb notebook so it matches the dataset being used.

To install dependencies
-
open a cmd on the root folder and (having python already installed on your system) type "pip install -r .\requirements.txt"
this should install all necessary dependencies for the project.

if this doesn't work try doing a "pip install pipreqs" on the same cmd and then going back to the first command
