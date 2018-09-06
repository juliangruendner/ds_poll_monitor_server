from flask_restful import Resource, Api, reqparse, abort
from flask_restplus import inputs
from flask import send_from_directory
import os
import sys
import signal
import psutil
import re
import subprocess
import json
import time
from time import gmtime, strftime
from util.logSearcher import LogSearcher
import uuid

examples = [
    {
        'id': 1,
        'data': 'data1'
    }
]

class LoggingList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        #self.parser.add_argument('data', type=str, required=True, help='No data provided', location='json')
        self.parser.add_argument('pollStatus', type=inputs.boolean, default=False, required=False, location='args')
        self.parser.add_argument('changeStatus', type=str, default=False, required=False, location='args')
        self.parser.add_argument('timestamp', type=str, default=False, required=False, location='args')
        self.parser.add_argument('timestampEnd', type=str, default=False, required=False, location='args')
        self.parser.add_argument('getLogFiles', type=inputs.boolean, default=False, required=False, location='args')
        self.parser.add_argument('download', type=inputs.boolean, default=False, required=False, location='args')
        super(LoggingList, self).__init__()

    def get(self):
        args = self.parser.parse_args()
        timestamp = args['timestamp']
        timestamp_end = args['timestampEnd']
        download = args['download']

        if timestamp:
            plusLines = 4
            last_request_lines = self.get_log_by_timestamp(timestamp, plusLines)

            if download:

                return self.prepare_and_send_logfiles(timestamp, timestamp_end)

        else:
            time = strftime("%Y-%m-%d", gmtime())
            logfile = time + "_poll.log"
            logfile = "/root/ds_poll/logging/" + logfile
            last_request_lines = self.tail(logfile, 5)

        requests = self.convert_log_to_json(last_request_lines)
        
        return requests, 200

    def delete(self):

        return {"status": False}

    def post(self):
        args = self.parser.parse_args()

        return {"status": "blub"}, 201

    def tail(self, logfile, n, offset=0):
        n = str(n + offset)
        proc = subprocess.Popen(['tail', '-n', n ,logfile], stdout=subprocess.PIPE)
        lines = proc.stdout.readlines()

        if offset == 0:
            return lines[:]

        return lines[:-offset]

    def convert_log_to_json(self, log_lines):
        reg_begin = re.compile(".*{")
        reg_end = re.compile("\\n")

        requests = []

        for log_line in log_lines:
            if not isinstance(log_line, str): log_line = str(log_line, 'latin-1')
            log_line = re.sub(reg_begin, "{", log_line)
            log_line = re.sub(reg_end, "", log_line)
            log_line = json.loads(log_line)
            requests.append(log_line)
        
        return requests


    def get_log_by_timestamp(self, timestamp, plusLines ):
        date = timestamp[:4] + '-' + timestamp[4:6] + '-' + timestamp[6:8]
        logfile = date + "_poll.log"
        logfile = "/root/ds_poll/logging/" + logfile
        searcher = LogSearcher(logfile)
        timestamp = date + ' ' + timestamp[8:10] + ':' + timestamp[10:12] + ':' + timestamp[12:14]
        return searcher.find(timestamp, plusLines)

    def prepare_and_send_logfiles(self, timestamp, timestamp_end):
        p1 = subprocess.Popen(['ls', '/root/ds_poll/logging'] , stdout=subprocess.PIPE)
        p2 = subprocess.Popen(['grep' ,'_poll.log'] , stdin=p1.stdout, stdout=subprocess.PIPE)
        logfiles = p2.stdout.readlines()
        logifles_to_zip = []
        logging_path = "/root/ds_poll/logging/"

        for logfile in logfiles:
            logfile = str(logfile, 'latin-1')
            cur_file_date = logfile[:-10]
            cur_file_date = int(cur_file_date.replace("-", ""))

            if cur_file_date >= int(timestamp[:8]) and cur_file_date <= int(timestamp_end[:8]):
                logfile = logfile[:-1]
                logifles_to_zip.append(logging_path + logfile)
        
        cur_uuid = str(uuid.uuid1())
        command = ['zip', logging_path + cur_uuid + '.zip']
        command.extend(logifles_to_zip)
        print(command, file=sys.stderr)
        subprocess.Popen(command)

        file_path = logging_path + cur_uuid + '.zip'
        while not os.path.exists(file_path):
            time.sleep(1)

        response = send_from_directory(logging_path, cur_uuid + '.zip' , as_attachment=True)
        response.headers['content-type'] = 'application/octet-stream'
        response.status_code = 200

        return response

class Logging(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('data', type=str, required=True, help='No data provided', location='json')
        super(Logging, self).__init__()

    def abort_if_example_doesnt_exist(self, example_id):
        if example_id not in examples:
            abort(404, message="example {} doesn't exist".format(example_id))

    def get(self, example_id):
        example = [x for x in examples if x['id'] == example_id]
        if len(example) == 0:
            self.abort_if_example_doesnt_exist(example_id)
        return example

    def delete(self, example_id):
        example = [x for x in examples if x['id'] == example_id]
        if len(example) == 0:
            self.abort_if_example_doesnt_exist(example_id)
        examples.remove(example[0])
        return {'result': True}, 204

    def put(self, example_id):
        example = [x for x in examples if x['id'] == example_id]
        if len(example) == 0:
            self.abort_if_example_doesnt_exist(example_id)
        example = example[0]
        args = self.parser.parse_args()
        for k, v in args.items():
            if v is not None:
                example[k] = v
        return example, 201

