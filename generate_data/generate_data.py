import argparse
from probgen import generateInstance
import os

nodeLimit = 2000000
run_cmd = 'gurobi_cl ResultFile={0} TimeLimit=3600 NodeLimit=%d LogFile={2} {1}'%nodeLimit

def main(outFolder, offset, max_n, min_n, g_type, edge, num_instances_per_dataset):
    print('Creating %s'%outFolder)
    os.system('mkdir -p %s'%outFolder)
    os.system('mkdir -p %s'%outFolder.replace('lpfiles', 'gpickle'))

    for i in range(num_instances_per_dataset):
        outPrefix = outFolder + '/input%d'%(offset+i)
        generateInstance(max_n, min_n, g_type, edge, outPrefix=outPrefix)

    return

def cmdLineParser():
    parser = argparse.ArgumentParser(description='Maximum cut')
    parser.add_argument('--outfile_dir', dest='outfile_dir', type=str, action='store', \
                      default='data/', help='Output Folder')
    parser.add_argument('--graph_type', dest='graph_type', type=str, action='store', \
                      default='erdos_renyi', help='Graph type')
    parser.add_argument('--num_instances_per_dataset', dest='num_instances_per_dataset', type=int, action='store', \
                      default=15, help='Number of instances of each type')
    parser.add_argument('--number_of_iterations', dest='number_of_iterations', type=int, action='store', \
                      default=1, help='Number of iterations to generate graphs for')
    parser.add_argument('--max_n', dest='max_n', type=int, action='store', \
                      default=20, help='max number of nodes')
    parser.add_argument('--min_n', dest='min_n', type=int, action='store', \
                      default=20, help='min number of nodes')
    parser.add_argument('--num_edges', dest='num_edges', type=int, action='store', \
                      default=20, help='number of edges to attach')
    return parser.parse_args()


def safe_mkdir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

if __name__ == '__main__':
    args = cmdLineParser()
    print("HERE")
    folders = ['train', 'test']
    min_n = args.min_n
    max_n = args.max_n

    if not os.path.isdir(args.outfile_dir):
        print("Creating data directory")
        os.mkdir(args.outfile_dir)

    for i, _ in enumerate(range(args.number_of_iterations)):
        # for each iteration, go and create a new set of train/test random graphs
        file_name_index_offset = 0
        for prefix in folders:

            # create outer directory
            outer_directory = os.path.join(args.outfile_dir, f"maxn_{max_n}_minn_{min_n}_numedges_{args.num_edges}")

            safe_mkdir(outer_directory)

            # create lpfile directory
            safe_mkdir(os.path.join(outer_directory, "lpfiles"))

            # create gpickle directory
            safe_mkdir(os.path.join(outer_directory, "gpickle"))

            lpfile_outdir = os.path.join(outer_directory, f"lpfiles/{prefix}")
            gpickle_outdir = lpfile_outdir.replace("lpfiles", "gpickle")
            safe_mkdir(lpfile_outdir)
            safe_mkdir(gpickle_outdir)

            # for each (iteration, dataset) go and create num_instances_per_dataset new graph instances
            for j in range(args.num_instances_per_dataset):
                outPrefix = lpfile_outdir + '/input%d' % (j + i)
                generateInstance(max_n, min_n, args.graph_type, args.num_edges, outPrefix=outPrefix)


