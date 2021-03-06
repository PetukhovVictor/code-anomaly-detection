import argparse
import json

from lib.TimeLogger import TimeLogger

parser = argparse.ArgumentParser()
parser.add_argument('--anomalies_list_1', nargs=1, type=str, help='folder with kotlin source codes')
parser.add_argument('--anomalies_list_2', nargs=1, type=str, help='output folder with anomalies as JSON')
parser.add_argument('--output', '-o', nargs=1, type=str, help='output folder with anomalies as JSON')

args = parser.parse_args()
anomalies_list_1 = args.anomalies_list_1[0]
anomalies_list_2 = args.anomalies_list_2[0]
output = args.output[0]

time_logger_common = TimeLogger(task_name="Anomalies calc intersection")

anomalies_1 = {}
anomalies_2 = {}
intersect = {}
first_contain_only = {}
second_contain_only = {}

with open(anomalies_list_1) as anomalies_list_1_descriptor:
    anomalies = json.loads(anomalies_list_1_descriptor.read())

    for anomaly in anomalies:
        anomalies_1[anomaly[0]] = anomaly[1]


with open(anomalies_list_2) as anomalies_list_2_descriptor:
    anomalies = json.loads(anomalies_list_2_descriptor.read())

    for anomaly in anomalies:
        anomalies_2[anomaly[0]] = anomaly[1]
        if anomaly[0] in anomalies_1:
            intersect[anomaly[0]] = [anomalies_1[anomaly[0]], anomaly[1]]
        else:
            second_contain_only[anomaly[0]] = anomaly[1]

for anomaly in anomalies_1:
    if anomaly not in anomalies_2:
        first_contain_only[anomaly] = anomalies_1[anomaly]


with open(output, 'w') as output_descriptor:
    output_descriptor.write(json.dumps({
        'intersect': intersect,
        'first_contain_only': first_contain_only,
        'second_contain_only': second_contain_only
    }))

time_logger_common.finish(full_finish=True)
