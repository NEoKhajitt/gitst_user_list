# Gist Pub Tool

#### Description
The Gist Pub tool is meant to interface with the GitHub public gist list for a targeted user and return a list of public gist urls


#### Internals
The tool makes use of fastAPI/Uvicorn as it's api/server layer
Colored logs for some color in your life ##TODO: Increase logging output where required.
Requests for making the requests to Github server.


#### TL;DR Getting Started
Clone this repo.  
```bash
repo_name='equal-experts-quick-original-desirable-joy-8e35c12cad4b'
cd $repo_name/build
docker build -f Dockerfile -t gist-user-tool:latest ..
docker run -p 8080:8080 --name gist-test-tool gist-user-tool:latest
# Open a new terminal to keep an eye on the api logs
curl -L -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" -H "raw_results: false" http://0.0.0.0:8080/octocat

```


#### Endpoints
##### `/health`
Health endpoint return a 200 with Health Status OK
```json
"Health Status": "OK"
```
###### Options
None


##### `/{user}`
User endpoint uses the endpoint parameter as a username, passes additional headers in from the curl/postman request
```python
requests.get(f"https://api.github.com/users/{user}/gists", headers={'X-GitHub-Api-Version': git_api_version, 'accept': accept, 'Authorization': authorisation_token})
```
The endpoint includes an `Elapsed Time` result for performance metrics.

###### Options
users endpoint has an additional option/header:
`raw_results` Defaults to `False`
When enabled (set to true) instead of producing a simple list of gist urls, it will return the raw request from the GitHub endpoint, this might help in debugging or when needing to see additional information.


#### Testing
To install and run the gist-tool locally, ensure you have a fresh Python 3 Virtual Environment by running:
```bash
python3.11 -m venv .venv311
source .venv311/bin/activate
```
Appending the venv name with 311 is not required, it's a personal preference as I usually have more than one Python version to run or test with depending on the requirement.

Then run `pip install -r requirements.txt` from [requirements/requirement.txt](../requirements/requirements.txt)

Then run `python app.py` from [src/app.py](../src/app.py)

To Optionally run the automated test, run `pip install -r test-requirements.txt` from [requirements/test-requirement.txt](../requirements/test-requirements.txt) to install the testing dependencies.  
Then run the `pytest -sv test_gist-tool.py` from [tests/test_gist_tool.py](../tests/test_gist-tool.py)
![alt text](test_results.png)

In testing cases we use octocat as the existing user and octodog as a non-existing user
Has a few tests to check if API is running, data of existing and non-existing users and difference of expected and raw data

For reaching the running service use the following curl
```bash
curl -L -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" -H "raw_results: False" http://0.0.0.0:8080/<user>
```

You can also import the [Postman Collection](../tests/Project.postman_collection.json)


#### Requirements
I use `pip-tools` to manage the dependency tree and compile the pip reuiqrements.txt file.  

Ensure you have pip-tools installed by running `pip install pip-tools`  

In [requirements/pyproject.toml](../requirements/pyproject.toml) I have all the main package requirements.
From the requirements directory run `pip-compile --no-emit-index-url --output-file=requirements.txt pyproject.toml`  
This will generate a requirements.txt with pinned dependencies, subdependencies and indicating the dependency tree.  

Similarly for the `test-requirements.txt`
Run `pip-compile --extra=test --no-emit-index-url --output-file=test-requirements.txt pyproject.toml`

Making use of the pyproject.toml also puts you 90% closer to building the tool as a stand alone package to commit to your artifactory.  


#### Docker Build

Change directory to [build](../build/) and run `docker build -f Dockerfile -t gist-user-tool:latest ..`

For the sake of simplicity i'm using `python:3.11.11-slim`, it has low vulnerabilitties, but for a production based image I would rather opt for a Canonical image with zero vulnerabilitites and install python and other requirements from there.  

Mentioning vulnerabilities, I have included a HEALTHCHECK in the Dockerfile as most tools will report it as a requirement, since this image will only run on docker and not kubernetes I added `CMD curl --fail http://localhost:8080/health || exit 1` as the health check, but installing curl when not required is typically frowned upon.  

Docker build utilise base and final strategy to keep the final layer as clean as possible.  
The pip install will run on the base layer and copy the .local directory over to the final layer.  

I create a nonroot user with a high uid to to ensure the user is not privileged in the container and that it does not potentially conflict with the host's uid's.  

I also don't explicitly expose the port in the Dockerfile as that can potentially bypass proxy rules depending on which docker network it's assigned.

#### Docker run
Once the docker image is successfully built, use the following to start up the tool:
```bash
docker run -p 8080:8080 --name gist-test-tool gist-user-tool:latest
```

Viewing container logs can be done with:
```bash
docker logs -f gist-test-tool
```

Stopping the container with:
```bash
docker stop gist-test-tool
```

Typically i would rather use `docker-compose` with a `docker-compose.yml` as it's much better in keeping track of what arguments were passed to run the container, and a lot more flexibility than docker run.
#TODO Include docker-compose.yml for reference

#### Docker Compose
Using the [docker-compose.yml](../build/docker-compose.yml) to start the service by running the below in the `build` directory
```bash
docker-compose up -d 
```

View logs with:
```bash
docker-compose logs -f
```

Stopping the container with:
```bash
docker-compose down
```

Even though this is very overkill for this API service, it's a nice base to have if the service becomes more complex and needs to tie into a nginx proxy service network etc.  

#### Vulnerability Scans
For this test I used Trivy as it gives you a general all round view of OS Package and Framework Package vulnerabilities. 
Please see for reported vulnerabilities [gist-user-tool-vulnerability-report.sarif](../build/gist-user-tool-vulnerability-report.sarif)