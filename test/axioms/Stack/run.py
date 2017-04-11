import subprocess
import re
import math

def main(num_trials, test):
    result_file = 'results/{}.csv'.format(test)
    error_file = 'errors/{}.txt'.format(test)
    log_file = 'logs/{}.txt'.format(test)
    input_dir = 'input_{}'.format(test)
    with open(result_file, 'w') as f: pass
    with open(error_file, 'w') as f: pass
    with open('{}/test.sk'.format(input_dir)) as f: text = f.read()
    log = open(log_file, 'w')
    num_tests=int(re.findall(r't[0-9]+', text)[-1][1:]) + 1
    for i in range(num_tests):
        print 'Running test {}'.format(i)
        times = []
        for j in range(num_trials):
            cmd = ['sketch', '--fe-def', 'TID={}'.format(i), '--fe-inc', input_dir, '{}/main.sk'.format(input_dir)]
            log.write('test: {}, trial: {}, cmd: {}\n'.format(i, j, ' '.join(cmd)))
            log.flush()
            try:
                t = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
                start = t.rfind('Total time = ') + len('Total time = ')
                times.append(float(t[start:t.find('\n', start)]))
            except:
                print 'ERROR: {}'.format(' '.join(cmd))
                with open(error_file, 'a') as f: f.write('{}\n'.format(' '.join(cmd)))
                times.extend([0.0]*num_trials)
                break
        with open(result_file, 'a') as f:
            [f.write('{:.2f}\t'.format(n)) for n in times]
            f.write('\n')
    sort_results(test)

def sort_results(test):
    result_file = 'results/{}.csv'.format(test)
    sorted_result_file = 'results/{}_s.csv'.format(test)
    with open(result_file,'r') as fd:
        lines = fd.readlines()
    # do it all on one line! (split line, convert to float, sort)
    res = map(lambda l: sorted(map(float, l.strip('\n\t').split('\t') if l.split('\t') != [''] else [0])), lines)
    with open(sorted_result_file, 'w') as fd:
        for r in res: fd.write('{}\n'.format('\t'.join(map(str,r))))
    
if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options]*")
    parser.add_option('-i', action='store_true', dest='impl', default=False,
                      help='Execute implementation tests.')
    parser.add_option('-a', action='store_true', dest='adt', default=False,
                      help='Execute adt tests.')
    parser.add_option('-o', action='store_true', dest='obj', default=False,
                      help='Execute Object tests.')
    parser.add_option('-n', action='store', type='int', dest='trials', default=1,
                      help='Number of trials to run.')
    (options, args) = parser.parse_args()
    print 'Number of trials: {}'.format(options.trials)
    if options.impl:
        print 'Testing implementation'
        main(options.trials, 'impl')
        print
    if options.adt:
        print 'Testing adt'
        main(options.trials, 'adt')
        print
    if options.obj:
        print 'Testing Object'
        main(options.trials, 'Object')
        print
    if (not options.impl) and (not options.adt) and (not options.obj):
        print 'Testing implementation'
        main(options.trials, 'impl')
        print 'Testing adt'
        main(options.trials, 'adt')
        print 'Testing Object'
        main(options.trials, 'Object')