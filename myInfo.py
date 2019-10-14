import csv
from pathlib import Path
from project_pb2 import Project, Bug, Commit, Comment


def get_project_info(param):
    csv_file = Path("./Projects.csv")
    with csv_file.open() as infile:
        reader = csv.DictReader(infile, delimiter=";")
        for row in reader:
            if row["Name"] == param["project"]:
                print("\nProject info:")
                for key, value in row.items():
                    print("\t"+str(key)+": "+str(value))
                print("\n")


def get_bug_info(param):
    project_name = param["project"]
    bug_id = int(param["bug-ID"])
    directory = Path("./Projects") / project_name

    csv_file = directory / (project_name + "_bugs.csv")
    with csv_file.open() as infile:
        reader = csv.DictReader(infile, delimiter=";")
        for row in reader:
            if int(row["ID"]) == bug_id:
                print("Bug info:")
                for key, value in row.items():
                    print("\t"+str(key)+": "+str(value))
                print("\n")
    
    issues_file = directory / (project_name + "_issues.bin")
    proj = Project()
    with issues_file.open(mode="rb") as infile:
        proj.ParseFromString(infile.read())
    issues = [bug for bug in proj.bugs if bug.id == bug_id]
    issues.sort(key=lambda bug: bug.orig_id)
    print("Related discussion(s):")
    count = 0
    for issue in issues:
        count += 1
        print(f"{count}:")
        print(f"\tDescription:")
        print("\t\t" + "\n\t\t".join(issue.description.split("\n")))
        if len(issue.comments) > 0:
            print("\tComments:")
        for comment in issue.comments:
            print("\t\t" + "\n\t\t".join(comment.comment.split("\n")))
            print()
        print(f"\tURL: https://github.com/{proj.user}/{proj.repository}/issues/{issue.orig_id}")
        print(f"\tFix: https://github.com/{proj.user}/{proj.repository}/commit/{issue.fix.hash}")
        print()
