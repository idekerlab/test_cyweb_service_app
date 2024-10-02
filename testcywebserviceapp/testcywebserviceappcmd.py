#!/usr/bin/env python

import os
import sys
import argparse
import json
from ndex2.cx2 import RawCX2NetworkFactory

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
    parser.add_argument('network',
                        help='Network in CX2 format')
    parser.add_argument('--mode', choices=['UpdateTables'], default='UpdateTables',
                        help='Mode. Default: UpdateTables.')
    parser.add_argument('--column_name', default='test_col',
                        help='Column name. Default: test_col.')
    return parser.parse_args(args)


def run_update_tables(net_cx2, column_name='test_col'):
    col_update_data = {}
    for node_id in net_cx2.get_nodes().keys():
        col_update_data[node_id] = {column_name: "test_val"}
    data = [
        {
            "id": "nodes",
            "columns": [{"id": column_name, "type": "string"}],
            "rows": col_update_data
        }
    ]
    return data


def main(args):
    """
    Main entry point for program

    :param args: command line arguments usually :py:const:`sys.argv`
    :return: 0 for success otherwise failure
    :rtype: int
    """
    desc = """
        Running gene enrichment against Integrated Query

        Takes file with comma delimited list of genes as input and
        uses Integrated Query (iQuery) enrichment service to 
        to find best network that best matches query genes. The
        best network is the one with highest similarity score.
        This tool then uses the network name as the term name.
        
        The result is sent to standard out in JSON format 
        as follows:
        
        {
         "name":"<TERM NAME WHICH IS NAME OF NETWORK>",
         "source":"<SOURCE OF NETWORK>",
         "p_value":<PVALUE>,
         "description":"<URL OF NETWORK IN NDEx>",
         "term_size":<NUMBER OF NODES IN NETWORK>,
         "intersections":["<LIST OF FOUND IN NETWORK>"]
        }
        
        NOTE: term_size is set to number of nodes in network
              and NOT number of genes
    """

    theargs = _parse_arguments(desc, args[1:])
    try:
        theres = None
        if theargs.mode == 'UpdateTables':
            net_cx2_path = os.path.abspath(theargs.network)
            factory = RawCX2NetworkFactory()
            net_cx2 = factory.get_cx2network(net_cx2_path)
            theres = run_update_tables(net_cx2=net_cx2, column_name=theargs.column_name)

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
