Build and train notebook can be used to setup the model in an .h5 file, already trained.
This will work given the dataset is stored in the folder TestDataset/handsign_#, with all the videos for that handsign stored there, and all handsigns containing the same ammount of videos.
Also, the parameters on the first section of the notebook need to be adjusted accordingly before executing anything. The number of frames indicate the number of equidistant frames to be taken from the dataset videos (not the number of frames the videos have). This number should not be longer than the number of frames the videos have.

In the Landmark visualization folder you will find a scrit that takes the landmarks extracted from the dataset videos and shows you in an .mp4 file output how any one video's landmarks look like. 
This is to manually ensure the landmarks are being captured correctly before training on a big dataset.
