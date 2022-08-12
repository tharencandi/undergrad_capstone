### Glioblastoma Cell Pre-Processing Portal ###

Current Version: 0.0.0
Build Passing: N/A

### Project Setup ###

1. Clone the repository onto your local machine
	- Via ssh: `git clone git clone git@bitbucket.org:tharencandi/glioblastoma_processing.git`
	- Via https: `git clone https://hbal7849@bitbucket.org/tharencandi/glioblastoma_processing.git`
2. Configuration: N/A
3. Dependencies: All dependencies are listed in the requirements.txt file at the root of the repository.
	1. Using your shell of choice, enter the root directory of the project `cd glioblastoma_processing`
	2. Create a python3 virtual environment `python3 -m venv .venv`
	3. Activate the virtual environment `source .venv/bin/activate`
	4. Install the project dependencies using the requirements.txt file at the root of the repository `pip install -r requirements.txt`
4. Database configuration: N/A
5. How to run tests: N/A
6. Deployment instructions: N/A

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
