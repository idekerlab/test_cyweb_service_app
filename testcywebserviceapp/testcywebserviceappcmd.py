#!/usr/bin/env python

import os
import sys
import argparse
import json
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
                        choices=['updateTables', 'addNetworks', 'updateNetwork', 'updateLayouts', 'updateSelection'],
                        default='updateTables',
                        help='Mode. Default: updateTables.')
    parser.add_argument('--column_name', default='test_col',
                        help='Column name. Default: test_col.')
    parser.add_argument('--apply_to_edges', action='store_true',
                        help='Applies action on edges instead of nodes.')
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


def run_update_tables(net_cx2, column_name='test_col', aspect="nodes"):
    col_update_data = {}
    aspect_keys = net_cx2.get_nodes().keys() if aspect == "nodes" else net_cx2.get_edges().keys()
    for aspect_id in aspect_keys:
        col_update_data[aspect_id] = {column_name: "test_val"}
    data = [
        {
            "id": aspect,
            "columns": [{"id": column_name, "type": "string"}],
            "rows": col_update_data
        }
    ]
    return data


def run_update_layouts(net_cx2):
    layouts_update_data = []
    test_x = 0
    test_y = 5
    test_z = 6
    for node_id in net_cx2.get_nodes().keys():
        data = {
            "id": node_id,
            "x": test_x,
            "y": test_y,
            "z": test_z
        }
        layouts_update_data.append(data)
    return layouts_update_data


def run_update_selection(net_cx2):
    data = {
        "nodes": list(net_cx2.get_nodes())[:3],
        "edges": list(net_cx2.get_nodes())[:2]
    }
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
        if theargs.mode == 'updateTables':
            net_cx2 = get_cx2_net_from_input(theargs.input)
            aspect = "edges" if theargs.apply_to_edges else "nodes"
            theres = run_update_tables(net_cx2=net_cx2, column_name=theargs.column_name, aspect=aspect)
        elif theargs.mode == 'addNetworks':
            net_cx2 = get_cx2_net_from_input(theargs.input)
            theres = run_add_networks(net_cx2)
        elif theargs.mode == 'updateNetwork':
            net_cx2 = get_cx2_net_from_input(theargs.input)
            theres = run_update_network(net_cx2)
        elif theargs.mode == 'updateLayouts':
            net_cx2 = get_cx2_net_from_input(theargs.input)
            theres = run_update_layouts(net_cx2)
        elif theargs.mode == 'updateSelection':
            net_cx2 = get_cx2_net_from_input(theargs.input)
            theres = run_update_selection(net_cx2)

        if theres is None:
            sys.stderr.write('No results\n')
        else:
            json.dump(theres, sys.stdout, indent=2)
        sys.stdout.flush()
        return 0
    except Exception as e:
        sys.stderr.write('Caught exception: ' + str(e))
        return 2


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(sys.argv))
