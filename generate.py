import getopt
import os
import re
import shutil
import subprocess
import sys
import tempfile
import yaml

# ----------------------
# VARIABLES
# ----------------------


file_defined = False
config_file_default = 'config.yaml'
config_file = ""

username_param_keys = ["username", "user"]
reponame_param_keys = ["reponame", "repo", "repository"]
artifact_param_keys = ["artifact", "maven-artifact"]
group_param_keys = ["group", "mavengroup", "maven-group"]
package_param_keys = ["pkg", "package", "packagename", "package-name"]

username_key = "username"
reponame_key = "reponame"
artifact_key = "artifact"
group_key = "group"
package_name_key = "package_name"
codecov_key = "codecov"
publish_key = "publish"

src_reponame = 'release-please-template'
git_src_repo = 'https://github.com/state303/release-please-template-gradle.git'

# ----------------------
# FUNCTIONS
# ----------------------


def get_config_filepath():
    argv = sys.argv[1:]
    try:
        opts, _ = getopt.getopt(argv, "f:", ["file="])
    except getopt.GetoptError:
        print('create.py -f <config_file>')
        sys.exit(2)
    # read flags
    for opt, arg in opts:
        if opt in ("-f", "--file"):
            print('setting target config: {}'.format(arg))
            return arg
    return config_file_default


def translate_key(src_key):
    if src_key in username_param_keys:
        return username_key
    elif src_key in reponame_param_keys:
        return reponame_key
    elif src_key in artifact_param_keys:
        return artifact_key
    elif src_key in group_param_keys:
        return group_key
    elif src_key in package_param_keys:
        return package_name_key
    elif src_key == codecov_key or src_key == publish_key:
        return src_key
    return ""


def load_config(filepath):
    file_specified = filepath != config_file_default
    found = os.path.exists(os.path.join(os.getcwd(), filepath))

    if file_specified and not found:
        print('failed to locate file: {}'.format(filepath))
        sys.exit(2)

    values = {}
    config_keys = [username_key, reponame_key,
                   artifact_key, group_key, package_name_key, codecov_key, publish_key]

    # set found configs into target values
    if found:
        with open(filepath, 'r') as stream:
            user_settings = yaml.safe_load(stream)
            for user_defined_key in user_settings:
                key = translate_key(user_defined_key)
                if len(key) == 0:  # unknown key
                    print('unknown key: {}. please try again'.format(
                        user_defined_key))
                    sys.exit(2)
                # mark as config set
                if key in config_keys:
                    config_keys.remove(key)
                # always overwrite
                values[key] = user_settings[user_defined_key]

    # fill missing settings with default values
    # if no config was given, missing_configs will have all required fields to be set
    for key in config_keys:
        if key == codecov_key or key == publish_key:
            values[key] = "false"
            continue
        values[key] = "<YOUR_{}_VALUE>".format(key.upper())

    for key in [codecov_key, publish_key]:
        v = str(values[key]).lower()
        if v in ['yes', 'y', 't', 'true', '1']:
            values[key] = True
        elif v in ['no', 'n', 'f', 'false', '0']:
            values[key] = False 
        else:
            print("unknown value for {}: found {}".format(
                key, values[key]))

    return values


def sed_inline(filepath, pattern, repl):
    pattern_compiled = re.compile(pattern)
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        with open(filepath) as src_file:
            for line in src_file:
                tmp_file.write(pattern_compiled.sub(repl, line))
    shutil.copystat(filepath, tmp_file.name)
    shutil.move(tmp_file.name, filepath)


# ----------------------
# RUN
# ----------------------

# read flags
config_path = get_config_filepath()

# load configs
values = load_config(config_path)

# report values
print("setting with following values")
for key in values:
    print("{}: {}".format(key, values[key]))

# clone then move direcotry, dig 1 level into target repository dir
reponame = values[reponame_key]
cDir = os.getcwd()
clPath = os.path.join(cDir, src_reponame)
cpPath = os.path.join(cDir, reponame)

for p in [clPath, cpPath]:
    if os.path.exists(p):
        print('directory already exists: {}'.format(clPath))
        sys.exit(2)

subprocess.run(["git", "clone", git_src_repo])
shutil.move(clPath, cpPath)
os.chdir(cpPath)

# reset changelog
fd = os.open('CHANGELOG.md', os.O_RDWR | os.O_CREAT)
os.truncate(fd, 0)
os.close(fd)

repoRootDir = os.getcwd()
targetPath = os.path.join(repoRootDir, 'gradle.properties')

github_repo = values[username_key] + "/" + values[reponame_key]
v = 'maven_group = ' + values[group_key]
sed_inline(targetPath, r'maven_group.*', v)
v = 'github_repo = ' + github_repo
sed_inline(targetPath, r'github_repo.*', v)
v = 'artifact_version = 0.0.0'
sed_inline(targetPath, r'artifact_version.*', v)
v = 'rootProject.name = ' + values[artifact_key]
targetPath = os.path.join(repoRootDir, 'settings.gradle')
sed_inline(targetPath, r'rootProject.name.*', v)
v = 'package-name: ' + values[package_name_key]
targetPath = os.path.join(repoRootDir, '.github', 'workflows', 'release.yml')
sed_inline(targetPath, r'package-name.*', v)

# in case publish is true
if values[publish_key]:
    for line in ['#     - name: 🚀 Publish new package',
                 '#       run: ./gradlew publish',
                 '#       env:',
                 '#         GITHUB_']:
        sed_inline(targetPath, line, line.replace("#", " "))

targetPath = os.path.join(repoRootDir, '.github', 'workflows', 'build.yml')
# in case codecov is true
if values[codecov_key]:
    for line in ['#     - name: 🎯️ Upload codecov',
                 '#       uses: codecov/codecov-action@v3',
                 '#       with:',
                 '#         files: ']:
        sed_inline(targetPath, line, line.replace("#", " "))

        # remove previous java packages
shutil.rmtree(os.path.join(repoRootDir, 'src', 'main', 'java', 'io'))

# reset git
shutil.rmtree('.git')
subprocess.run(['git', 'init'])

os.remove('generate.py')

print('done')
