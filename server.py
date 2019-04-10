#!flask/bin/python
import json
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

with open('./data/api_data.json', 'r') as f:
	data = json.load(f)

class StdHypeCycle(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.std_hype_cycle = data['Std_Hype_cycle']

	def get(self):
		return jsonify( self.std_hype_cycle )

class HypeCycle(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.hype_cycles = data['Hype_cycles']

	def get(self, term):
		if term not in self.hype_cycles:
			abort(404)
		else:
			res = self.hype_cycles[term]
			res['term'] = term
			return jsonify( res )

class Position(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument('term', type=str)
		self.parser.add_argument('year', type=str)
		self.positions = data['Positions']
		self.values = data['Std_Hype_cycle_value']

	def get(self, term, year):
		if term not in self.positions or year not in self.positions[term]:
			abort(404)
		else:
			pos = int(self.positions[term][year])
			return jsonify( {'pos': pos * 0.1, 'value': self.values[pos]} )

class Patents(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument('term', type=str)
		self.patents = data['Patents']

	def get(self, term):
		if term not in self.patents:
			abort(404)
		else:
			res = self.patents[term]
			res['term'] = term
			return jsonify( res )

class Papers(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument('term', type=str)
		self.papers = data['Papers']

	def get(self, term):
		if term not in self.papers:
			abort(404)
		else:
			res = self.papers[term]
			res['term'] = term
			return jsonify( res )


api.add_resource(StdHypeCycle, '/std_hype_cycle')
api.add_resource(Patents, '/patents/<term>')
api.add_resource(Papers, '/papers/<term>')
api.add_resource(HypeCycle, '/hype_cycles/<term>')
api.add_resource(Position, '/position/<term>/<year>')


if __name__ == '__main__':
	app.run(port=9000, debug=True)

