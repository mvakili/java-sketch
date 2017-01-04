#! /usr/bin/env python

import util
import json
import logging
import logging.config
import os

from ast.compilationunit import CompilationUnit
from ast.utils import utils
from ast.dataflow.dataflow import DataFlow
from ast.visit.sourcevisitor import SourcePrinter
from ast.visit.symtabgen import SymtabGen
from ast.visit.generic import GenericVisitor

pwd = os.path.dirname(__file__)
log_lvls = {'0':logging.NOTSET, '10':logging.DEBUG, '20':logging.INFO, '30':logging.WARNING,
            '40':logging.ERROR, '50':logging.CRITICAL}

def parse(path, **kwargs):
    ## logging configuration
    create_logger(log_lvls.get(kwargs.get('log_lvl', '10')))
    
    with open(util.toAST(path, 'java'), 'r') as fd:
        d = json.load(fd)
        d.update({u'GSYMTAB':'RESET'})
        logging.info('parsing file...')
        program = CompilationUnit(d)
        
        s = SymtabGen()
        logging.info('generating symbol table...')
        s.visit(program)
        logging.info('building class heirarchy...')
        utils.build_subs(program)

    return program

def create_logger(log_lvl):
    # create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level
    h = logging.StreamHandler()
    h.setLevel(log_lvl)
    formatter = logging.Formatter(fmt='%(asctime)s %(message)s', datefmt='%I:%M:%S') # create formatter
    h.setFormatter(formatter) # add formatter to h
    logger.addHandler(h) # add h to logger

    # create file handler and set level
    h = logging.FileHandler(os.path.join(pwd, 'logs', 'log.txt'))
    h.setLevel(log_lvl)
    formatter = logging.Formatter(fmt='{} %(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d %(message)s', datefmt='%I:%M:%S')
    h.setFormatter(formatter) # add formatter to h
    logger.addHandler(h) # add h to logger
    
if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options]* [FILE]+")
    
    parser.add_option("-r", "--reach",
                      action="store_true", dest="reach", default=False,
                    help="whether or not to do reaching defs")
    parser.add_option("-f", "--dataflow",
                      action="store_true", dest="dataflow", default=False,
                    help="whether or not to do dataflow analysis")
    parser.add_option("-i", "--inputs",
                      action="store_true", dest="inputs", default=False,
                      help="do input analysis")
    parser.add_option("-e", "--expr",
                      action="append", type="int", dest="e", default=[],
                      help="start and stop nodes for i/o")
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="print intermediate messages verbosely")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print dataflow results")
    parser.add_option("-s", "--symtab",
                      action="store_true", dest="symtab", default=False,
                      help="Print symbol tables")
    parser.add_option("-l", "--log_lvl",
                      action="store", dest="log_lvl", default='10',
                      help="level of logging")
    
    (OPT, argv) = parser.parse_args()
    
    if len(argv) < 1: exit("incorrect number of arguments: missing program(s)")
    program = parse(argv, **vars(OPT))

    if OPT.dataflow:
        d = DataFlow()
        d.analyze(program, program.gsymtab, vars(OPT))
    else:
        if OPT.symtab:
            def f(n):
                if type(n) not in SymtabGen.NONSYM:
                    print type(n).__name__, n.name, map(lambda nn: (nn[0], nn[1]), n.symtab.items())
            g = GenericVisitor(f)
            g.visit(program)
        else:
            p = SourcePrinter()
            print p.visit(program)
    exit(0)