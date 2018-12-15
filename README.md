# Horus Scope

[![Build Status](https://dev.azure.com/eespina002/eespina002/_apis/build/status/ExcelE.horus-scope?branchName=master)](https://dev.azure.com/eespina002/eespina002/_build/latest?definitionId=1?branchName=master)

### Making the language barrier a thing of the past.
Our goal is to enable people who have cameras on their devices to learn more about the world no matter the language, culture or trend.
We are augmenting exploration through the utilization of Computer Vision and Deep Learning to deliver a seemless experience on your phone, laptop or desktop.


### Running the project
1) Clone repo  
2) Install docker and docker-compose  
3) Pull all binary engine files:  

Install `git lfs` with the following: 
>`curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash`  
>`apt-get install git-lfs`  
>`git lfs install`  
>`git lfs fetch`  
>`git lfs pull`  

4) Run `docker-compose up --build`  
5) Connect to `http://ip:7000/<route>` (or some other port, check the docker-compose.yml)  
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

### Documentation

API Routes:

`/register`:  
* Request Parameters:
    * username
    * password
* Return:
    * login: True (success)
    * access_token
    * error (fail)

`/login`:
* Request Parameters:
    * username
    * password
* Return:
    * login: True (success)
    * access_token
    * error (fail)

`/classify`:
* Request Parameters:
    * access_token_cookie
        * You get this access token when you sign in or register
    * photo
        * Please supply a jpeg or jpg
* Return:
    * predictions: (success)
        * This is an array of predictions with the following fields:
            * description
            * score
            * summary
            * wikipediaUrl
    * error (fail)
        * Failure usually means that there was no access token in the parameter and you should log the user in

`/refill`:
* Request Parameters:
    * access_token_cookie
    * amount (optional)
        * You can supply a custom amount of tokens to refill. If not specified, will default to 3 tokens
* Return:
    * Latest amount of tokens
    * error (fail)
        * Failure usually means that there was no access token in the parameter and you should log the user in

`/logout`:
* Request Parameters:
    * None
* Return:
    * logout: True