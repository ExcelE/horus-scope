# Horus Scope

[![Build Status](https://dev.azure.com/eespina002/eespina002/_apis/build/status/ExcelE.horus-scope?branchName=master)](https://dev.azure.com/eespina002/eespina002/_build/latest?definitionId=1?branchName=master)

### Making the language barrier a thing of the past.
Our goal is to enable people who have cameras on their devices to learn more about the world no matter the language, culture or trend.
We are augmenting exploration through the utilization of Computer Vision and Deep Learning to deliver a seemless experience on your phone, laptop or desktop.


### Running the project
1) Clone repo  
2) Install docker and docker-compose  
3) Pull all binary engine files:  
> Install `git lfs` with the following: `curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash`  
>`git lfs fetch`  
3) Run `docker-compose up --build`  
4) Connect to `http://ip:7000/<route>` (or some other port, check the docker-compose.yml)  
[Under construction]

### Tips

* Cleaning up files after tests:  
`docker image prune -a`  
`docker container prune`

* How to forceably switch branches:

```
git checkout HEAD^
git checkout -f <branch>
```
