### Glioblastoma Cell Pre-Processing Portal ###

Current Version: 0.0.0
Build Passing: N/A

---

### **PERFORMANCE WARNING** ###
for best performance, please configure tensorflow2 to use NVIDIA CUDA enabled GPU's for computation. Follow the install guide [here](https://www.tensorflow.org/install/pip).


---

### Project Setup ###

1. Clone the repository onto your local machine
	- Via ssh: `git clone git clone git@bitbucket.org:tharencandi/glioblastoma_processing.git`
	- Via https: `git clone https://hbal7849@bitbucket.org/tharencandi/glioblastoma_processing.git`
2. Configuration: N/A
3. Dependencies: All python pip dependencies are listed in the requirements.txt file at the root of the repository.
	1. Using your shell of choice, enter the root directory of the project `cd glioblastoma_processing`
	2. Create a python3 virtual environment `python3 -m venv .venv`
	3. Activate the virtual environment `source .venv/bin/activate`
	4. Install the project dependencies using the requirements.txt file at the root of the repository `pip install -r requirements.txt`
	5. apt-get update
	6. apt-get install -y openslide-tools
	7. apt-get install -y python3-opencv
	8. install nvm and nodejs
	8. DRAN/CNN weights available at 

4. How to run tests: run pytest in repo directory. 
5. Deployment instructions:

- How to setup CNN for mask generation:
	1. download pre-trained weights here or follow CNN training process.
	2. download model `.json` or generate by running `python3 src/CNN/cnn_model.py`
	3. configure `MODEL` and `WEIGHTS` constants at the top of `src/CNN/predict.py` to 1 and 2.
	4. deploy webportal and use its interface to generate masks on your computer *OR* follow **server** deploymenet process 


- How to deploy webportal:
	1. `python3 src/webportal/webportal.py ----existingDataPath [path_to_drive_with_GDC_data]`
	2. `redis-server`
	2. `celery -A "webportal" worker --loglevel=INFO`
	3. build react front end: cd into src/webportal/frontend and run `npm install` and `npm run build`

- How to train model
	1. training and validation datasets are available [here](link). 
		- place in `data/training` and `data/validation` respectivley.
	2. generate datasets by running `python3 src/CNN/dataset.py` and following its instructions. 
	3. after 2, set related constants `TRAIN_LOCATON` and `TEST_LOCATION` in `src/CNN/train.py`.
	4. set other hypermater constants in `train.py` and set ` FUNC = functions.SINGLE_TRAIN` or explore other functions
	5. `python3 src/CNN/train.py`

- How to test model
	- aside from testing that is done in `train.py`, the IOU and mIOU of the original **validation** dataset can be determined by way of `src/CNN/test.py`. This script it configured to the relative file path `data/validation`.
	1. set the constant `SAVE_DIR` to desired location for image and csv results at the top of `train.py` 
	2. set the correct `MODEL` and `WEIGHTS` paths at the top of `src/CNN/predict.py`
	3. `python3 src/CNN/test.py`.

- generate masks from manifest on a remote machine
	
	**WARNING: THIS IS ADVANCE USE OF THIS SOURCE CODE AND REQUIRES SET UP OF AN INTERNET WEB SERVICE. FOR THE DURATION OF THIS PROJECT WE HAVE USED A PAYED NGROK SERVICE.**

	1. configure and deploy **management_app** on the computer with your hard-drive. (the computer you want the masks to be sent to)
	2. clone repository on remote machine & install all dependancies
	3. Create a manifest file with the [GDC website](https://portal.gdc.cancer.gov/projects/TCGA-GBM). 
	4. configure `downloader_config.yaml`, 
		- `MIMIC_GDC_FOLDERS="MIMIC_GDC_FOLDERS` to `False`.
		- `UPLOAD` to `True`
		- and add the username and password you created for the management app. 
	5. configure `predict_config.yaml`.
		- `svs_dir` set to the same directory as the output directory in `downloader_config.yaml`. 
		- `MANIFEST_IN` set to the location of the manifest you created.
	6. open a new terminal window (preferably with tmux) and run the download script:
	 	- `python3 src/download_tool/download_script.py my_manifest.txt downloader_config.yaml`
	7. open another terminal window (preferably with tmux) and run `predict.py`
		-  `python3 src/CNN/predict.py preidct_config.yaml`

- deploy management app
	- Contact Haeata Balford Ash for deployement assistance, or any repo owner/admin.
### Contribution guidelines ###

* Git workflow:
	1. Create topic branch: `git checkout -b my_branch`
	2. Add/stage changes: `git add file1.py file2.py`
	3. Commit changes with a very informative message `git commit -m "A very informative message"`
	4. Push your changes using `git push origin` if the branch already exists on the remote or `git push --set-upstream origin my_branch` if not.
	5. Once the feature is finished or the changes should be merged into the main branch, create a pull request.
* Testing
	* All code should have unit tests - consider writing the unit tests first
* Code review: All code pulled into main should be reviewed by a minimum of one other individual
* Code Style: All python code should follow the PEP-8 style guideline. Python code will be formatted using the flak8 tool.


### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact
