import os
from templateframework.metadata import Metadata

def run(metadata: Metadata = None):
    output = "ck-output"

    def find_jar():
        import glob
        home = os.path.expanduser('~')

        for file in glob.glob(home + "/.stk/stacks/*/plugin-flacoco/flacoco.jar"):
            return os.path.abspath(file)

    def run_cmd(command):
        import subprocess
        result = subprocess.run(command,
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True)
        return result

    def run_inside_a_stack():
        dir_jar = find_jar()
        target_project = str(metadata.target_path)
        return ["java", "-jar", dir_jar, target_project]

    def run_outsite_a_stack():
        dir_jar = os.path.join(str(metadata.target_path), str(metadata.component_path), "flacoco.jar")
        
        import questionary
        target_project = questionary.path("What's the path to the project you want to analyze?").ask()

        return ["java", "-jar", dir_jar, "-p", target_project, "--format=JSON"]

    print("Runing Jacoco fault localization metrics..")

    command = run_outsite_a_stack()

    result = run_cmd(command)

    if result.returncode == 0:
        output = result.stdout.split("\n")

        with open("facoco.json", "w") as json:
            json.write(output[-1])

        #for item in result.stdout.split("\n"):
        #   print(item)

        print("Output written at the facoco.json file")
    else:
        for item in result.stderr.split("\n"):
           print(item)
            
    return metadata