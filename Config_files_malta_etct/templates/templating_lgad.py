from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import subprocess
import numpy as np

def main():
    positions_x = [0]
    positions_z = np.linspace(-300, -360, 13)

    files_tot = []
    
    for x in positions_x:
        files = []
        for z in positions_z:
            print('Starting new simulation')
            filename = f'tcad_error_{x}_{z}'
            files.append(f'root_files/{filename}.root')
            print(f'Running Simulation {filename}')
            #new_simu(x, z, filename)
            if z == -360:
                files_tot.append(files)
                    
    print(files_tot)

def new_simu(x, z, filename):
    location = '/home/user280/allpix_folder/allpix-squared/install'
    
    if os.path.exists(f'{location}/lgad.conf'):
        print('Removing.conf file')
        os.remove(f'{location}/lgad.conf')

    env = Environment(
        loader=FileSystemLoader("./"),
        autoescape=select_autoescape()
    )

    elec_temp = env.get_template("lgad.conf.jinja")
    elec_render = elec_temp.render(x=x, z=z)
    with open(f'{location}/lgad.conf', 'w') as h:
        h.write(elec_render)

    subprocess.run(["bin/allpix", "-c", "lgad.conf"])
    print('Moving file')
    subprocess.run(["mv", f'{location}/output/modules.root', f'/home/user280/root_python/root_files/{filename}.root'])

    os.remove(f'{location}/lgad.conf')

if __name__ == '__main__':
    main()
