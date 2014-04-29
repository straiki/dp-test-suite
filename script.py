#!/usr/bin/python3
from __future__ import print_function
from subprocess import call
import sys
import os
import shutil
import random

models = os.path.abspath("models/")


def create_tests(_files):
    """It will create new test set.
    :param _files: list of files
    """

    print("-- Creating new tests..")

    for _file in _files:
        if not os.path.isfile(current + "/Model/" + _file) and _file.endswith(".jpg"):
            shutil.copyfile(original + "/" + _file, current + "/Model/" + _file)  # if its not there, copy it

    localization = random.sample(_files, min(5, max(int(len(_files) / 10), 2)))

    # print("rm " + current + "/Localization/*.jpg")
    print("-- -- Cleaning Localization directory")
    call("rm " + current + "/Localization/*.jpg", shell=True)

    print("-- -- Moving randomly selected files..")
    for _file in localization:  # move randomly selected files
        call("mv " + current + "/Model/" + _file + " " + current + "/Localization/" + _file.lstrip(), shell=True)

    #create model from rest of files
    print("-- -- Creating ref model from rest")
    _ret = call("./CreateModel " + current + "/Model true > " + current + "/Model" + "/output.txt 2>&1", shell=True)
    print("-- -- -- Done")
    if _ret != 0:
        return False  # means that from this set its not possible to create model

    for _file in localization:
        print("-- -- Localizing " + _file)
        _ret = call("./model_localization " + current + "/Model/model_data.yaml " + current + "/Localization/"
                    + _file + " true > " + current + "/Localization/" + _file + ".txt ", shell=True)
        # print("-- -- -- " + str(_ret))
        if _ret != 0:
            return False  # unable to locate cam
        if os.path.isfile(current + "/Model/output.yaml"):
            call("mv " + current + "/Model/output.yaml " + current + "/Localization/" + _file + ".yaml", shell=True)
        else:
            print("File '" + current + "/Model/output.yaml' not found")

    return True


if __name__ == "__main__":

    print("Test suite for my DP\n" + models)

    if len(sys.argv) == 2:
        directory = sys.argv[1]
        print("Getting: " + directory)
        if not os.path.exists(models + "/" + directory):
            print("Does not exists! Exiting..")
            exit()
    else:
        directory = sys.stdin.readline()
        directory = directory.rstrip()

    # sys.stdout.write(directory)

    path = models + "/" + directory
    reference = path + "/Reference"
    current = path + "/Current"
    original = path + "/Original"

    if not os.path.isdir(reference):
        os.mkdir(reference)

    if not os.path.isdir(current):
        os.mkdir(current)

    tmp = os.listdir(original)

    files = [file for file in tmp if file.endswith(".jpg")]

    if len(files) <= 0:
        print("Missing pictures! Exiting..")
        exit()

    for file in files:
        if not os.path.isfile(reference + "/" + file) and file.endswith(".jpg"):
            shutil.copyfile(original + "/" + file, reference + "/" + file)  # if its not there, copy it

    if not os.path.isfile(reference + "/model_data.yaml"):
        ret = call("./CreateModel " + reference + " true > " + reference + "/output.txt 2>&1", shell=True)
        if ret != 0:
            exit("Failed to create reference model..")

    print("-- Reference model created")

    counter = 0
    while True:
        counter += 1
        ret = create_tests(files)
        if ret:
            break
        else:
            if counter > 1000:
                exit("Failed ten ten ten times!")
            print("Failed to create model.. trying again.. " + str(counter))

