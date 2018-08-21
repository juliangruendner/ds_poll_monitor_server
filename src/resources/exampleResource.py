from flask_restful import Resource, Api, reqparse, abort

examples = [
    {
        'id': 1,
        'data': 'data1'
    }
]

class ExampleList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('data', type=str, required=True, help='No data provided', location='json')
        super(ExampleList, self).__init__()

    def get(self):
        return examples

    def post(self):
        args = self.parser.parse_args()
        example = {
            'id': examples[-1]['id'] + 1,
            'data': args['data']
        }
        examples.append(example)
        return example, 201

class Example(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('data', type=str, required=True, help='No data provided', location='json')
        super(Example, self).__init__()

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