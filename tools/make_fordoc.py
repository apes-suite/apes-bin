def gendoc(task):
    """ A Task rule to generate Documentation with FORD

        The rule expects the location of the mainpage with the
        FORD project description as task generator argument 'mainpage'.
        The location of the index.html that is to be generated, should
        be the first target argument.
        All unique parent nodes of the files given as sources will be
        used as src_dir for the FORD command.
        Pathes to external projects can be provided to the generator via
        the 'extern' argument.
    """
    import os
    tgt_path = os.path.dirname(task.outputs[0].abspath())
    src_paths = set()
    if not hasattr(task.generator, 'extern'):
        task.generator.extern = []
    for srcfile in task.inputs:
        if srcfile not in task.generator.extern:
            src_paths.add(srcfile.parent.abspath())
    cmd = ['ford', '--externalize', '-o', tgt_path]
    if hasattr(task.env, 'revision_string'):
        cmd.append('-r')
        cmd.append(task.env.revision_string)
    for spath in src_paths:
        cmd.append('-d')
        cmd.append(spath)
    for elink in task.generator.extern:
        cmd.append('-L')
        cmd.append(elink.parent.abspath())
    cmd.append(task.generator.mainpage)
    return task.exec_command( cmd, shell=False, cwd=task.generator.bld.top_dir )
