def PrepareJob(Geometry,Parameters,debug=False):
    import hashlib
    import shutil
    import os
    import sys
    
    Parameters['hash'] = hashlib.sha1(repr(Geometry)).hexdigest()
    if os.getenv('PBS_JOBID'):
        Parameters['jobid'] = os.getenv('PBS_JOBID')
    elif os.getenv('JOB_ID'):
        Parameters['jobid'] = os.getenv('JOB_ID')
    else:
        Parameters['jobid'] = '0000'
     
    ### 
    ### Create a long file prefix if necessary
    ###
    if Parameters['prefix']:
        for k in sorted(Geometry.keys()):
            Parameters['prefix'] +='-%s_%s'%(k,Geometry[k])
    else:
        Parameters['prefix'] = Parameters['jobid']
    
    
    ###
    ### Find where the script was submitted from
    ###
    if os.getenv('PBS_O_WORKDIR'):
        # We are runnning inside a PBS job 
        submitdir = os.getenv('PBS_O_WORKDIR')
    elif os.getenv('SGE_O_WORKDIR'):
        # We are running inside a SGE job
        submitdir = os.getenv('SGE_O_WORKDIR')
    else:
        # We are running in interactive mode
        submitdir = os.getcwd()

    ###
    ### Set workdir
    ###
    if Parameters['workdir']:
        ###
        ### Try to figure out if workdir is a relative or absolute path
        ### 
        if not args.workdir[0] == '/':
            Parameters['workdir'] = os.path.join(submitdir,args.workdir)
    else:
        if os.getenv('PBS_O_WORKDIR'):
            # We are runnning inside a PBS job 
            Parameters['workdir'] = os.path.join(os.getenv('PBS_O_WORKDIR'),Parameters['jobid'])
        elif os.getenv('SGE_O_WORKDIR'):
            # We are running inside a SGE job
            Parameters['workdir'] = os.path.join(os.getenv('SGE_O_WORKDIR'),Parameters['jobid'])
        else:
            # We are running in interactive mode
            Parameters['workdir'] = os.path.join(os.getcwd(),Parameters['jobid'])
       
    ###
    ### Find the argument file
    ### Try  absolute path then submission directory, then script directiry
    ### 
    for root in ['/',submitdir,os.path.dirname(os.path.abspath(__file__))]:
        if debug:
            print 'searching for argfile in %s'%root
        if os.path.isfile(os.path.join(root,Parameters['argfile'])):
            Parameters['argfile'] = os.path.join(root,Parameters['argfile'])
            break

    ###
    ### Find the meshes location
    ### Try  absolute path then submission directory, then script directory
    ### 
    for root in ['/',submitdir,os.path.dirname(os.path.abspath(__file__))]:
        if debug:
            print 'searching for meshdir in %s'%root
        if os.path.isdir(os.path.join(root,Parameters['meshdir'])):
            Parameters['meshdir'] = os.path.join(root,Parameters['meshdir'])
            break

    if not os.path.isdir(Parameters['meshdir']):
        print 'meshdir %s does not exist, giving up'%Parameters['meshdir']
        sys.exit(-1)

        
    Parameters['MEF90_DIR'] = os.getenv("MEF90_DIR")
    Parameters['PETSC_DIR'] = os.getenv("PETSC_DIR")
    Parameters['PETSC_ARCH'] = os.getenv("PETSC_ARCH")
    Parameters['scriptdir'] = os.path.dirname(os.path.abspath(__file__))
    
    return Parameters
