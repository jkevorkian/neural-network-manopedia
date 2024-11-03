Build and train notebook can be used to setup the model in an .h5 file, already trained.
This will work given the dataset is stored in the folder TestDataset/handsign_#, with all the videos for that handsign stored there, and all handsigns containing the same ammount of videos.
Also, the parameters on the first section of the notebook need to be adjusted accordingly before executing anything. The number of frames indicate the number of equidistant frames to be taken from the dataset videos (not the number of frames the videos have). This number should not be longer than the number of frames the videos have.

In the Landmark visualization folder you will find a scrit that takes the landmarks extracted from the dataset videos and shows you in an .mp4 file output how any one video's landmarks look like. 
This is to manually ensure the landmarks are being captured correctly before training on a big dataset.


dataset we are currently using was obtained from here: https://facundoq.github.io/datasets/lsa64/

PYTHON VERSION INSTALLED NEEDS TO BE 3.12 FOR THIS TO WORK


How to set up:
-
get the handsign in a folder in the root path, this handsigns folder can be names as you want, but you will have to specify it on the first cell.
Inside said folder you may place all the videos from each handsign you wish to train into their respective folders with the handsign's name.
Once you run the first cell once, you will see in the output how many videos each handsign has. From here YOU NEED TO MODIFY the videos_per_handsign variable on the first cell according to the handsign with the least videos.

Once that is set, you can execute all the cells one by one in order to get to the fully trained model. If you did not modify the dataset or any function that extracts it, you dont need to execute the video processing functions (they have an execution cell separated for this purpose, as you will need to rerun the dataset processing funciton definition cell at least once each time you close the environment for the live prediction to work).

Mind the data augmentation and number of samples variables, adjust them to your dataset and needs.

here is a 64 words 50 videos per word dataset you can download to test this.
download dataset from https://facundoq.github.io/datasets/lsa64/
if you use this dataset the datasetOrganizingScript will auto-sort it into the handsigns names in spanish.


Also dont forget to modify the data shape parameters on the first cell of the building-and-training.ipynb notebook so it matches the dataset being used.

To install dependencies
-
open a cmd on the root folder and (having python already installed on your system) type "pip install -r .\requirements.txt"
this should install all necessary dependencies for the project.

if this doesn't work try doing a "pip install pipreqs" on the same cmd and then going back to the first command
