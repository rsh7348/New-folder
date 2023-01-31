import csv
import requests

def export_server_metrics_to_csv(server_id, api_token, csv_file):
    headers = {'Authorization': 'Api-Token ' + api_token}
    url = 'https://your-dynatrace-server/api/v1/metrics/' + server_id + '/process-group'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        metrics_data = response.json()
        with open(csv_file, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'metricName', 'value']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for data in metrics_data['data']:
                for timestamp in data['dataPoints']:
                    writer.writerow({'timestamp': timestamp['timestamp'], 'metricName': data['metricId']['metric'], 'value': timestamp['value']})
    else:
        print('Error: ' + str(response.status_code))
