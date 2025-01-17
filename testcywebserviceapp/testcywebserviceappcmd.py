#!/usr/bin/env python

import os
import sys
import time
import argparse
import json
import random
from ndex2.cx2 import RawCX2NetworkFactory, CX2Network

SOURCES_KEY = 'sources'
RESULTS_KEY = 'results'
DETAILS_KEY = 'details'
SIMILARITY_KEY = 'similarity'


def _parse_arguments(desc, args):
    """
    Parses command line arguments
    :param desc:
    :param args:
    :return:
    """
    help_fm = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(description=desc,
                                     formatter_class=help_fm)
    parser.add_argument('input',
                        help='Input: network in CX2 format, node data or edge data.')
    parser.add_argument('--mode',
                        choices=['updateTables', 'addNetworks', 'updateNetwork', 'updateLayouts', 'updateSelection',
                                 'openURL', 'updatelayoutandselection'],
                        default='updateTables',
                        help='Mode. Default: updateTables.')
    parser.add_argument('--input_type', default='network', choices=['network', 'edge', 'node'],
                        help='Denotes format of input file passed in')
    parser.add_argument('--column_name', default='test_col',
                        help='Column name. Default: test_col.')
    parser.add_argument('--column_value', default='test_val',
                        help='Value to put in --column_name column. Used by --mode updateTables')
    parser.add_argument('--apply_to_edges', action='store_true',
                        help='Applies action on edges instead of nodes.')
    parser.add_argument('--sleep_time', type=int, default=0,
                        help='Number of seconds to wait before returning a result')
    parser.add_argument('--error_message',
                        help='If set, job should fail and return this error message to standard error')
    parser.add_argument('--min_x_layoutcoord', default=-1000.0, type=float,
                        help='Sets minimum range for random x coordinates for updateLayouts')
    parser.add_argument('--max_x_layoutcoord', default=1000.0, type=float,
                        help='Sets maximum range for random x coordinates for updateLayouts')
    parser.add_argument('--min_y_layoutcoord', default=-1000.0, type=float,
                        help='Sets minimum range for random y coordinates for updateLayouts')
    parser.add_argument('--max_y_layoutcoord', default=1000.0, type=float,
                        help='Sets maximum range for random y coordinates for updateLayouts')
    parser.add_argument('--min_z_layoutcoord', default=-1000.0, type=float,
                        help='Sets minimum range for random z coordinates for updateLayouts')
    parser.add_argument('--max_z_layoutcoord', default=1000.0, type=float,
                        help='Sets maximum range for random z coordinates for updateLayouts')
    parser.add_argument('--include_zcoord', action='store_true',
                        help="If set, include z coordinate for when generating layout coordinates for updateLayouts")
    parser.add_argument('--random_seed', default=time.time(), type=float,
                        help='Seed for random number generator')
    parser.add_argument('--openurl', default='https://ndexbio.org',
                        help='URL to open with openURL mode')
    parser.add_argument('--openurltarget', default='none',
                        help='If set to value other then empty string, whitespace, or "none", '
                             'open url in iframe on right side of Cytoscape Web')
    return parser.parse_args(args)


def run_add_networks(net_cx2):
    new_net = CX2Network()
    new_net.add_network_attribute(key="name", value="New network from: " +
                                                    net_cx2.get_network_attributes().get("name", ""))
    node_id1 = new_net.add_node(attributes={"name": "node1"})
    node_id2 = new_net.add_node(attributes={"name": "node2"})
    new_net.add_edge(source=node_id1, target=node_id2)
    return [new_net.to_cx2()]


def run_update_network(net_cx2):
    net_cx2.add_node(attributes={"name": "new_node"})
    return net_cx2.to_cx2()


def run_update_tables(net_cx2, column_name='test_col', column_value='test_val',
                      aspect="node"):
    col_update_data = {}
    aspect_keys = net_cx2.get_nodes().keys() if aspect == "node" else net_cx2.get_edges().keys()
    for aspect_id in aspect_keys:
        col_update_data[aspect_id] = {column_name: str(column_value)}
    data = {
            "id": aspect,
            "columns": [{"id": column_name, "type": "string"}],
            "rows": col_update_data
           }

    return data


def run_update_layouts(net_cx2, include_z=False, min_x=-1000.0,
                       max_x=1000.0, min_y=-1000.0, max_y=1000.0,
                       min_z=-1000.0, max_z=1000.0):
    """
    Generate random layout coordinates for x and y (z if include_z is set to True)

    """
    layouts_update_data = []
    for node_id in net_cx2.get_nodes().keys():
        data = {
            "id": node_id,
            "x": round(random.uniform(min_x, max_x), 4),
            "y": round(random.uniform(min_y, max_y), 4)
        }
        if include_z is True:
            data['z'] = round(random.uniform(min_z, max_z), 4)

        layouts_update_data.append(data)
    return layouts_update_data

def get_unique_random_choices_from_list(thelist, num_choices):
    if num_choices >= len(thelist):
        return thelist
    picked_choices = set(random.choices(thelist, k=num_choices))
    while len(picked_choices) < num_choices:
        picked_choices.add(random.choice(thelist))
    return list(picked_choices)

def run_update_selection(net_cx2, num_nodes=3, num_edges=2):
    node_list = list(net_cx2.get_nodes())
    edge_list = list(net_cx2.get_edges())
    data = {
        'nodes': get_unique_random_choices_from_list(node_list, num_nodes),
        'edges': get_unique_random_choices_from_list(edge_list, num_edges)
    }

    return data

def run_openurl(input, openurl=None, openurltarget=None):
    """
    For now just ignore input and
    """
    targetval = None
    if openurltarget is not None and len(openurltarget.strip()) > 0 and openurltarget.lower() != 'none':
        targetval = openurltarget
    data = {'url': str(openurl),
            'target': targetval}
    return data


def get_cx2_net_from_input(input_path):
    net_cx2_path = os.path.abspath(input_path)
    factory = RawCX2NetworkFactory()
    return factory.get_cx2network(net_cx2_path)


def main(args):
    """
    Main entry point for program

    :param args: command line arguments usually :py:const:`sys.argv`
    :return: 0 for success otherwise failure
    :rtype: int
    """
    desc = """
    TODO
    """

    theargs = _parse_arguments(desc, args[1:])
    try:
        theres = None

        # sleep amount of time designated
        sys.stderr.write('Sleeping ' + str(theargs.sleep_time) + ' seconds.\n')
        time.sleep(theargs.sleep_time)

        sys.stderr.write('Setting random seed to: ' + str(theargs.random_seed) +'\n')
        random.seed(theargs.random_seed)
        if theargs.error_message is not None:
            sys.stderr.write(theargs.error_message)
            sys.stderr.flush()
            return 1

        if theargs.mode == 'updateTables':
            net_cx2 = get_cx2_net_from_input(theargs.input)
            aspect = "edge" if theargs.apply_to_edges else "node"
            theres = run_update_tables(net_cx2=net_cx2, column_name=theargs.column_name,
                                       column_value=theargs.column_value, aspect=aspect)
        elif theargs.mode == 'addNetworks':
            net_cx2 = get_cx2_net_from_input(theargs.input)
            theres = run_add_networks(net_cx2)
        elif theargs.mode == 'updateNetwork':
            net_cx2 = get_cx2_net_from_input(theargs.input)
            theres = run_update_network(net_cx2)
        elif theargs.mode == 'updateLayouts':
            net_cx2 = get_cx2_net_from_input(theargs.input)
            theres = run_update_layouts(net_cx2,
                                        min_x=theargs.min_x_layoutcoord,
                                        max_x=theargs.max_x_layoutcoord,
                                        min_y=theargs.min_y_layoutcoord,
                                        max_y=theargs.max_y_layoutcoord,
                                        min_z=theargs.min_z_layoutcoord,
                                        max_z=theargs.max_z_layoutcoord,
                                        include_z=theargs.include_zcoord)
        elif theargs.mode == 'updateSelection':
            net_cx2 = get_cx2_net_from_input(theargs.input)
            theres = run_update_selection(net_cx2)
        elif theargs.mode == 'openURL':
            theres = run_openurl(theargs.input, openurl=theargs.openurl,
                                 openurltarget=theargs.openurltarget)
        elif theargs.mode == 'updatelayoutandselection':
            net_cx2 = get_cx2_net_from_input(theargs.input)
            theres = [{ 'action': 'updateLayouts',
                        'data': run_update_layouts(net_cx2,
                                                   min_x=theargs.min_x_layoutcoord,
                                                   max_x=theargs.max_x_layoutcoord,
                                                   min_y=theargs.min_y_layoutcoord,
                                                   max_y=theargs.max_y_layoutcoord,
                                                   min_z=theargs.min_z_layoutcoord,
                                                   max_z=theargs.max_z_layoutcoord,
                                                   include_z=theargs.include_zcoord)},
                      { 'action': 'updateSelection',
                        'data': run_update_selection(net_cx2)}]

        if theres is None:
            sys.stderr.write('No results\n')
        else:
            # special case if updatelayoutandselection just return the value
            # since that call already adds in an action
            if theargs.mode == 'updatelayoutandselection':
                newres = theres
            else:
                newres = [{'action': theargs.mode,
                           'data': theres}]
            json.dump(newres, sys.stdout, indent=2)
        sys.stdout.flush()
        sys.stderr.flush()

        return 0
    except Exception as e:
        sys.stderr.write('Caught exception: ' + str(e))
        sys.stderr.flush()
        return 2


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(sys.argv))
