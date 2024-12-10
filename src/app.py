from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
import uvicorn
import requests
from config import config
import logging
import coloredlogs


logger = logging.getLogger(__name__)
coloredlogs.install(
  level='DEBUG',
  logger=logger,
  fmt='%(asctime)s [%(name)s][%(levelname)s] %(message)s'
  )

app = FastAPI()


@app.get('/health')
def health_check():
  return JSONResponse(content={"Health Status": "OK"}, status_code=200)


@app.get('/{user}')
async def get_public_user_gists(
  user: str,
  git_api_version: str = Header('2022-11-28', alias="X-GitHub-Api-Version", description="GitHub API Version"),
  authorisation_token: str = Header(None, alias="Authorisation", description="Value is not required for this tokem, but the Header seems to be required to avoid 403"),
  accept: str = Header('application/vnd.github+json', alias="accept", description="Content-Type for GET"),
  raw_results: str = Header(False, alias="raw_results", description="Enable raw results from GitHub API")
  ):
  pub_git_list = []

  ## Have to include the Authorization header, does not have to have a value to get pub gists else you get 403
  r = requests.get(f"https://api.github.com/users/{user}/gists", headers={'X-GitHub-Api-Version': git_api_version, 'accept': accept, 'Authorization': authorisation_token})
  elapsed_time = r.elapsed.total_seconds()
  
  ## Typically would not catch each status_code
  if r.status_code == 200:
    raw_content = r.json()
  elif r.status_code == 404:
    return JSONResponse(content={"User-Url": "Not Found", "Elapsed Time": elapsed_time}, status_code=404)
  elif r.status_code == 403:
    return JSONResponse(content={"Authorization-header": "Required", "Elapsed Time": elapsed_time}, status_code=403)
  else:
    return JSONResponse(content={"HTTP": "Error", "Elapsed Time": elapsed_time}, status_code=r.status_code)
    

  if raw_results.lower() == 'true':
    return JSONResponse(content=raw_content, status_code=200)
  else:
    try:
      for value in raw_content:
        gits_html_url = value.get('html_url', "")
        pub_git_list.append(gits_html_url)
    except Exception as e:
      raise e

    return JSONResponse(content={"User": user, "Public Gist List": pub_git_list, "Elapsed Time": elapsed_time}, status_code=200)





if __name__ == '__main__':

    uvicorn.run(app, host='0.0.0.0', port=config['service_port'])
