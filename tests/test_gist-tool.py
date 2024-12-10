import requests

TEST_USER = 'octocat'
NON_EXISTING_USER = 'octodog'
HEALTH_ENDPOINT = 'http://0.0.0.0:8080/health'
API_ENDPOINT = 'http://0.0.0.0:8080'

headers = {
    'Authorization': '',
    'accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'raw_results': 'False'
}

raw_enabled_headers = {
    'Authorization': '',
    'accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'raw_results': 'True'
}

def test_health_endpoint():
  r = requests.get(f"{API_ENDPOINT}/health")
  assert r.status_code == 200

def test_existing_gist_user():
  r = requests.get(f"{API_ENDPOINT}/{TEST_USER}", headers=headers)
  data = r.json()
  assert data['User'] == TEST_USER

def test_existing_gist_data():
  r = requests.get(f"{API_ENDPOINT}/{TEST_USER}", headers=headers)
  data = r.json()

  assert data['Public Gist List'] is not None

def test_existing_gist_raw_data():
  r = requests.get(f"{API_ENDPOINT}/{TEST_USER}", headers=raw_enabled_headers)
  data = r.json()
  # Raw data is returend in a dictionery. check position 0
  assert data[0]['public'] == True

def test_non_existing_gist_user():
  r = requests.get(f"{API_ENDPOINT}/{NON_EXISTING_USER}", headers=headers)
  data = r.json()
  assert data['User'] == NON_EXISTING_USER

def test_non_existing_gist_data():
  r = requests.get(f"{API_ENDPOINT}/{NON_EXISTING_USER}", headers=headers)
  data = r.json()
  assert data['Public Gist List'] == []
