import requests
from requests.auth import HTTPDigestAuth
import os
import time

CHAT2QUERY_ENPOINT_ID = os.getenv("CHAT2QUERY_ENPOINT_ID")

def query_information_database(query:str):

    print("Got the query:", query)

    url = f'https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/chat2query-{CHAT2QUERY_ENPOINT_ID}/endpoint/v3/chat2data'
    headers = {'content-type': 'application/json'}
    data = {
        "cluster_id": "10843682973482617161",
        "database": "PetFit",
        "question": query,
        "sql_generate_mode": "direct"
    }
    response = requests.post(
        url,
        json=data,
        headers=headers,
        auth=HTTPDigestAuth(os.getenv("TIDB_DATA_API_PUBLIC_KEY"),os.getenv("TIDB_DATA_API_PRIVATE_KEY"))
    )
    response = response.json()
    job_id = response["result"]["job_id"]
    data = None

    print("Job Id is:", str(job_id))

    while not data:
        job_response = requests.get(
            f"https://ap-southeast-1.data.tidbcloud.com/api/v1beta/app/chat2query-{CHAT2QUERY_ENPOINT_ID}/endpoint/v2/jobs/{job_id}",
            headers=headers,
            auth=HTTPDigestAuth(os.getenv("TIDB_DATA_API_PUBLIC_KEY"),os.getenv("TIDB_DATA_API_PRIVATE_KEY"))
        )

        job_response = job_response.json()

        if job_response["code"] == 200 and job_response["result"]["status"] == 'done':
            data = job_response["result"]["result"]["data"]
        else:
            time.sleep(10)
    print("Data is:", str(data))
    return data