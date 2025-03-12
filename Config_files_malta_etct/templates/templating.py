from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import shutil
import argparse
import re
import subprocess

def main():
    bias_volt = []
    dep_volt = []
    positions = [40, 30, 20, 10, 0, -10, -20, -30, -40] 

    files_tot = []

    for b in bias_volt:
        for d in dep_volt:
            files = []
            for p in positions:
                filename = f'lin_{b}_{d}_{p}'
                files.append(f'{filename}.root')
                new_simu(b, d, p, filename)
                if p == -40:
                    files_tot.append(files)

def new_simu(bias, deplete, position, filename):
    electrode_location = '/home/user280/allpix_folder/allpix-squared/install'

    env = Environment(
        loader=FileSystemLoader("./"),
        autoescape=select_autoescape()
    )

    elec_temp = env.get_template("electrode.conf.jinja")
    elec_render = elec_temp.render(bias = bias, deplete = deplete, position = position)
    with open(f'{electrode_location}/electrode.conf', 'w') as h:
        h.write(elec_render)

    subprocess.run(["bin/allpix", "-c", "electrode.conf"])
    subprocess.run(["mv", f'{electrode_location}/output/modules.root', f'/home/user280/root_python/{filename}.root'])

    os.remove(f'{electrode_location}/src/electrode.conf')

if __name__ == '__main__':
    main()