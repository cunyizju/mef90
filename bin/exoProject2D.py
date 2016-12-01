import sys

def parse():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile",  help = "The name of the exodus file to fix.", type = str)
    parser.add_argument("outputFile", help = "The name of the exodus file to be written.", type = str)
    args = parser.parse_args()
    return args


def main():
    import exodus as exo
    import numpy as np
    options = parse()
    
    print options
    
    exoin  = exo.exodus(options.inputFile,mode='r')
    numNodes    = exoin.num_nodes()
    numElems    = exoin.num_elems()
    numBlocks   = exoin.num_blks()
    numNodeSets = exoin.num_node_sets()

    exoout=exo.exodus(options.outputFile, mode='w',title=exoin.title(),numDims=2,numNodes=numNodes, 
                      numElems=numElems,numBlocks=numBlocks,numNodeSets=numNodeSets,numSideSets=0)

    exoout.put_coord_names(exoin.get_coord_names()[0:2])

    coord = exoin.get_coords()
    exoout.put_coords(coord[0],coord[1],coord[2])

    # cell sets
    blkids = exoin.get_elem_blk_ids()
    for id in blkids:
        blkName = exoin.get_elem_blk_name(id)
        (elemType,numElemInBlock,numNodesPerElem,numAttr) = exoin.elem_blk_info(id)
        exoout.put_elem_blk_info(id,elemType,numElemInBlock,numNodesPerElem,0) #ignoring attributes
        exoout.put_elem_connectivity(id,exoin.get_elem_connectivity(id)[0])

    # node sets
    setids = exoin.get_node_set_ids()
    for id in setids:
        # e.get_node_set_params() -> get number of nodes and distribution factors
        numNodes,numDistFactors = exoin.get_node_set_params(id)
        exoout.put_node_set_params(id,numNodes,numDistFactors)
        exoout.put_node_set_name(id,exoin.get_node_set_name(id))
        exoout.put_node_set(id,exoin.get_node_set_nodes(id))

    exoin.close()
    exoout.close()

if __name__ == "__main__":
        sys.exit(main())

