from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import subprocess
import numpy as np

def main():
    bias_volt = [-545, -487, -333, -207, -192, 0, 76, 23, 208, 109, 290, 376]
    dep_volt = [10]
    positions = [40, 30, 20, 10, 0, -10, -20, -30, -40] 

    files_tot = []

    for b in bias_volt:
        for d in dep_volt:
            files = []
            for p in positions:
                print('Starting new simulation')
                filename = f'lin_{b}_{d}_{p}'
                files.append(f'root_files/{filename}.root')
                print(f'Running Simulation {filename}')
                new_simu(b, d, p, filename)
                if p == -40:
                    files_tot.append(files)
                    
    print(files_tot)

def new_simu(bias, deplete, position, filename):
    electrode_location = '/home/user280/allpix_folder/allpix-squared/install'
    
    if os.path.exists(f'{electrode_location}/electrode.conf'):
        print('Removing electrod.conf file')
        os.remove(f'{electrode_location}/electrode.conf')

    env = Environment(
        loader=FileSystemLoader("./"),
        autoescape=select_autoescape()
    )

    elec_temp = env.get_template("electrode.conf.jinja")
    elec_render = elec_temp.render(bias = bias, deplete = deplete, position = position)
    with open(f'{electrode_location}/electrode.conf', 'w') as h:
        h.write(elec_render)

    subprocess.run(["bin/allpix", "-c", "electrode.conf"])
    print('Moving file')
    subprocess.run(["mv", f'{electrode_location}/output/modules.root', f'/home/user280/root_python/root_files/{filename}.root'])

    os.remove(f'{electrode_location}/electrode.conf')

if __name__ == '__main__':
    main()