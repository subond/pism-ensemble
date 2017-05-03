
import os
import jinja2
import subprocess
import itertools
import hashlib

def write_pism_runscript(up_settings, template, runscript_path, **kwargs):

    """ This writes a PISM run script.
    """

    # make jinja aware of templates in the templates folder
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
                searchpath=os.path.join(up_settings.project_root,"templates")))

    scen_template = jinja_env.get_template(template)
    out = scen_template.render(**kwargs)

    script_to_write = os.path.join(runscript_path,template.replace("template.",""))

    with open(script_to_write, 'w') as f:
        f.write(out)
    subprocess.check_call("chmod u+x "+script_to_write, shell=True)

    print "Wrote",script_to_write


def span_ensemble(ensemble_variables,use_numbers=False,
                 start_number=0):

    parameter_combinations = list(itertools.product(*ensemble_variables.values()))
    parameter_names = ensemble_variables.keys()

    ensemble_members = {}

    for i,pc in enumerate(parameter_combinations):

        if use_numbers:
            em_id = i + start_number
        else:
            em_id = hashlib.sha224(str(pc)).hexdigest()[0:10]

        em_params = {name:pc[i] for i,name in enumerate(parameter_names)}
        ensemble_members[em_id] = em_params

    return parameter_names,ensemble_members