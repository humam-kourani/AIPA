import os
import subprocess
import time
import pathlib
import shutil

CURRENT_DIRECTORY = os.getcwd()
directories = os.listdir(CURRENT_DIRECTORY)
NON_ANGULAR_DIRS = ['static', 'templates', 'venv']


ANGULAR_PROJECT_PATH = pathlib.PureWindowsPath(os.path.join(CURRENT_DIRECTORY, 'frontend'))
DIST_PATH = pathlib.PureWindowsPath(os.path.join(ANGULAR_PROJECT_PATH, 'dist', 'frontend', 'browser'))

FLASK_STATIC_PATH = pathlib.PureWindowsPath(os.path.join(CURRENT_DIRECTORY, 'static'))
FLASK_TEMPLATES_PATH = pathlib.PureWindowsPath(os.path.join(CURRENT_DIRECTORY, 'templates'))

subprocess.Popen(('cd ' + str(ANGULAR_PROJECT_PATH) + ' && ng build --watch --base-href=/static/ &'), shell=True)

dir_exists = True

while dir_exists:
    try:
        files = os.listdir(DIST_PATH)
        build_files = []
        for file in files:
            if '.js' in file or '.js.map' in file or '.ico' in file:
                build_files.append({'src': str(DIST_PATH) + '\\' + file, 'dest': str(FLASK_STATIC_PATH) + '\\' + file})
            if '.html' in file:
                build_files.append({'src': str(DIST_PATH) + '\\' + file, 'dest': str(FLASK_TEMPLATES_PATH) + '\\' + file})

        if len(build_files) > 0:
            for file in build_files:
                if os.name == 'nt':  # Windows
                    src = file['src'].replace('\\', '/')
                    dest = file['dest'].replace('\\', '/')
                    cmd = f'copy "{src}" "{dest}"'
                    arg = ['copy', file['src'].replace('\\', '/'), file['dest'].replace('\\', '/')]
                else:
                    arg = ['cp', file['src'].replace('\\', '/'), file['dest'].replace('\\', '/')]
                #aa =  os.path.isfile(file['src'].replace('\\', '/'))
                #status = subprocess.call(cmd, shell=True)
                shutil.copyfile(file['src'].replace('\\', '/'), file['dest'].replace('\\', '/'))

    except Exception as e:
        dir_exists = False
        print(e)
    time.sleep(10.0)
