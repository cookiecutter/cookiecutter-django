import os
import re
from pprint import pprint


# script to check if licenses generated have placeholders not replaced
def check_scripts_for_placeholders():
    brackets = []
    for filename in os.listdir("../{{cookiecutter.project_slug}}/licenses"):
        file = open("../{{cookiecutter.project_slug}}/licenses/" + filename, encoding="utf8")

        # 'found' stores all found bracket instances
        found = []

        # dashes counts the '---\n' lines in the licenses.
        # it skips instances of brackets until after 2 as to skip the jekyll header
        dashes = 0
        for i, line in enumerate(file.readlines()):
            if line == "---\n":
                dashes += 1
            # skips any possible brackets until the jekyll header is skipped
            if dashes < 2:
                continue
            line = re.findall(r"\[.*\]", line)
            if line != []:
                found += (i, line)

        # add any found instances of placeholders to the brackets array
        # print it after the loop is executed
        if found != []:
            brackets += (filename, found)
    if len(brackets) > 0:
        print()
        pprint(brackets)
    assert len(brackets) == 0


if __name__ == "__main__":
    check_scripts_for_placeholders()
