import requests, json, pprint
from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route('/api/topology')
def print_topology():
    return jsonify(topology_json['response'])

@app.route('/')
def print_topology_html():
    return render_template('topology.html')

def new_ticket():
    url = 'https://sandboxapic.cisco.com/api/v1/ticket'
    payload = {'username': 'devnetuser',
               'password': 'Cisco123!'}
    header = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload),
                             headers=header, verify=False)
    return response.json()['response']['serviceTicket']


def req(url, ticket, req_type):
    header = {'content-type': 'application/json',
              'X-Auth-Token': ticket}
    print(url, flush=True)
    response = requests.get(url, headers=header, verify=False)
    print('--------------------------')
    print(req_type + ':')
    # pprint.pprint(json.dumps(response.json()))
    return response.json()


if __name__ == '__main__':
    ticket = new_ticket()
    controller = 'devnetapi.cisco.com/sandbox/apic_em'
    hosts_url = 'https://' + controller + '/api/v1/host'
    device_list_url = 'https://' + controller + '/api/v1/network-device'
    topology_url = 'https://' + controller + '/api/v1/topology/physical-topology'

    hosts_json = req(hosts_url, ticket, 'Hosts')
    device_list_json = req(device_list_url, ticket, 'Device list')
    topology_json = req(topology_url, ticket, 'Topology')

    app.run(debug=True, use_reloader=False)
