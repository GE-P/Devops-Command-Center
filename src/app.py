# Name : Devops_Command_Center
# Version : Alpha
# Author : GE-P
# INFO : The app main core actions.
# --------------------------------- #

import datetime
from flask import Flask, render_template, request, url_for, redirect, session, flash
import requests
import urllib3
from werkzeug.utils import secure_filename
from datetime import timedelta
import os
import gitlab
import urllib3
from colorama import Fore
import inflection
import pymsteams
from dotenv import load_dotenv
import json
import time
from threading import Thread

# import controllers
from controllers import auth

# Load environment variables
load_dotenv()

# Misc
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'yml'}

app = Flask(__name__)
app.register_blueprint(auth.auth)
app.config['SECRET_KEY'] = os.getenv('SECRET')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.permanent_session_lifetime = datetime.timedelta(minutes=60)
# app.config['Permanent_session_lifetime'] = timedelta(minutes=1)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'PRIVATE-TOKEN': os.getenv('TOKEN'),
}


# response = requests.get('https://gitlab.kelenn.lan/api/v4/projects/?per_page=100', headers=headers, verify=False)
#
# projects = response.json()
# # print(json.dumps(projects, indent=4))
# for p in projects:
#     print("Project name: " + p['name'] + " - Url: " + p['web_url'])
def hided_process():
    i = 0
    while i <= 10:
        time.sleep(1)
        print('toto')
        i += 1


# Index page with login redirection if not connected
@app.route('/')
def index():
    if 'loggedin' in session:
        p = Thread(target=hided_process)
        p.start()
        return render_template('index.html', isIndex=True)
    return redirect(url_for('auth.login'))


# Index page with login redirection if not connected
@app.route('/projects')
def projects():
    if 'loggedin' in session:

        # ---------- OLD
        # contents = []
        # dico_filtered = {}
        #
        # response_projects = requests.get('https://gitlab.kelenn.lan/api/v4/projects/?per_page=100', headers=headers,
        #                                  verify=False)
        # projects = response_projects.json()
        # # print(json.dumps(projects, indent=4))
        #
        # # Determine what projects have a CI
        # for project in projects:
        #     response_file_tree = requests.get(
        #         'https://gitlab.kelenn.lan/api/v4/projects/' + str(project['id']) + '/repository/tree', headers=headers,
        #         verify=False)
        #     if response_file_tree.status_code == 200:
        #         files = response_file_tree.json()
        #         # print(files)
        #         for file in files:
        #             if file['name'] == ".gitlab-ci_project01.yml":
        #                 response_time = requests.get(
        #                     'https://gitlab.kelenn.lan/api/v4/projects/' + str(project['id']) + '/jobs?page=1',
        #                     headers=headers, verify=False)
        #                 times = response_time.json()
        #                 dico_time = {}
        #                 # time_list = []
        #                 count = 0
        #                 pipeline_id = 0
        #                 for values in times:
        #                     # count += 1
        #                     # print(values['stage'])
        #                     # print(str(values['duration']) + " sec")
        #                     # for keys in values['pipeline']:
        #                     if values['pipeline']['id'] != pipeline_id:
        #                         if count != 0:
        #                             dico_time[str(values['pipeline']['created_at'])] = str(count)
        #                             # print(dico_time)
        #                             # time_list.append(str(count))
        #                             # print("\n" + "     Total time elapsed: " + str(count) + " sec")
        #                         # print("\nPipeline ID: " + str(values['pipeline']['id']) + " - URL: " + values['pipeline'][
        #                         #     'web_url'])
        #                         # print("     Commit message: " + values['commit']['title'] + "\n")
        #                         pipeline_id = values['pipeline']['id']
        #                         # pipeline_date = values['pipeline']['created_at']
        #                         count = 0
        #                     # elif values['pipeline']['id'] == pipeline_id:
        #                     #     print("     " + values['stage'] + " : " + str(values['duration']) + " sec")
        #                     #     count += values['duration']
        #                     # print(count)
        #                     # print("Pipeline ID: " + str(values['pipeline']['id']))
        #                     # print("     " + values['stage'] + " : " + str(values['duration']) + " sec" + " - STATUS: " +
        #                     #       values['status'])
        #                     if values['duration'] is not None:
        #                         count += values['duration']
        #
        #                 if dico_time:
        #                     key_one = next(iter(dico_time))
        #                     # print(key_one)
        #                 if key_one != '2022-09-16T08:14:22.957Z':
        #                     sec = dico_time[key_one]
        #                     # print(sec)
        #                 # dico_time[key_one]
        #                 data = {
        #                     "project_name": project['name'],
        #                     "url": project['web_url'],
        #                     "CI-CD": "9989",
        #                     "time": sec,
        #                     "date": key_one[:-14],
        #                     "month": key_one[:-14].split("-")[1],
        #                     "year": key_one[:-14].split("-")[0],
        #                 }
        #                 contents.append(data)
        #                 dico_filtered[project['name']] = 1
        #
        # # Determine what projects don't have a CI
        # for project in projects:
        #     if project['name'] not in dico_filtered:
        #         data = {
        #             "project_name": project['name'],
        #             "url": project['web_url'],
        #             "CI-CD": "10060",
        #             "time": "",
        #             "date": "",
        #         }
        #         contents.append(data)
        # ---------- OLD

        # # -------------------------- Projects list
        # page_project = 1
        # project_dico = {}  # --- Dico with projects names and projects ID's
        # project_dico_url = {}  # --- Dico with projects names and their URLs
        #
        # # project_list_with_ci = []
        # project_dico_with_ci = {}  # --- Dico with projects containing CI's
        # project_dico_no_ci = {}  # --- Dico with projects not containing CI's
        #
        # project_pipeline_execution_time = {}  # --- Dico with project name and last pipeline execution
        #
        # content_dico = {}  # --- Dico to store all data for further html parsing
        #
        # # --- Getting the header response to know the maximum number of pages for results --> Gitlab pagination, see Gitlab doc
        # response_projects = requests.get('https://gitlab.kelenn.lan/api/v4/projects/?per_page=100&page=1',
        #                                  headers=headers, verify=False)
        #
        # header_project = response_projects.headers["X-Total-Pages"]
        # # print(header_project)
        #
        # # --- Parsing all the projects with their respective ID's
        # while page_project <= int(header_project):
        #
        #     response_projects = requests.get(
        #         'https://gitlab.kelenn.lan/api/v4/projects/?per_page=100&page=' + str(page_project), headers=headers,
        #         verify=False)
        #
        #     projects = response_projects.json()
        #
        #     for project in projects:
        #         if project['name'] not in project_dico:
        #             project_dico[project['name']] = project['id']
        #             project_dico_url[project['name']] = project['web_url']
        #
        #             content_dico[project['name']] = {
        #                 "url": project['web_url'],
        #                 "CI-CD": "",
        #                 "time": "",
        #                 "date": "",
        #                 "status": "",
        #             }
        #
        #     page_project += 1
        #
        # # print("#### Project name + ID's ####")
        # # print(project_dico)
        # # print("#### Project name + URL ####")
        # # print(project_dico_url)
        #
        # # --- Filtering projects with CI's
        # for data in project_dico:
        #
        #     project_name = data
        #     project_id = project_dico[data]
        #
        #     # print(project_dico[data])
        #
        #     response_file_tree = requests.get(
        #         'https://gitlab.kelenn.lan/api/v4/projects/' + str(project_id) + '/repository/tree', headers=headers,
        #         verify=False)
        #
        #     if response_file_tree.status_code == 200:
        #
        #         files = response_file_tree.json()
        #
        #         # print(files)
        #
        #         for file in files:
        #             # print(file['name'])
        #             if file['name'] == ".gitlab-ci_project01.yml":
        #                 # project_list_with_ci.append(project_name)
        #                 project_dico_with_ci[project_name] = project_id
        #
        #                 content_dico[project_name]['CI-CD'] = "9989"
        #
        # # --- Filtering projects without CI's
        # for data in project_dico:
        #
        #     project_name = data
        #     project_id = project_dico[data]
        #
        #     if project_name not in project_dico_with_ci:
        #         project_dico_no_ci[project_name] = project_id
        #
        #         content_dico[project_name]['CI-CD'] = "10060"
        #
        # # print("##### with CI ######")
        # # print(project_dico_with_ci)
        # # print("##### No CI #####")
        # # print(project_dico_no_ci)
        # # print(project_list_with_ci)
        #
        # # --- Calculating last time execution of pipelines for each project containing a CI
        # for data in project_dico_with_ci:
        #
        #     dico_status = {}
        #
        #     project_name = data
        #     project_id = project_dico_with_ci[data]
        #
        #     pipeline = requests.get(
        #         'https://gitlab.kelenn.lan/api/v4/projects/' + str(project_id) + '/pipelines?per_page=1&page=1',
        #         headers=headers, verify=False)
        #
        #     pipe = pipeline.json()
        #
        #     # print("pipelines")
        #     # print(pipe)
        #     # print(pipe[0]['id'])
        #     # print("################################")
        #
        #     count = 0
        #     pipeline_id = 0
        #
        #     response = requests.get(
        #         'https://gitlab.kelenn.lan/api/v4/projects/' + str(project_id) + '/pipelines/' + str(
        #             pipe[0]['id']) + '/jobs', headers=headers, verify=False)
        #
        #     data = response.json()
        #
        #     # print(data)
        #
        #     if data:
        #         for values in data:
        #
        #             # print(values)
        #
        #             if values['pipeline']['id'] != pipeline_id:
        #                 # print("\n// ---- " + project_name + " ---- " + "Pipeline ID: " + str(
        #                 #     values['pipeline']['id']) + " - URL: " + values['pipeline'][
        #                 #           'web_url'] + " - Created: " + str(
        #                 #     values['pipeline']['created_at'])[:-14])
        #                 # print("     Commit message: " + values['commit']['title'] + "\n")
        #                 pipeline_id = values['pipeline']['id']
        #                 # count = 0
        #
        #                 content_dico[project_name]['date'] = str(values['pipeline']['created_at'])[: -14]
        #
        #             # print("     " + values['stage'] + " : " + str(values['duration']) + " sec" + " - STATUS: " + values[
        #             #     'status'])
        #
        #             if values['duration'] is not None:
        #                 count += values['duration']
        #
        #             if values['status'] == "failed" and project_name not in dico_status:
        #                 dico_status[project_name] = "Failed"
        #
        #
        #         if count != 0:
        #             # print("\n" + "     Total time elapsed: " + str(count) + " sec")
        #
        #             content_dico[project_name]['time'] = str(count)
        #
        #         if dico_status:
        #             # print("\n" + "     Status: " + str(dico_status[project_name]))
        #             content_dico[project_name]['status'] = "Failed"
        #         else:
        #             # print(dico_status)
        #             # print(data)
        #             # print("\n" + "     Status: Success")
        #             content_dico[project_name]['status'] = "Success"
        #     #     # elif count == 0:
        #     #     #     print("\n" + "     Total time elapsed:  NONE -- Canceled or Skipped")
        #     #
        #     # else:
        #     #     print("\n// ---- " + project_name + " ---- " + "Skipped")
        #
        # # print(content_dico)
        #
        # # return render_template('projects.html', projects=projects)
        # sorted_content = dict(sorted(content_dico.items(), key=lambda x: x[1]['CI-CD'], reverse=True))
        #
        # with open("projects.json", "w") as fp:
        #     json.dump(sorted_content, fp, indent=4)

        with open("projects_example.json", "r") as of:
            json_obj = json.load(of)

        # print(json_obj)

        # print(sorted_content)
        # return render_template('projects.html', contents=sorted_content)
        return render_template('projects.html', contents=json_obj)
    return redirect(url_for('auth.login'))


# @app.route('/metrics/<int:year>/<int:month>/<string:project>')
# def metrics(year, month, project):
#     return render_template('metrics.html')


@app.route('/metrics/<string:project>')
def metrics_project(project):
    data = {
        "url": "https://www.google.com",
        "CI-CD": "9989",
        "time": "100",
        "date": "22-05-2023",
    }
    contents = {"project_test": data}
    return render_template('metrics.html', contents=contents)


# Statistics page logic
@app.route('/stats', methods=['GET', 'POST'])
def stats():

    if 'loggedin' in session:
        # Define Plot Data
        labels = [
            'Janvier',
            'Fevrier',
            'Mars',
            'Avril',
            'Mai',
            'Juin',
            'Juillet',
            'Aout',
            'Septembre',
            'Octobre',
            'Novembre',
            'Decembre',
        ]

        data = [0, 10, 15, 8, 22, 18, 25, 8, 22, 18, 20, 16]

        contents = ["project_01", "project_02", "project_03", "project_04", "project_05", "project_06"]

        # Return the components to the HTML template
        return render_template(
            'stats.html',
            data=data,
            labels=labels,
            contents=contents
        )

        # return render_template('stats.html', date=graph_time, values=graph_values)
    return redirect(url_for('auth.login'))


# CI-CD page logic
@app.route('/cicd', methods=['GET', 'POST'])
def cicd():
    if 'loggedin' in session:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # return redirect(url_for('download_file', name=filename))
            # flash('Extension file not accepted')
        files_list = os.listdir(app.config['UPLOAD_FOLDER'])

        return render_template('cicd.html', files=files_list)

    return redirect(url_for('auth.login'))


# Convention verifyer page activator
@app.route('/convention', methods=['GET'])
def convention():
    if 'loggedin' in session:
        return render_template('convention.html')


# Convention verifyer page logic
@app.route("/verify/", methods=['POST'])
def verify():

    # All the secret variables stored inside .env file
    gitlab_url = os.environ.get('gitlab_url')
    token = os.environ.get('private_token')
    teams_url = os.environ.get('teams_url')

    # ------- Auto Correction ------- #
    auto_correction = 0  # Change this to 1 if you want autocorrection to be on
    # ------------------------------- #

    gl = gitlab.Gitlab(url=gitlab_url, private_token=token, ssl_verify=False)

    urllib3.disable_warnings()

    # Function that scans all members from a group
    def find_group_member(group):
        global user_list
        user_list = []
        groups = gl.groups.list(all=True)
        for grp in groups:
            if grp.name == group.name:
                try:
                    members = grp.members.list(all=True)
                    for member in members:
                        print("Member : " + str(member.name))
                        user_list.append(member.name)

                except:
                    # Authorisation error handler - lack of privileges
                    print(Fore.RED + "Not allowed" + Fore.RESET)

    # Function to verify and change groups name, accordingly with convention
    def camelcase(group):
        bad_name = 0
        left_word, right_word = "", ""
        name = group.name
        camel_name = inflection.camelize(name)
        for char in name:
            if char == " ":
                bad_name += 1
                listed_name = name.split()
                left_word = inflection.camelize(listed_name[0])
                right_word = inflection.camelize(listed_name[1])
            elif char == "_":
                bad_name += 1
                listed_name = name.split("_")
                left_word = inflection.camelize(listed_name[0])
                right_word = inflection.camelize(listed_name[1])
        if bad_name != 0:
            print(Fore.RED + "Group name convention not respected" + Fore.RESET)
            good_name = left_word + right_word
            print("Group name awaited : " + good_name)
            if auto_correction == 1:
                groups = gl.groups.list(all=True)
                for grp in groups:
                    if grp.name == name:
                        grp.name = good_name
                        grp.path = good_name
                        grp.save()
                print(Fore.BLUE + "Group name changed following convention" + Fore.RESET)
        else:
            if name == camel_name:
                print(Fore.GREEN + "Group name convention respected" + Fore.RESET)
            else:
                print(Fore.RED + "Group name convention not respected" + Fore.RESET)
                print("Group name awaited : " + camel_name)
                if auto_correction == 1:
                    groups = gl.groups.list(all=True)
                    for grp in groups:
                        if grp.name == name:
                            grp.name = camel_name
                            grp.path = camel_name
                            grp.save()
                    print(Fore.BLUE + "Group name changed following convention" + Fore.RESET)

    # Function to verify and change projects name, accordingly with convention
    def snakecase(project):
        first_char = project.name[:1]
        if first_char == "_":
            project.name = project.name[1:]

        # Optional ---------------------------------------------------------------------------------------------------------- #
        # project_snake_1 = inflection.parameterize(project.name)   # 1- We add dashes to all special characters as spaces
        # project_snake_2 = inflection.camelize(project_snake_1)    # 2- Then we add the uppercase to all first letters
        # project_snake_3 = inflection.underscore(project_snake_2)  # 3- Finally we add the underscore who are != uppercase
        # Optional ---------------------------------------------------------------------------------------------------------- #

        project_snake_3 = inflection.underscore(project.name)  # If it is snake_cased no need for upper lines
        print("# Name awaited : " + project_snake_3)
        if project.name != project_snake_3:
            print(Fore.RED + "Name convention not respected" + Fore.RESET)
            if auto_correction == 1:
                project.name = project_snake_3
                project.path = project.name
                project.save()
                print(Fore.BLUE + "Name and path changed following convention" + Fore.RESET)
        else:
            print(Fore.GREEN + "Name convention is respected" + Fore.RESET)

    # This is the main function, list all projects + groups + members + tree structure and count bad ones + teams report
    def list_projects():
        project_struct, project_count, project_bad_count = 0, 0, 0
        url = "https://"  # Use your documentation wiki url
        projects = gl.projects.list(all=True)

        for project in projects:
            project_bad = 0
            print("#------------------------------------#\n"
                  "# Project name : " + project.name + "\n"
                  "#------------------------------------#")

            snakecase(project)
            groups = project.groups.list(all=True)

            for group in groups:
                print("--> Group name : " + group.name)
                camelcase(group)
                if group == groups[0]:
                    find_group_member(group)
            branches = project.branches.list(all=True)

            for branch in branches:
                file, folder = 0, 0
                print("Branch name : " + branch.name)
                objects = project.repository_tree('.', ref=branch.name, all=True)

                for obj in objects:
                    obj_name = obj['name']
                    obj_type = obj['type']

                    if obj_type == "tree":
                        print("    --/ " + obj['name'] + " " + obj['type'])
                    else:
                        print("        --| " + obj['name'] + " " + obj['type'])

                    if obj_type == "blob" and obj_name == "README.md":
                        file += 1
                    elif obj_type == "blob" and obj_name == "CHANGELOG":
                        file += 1
                    elif obj_type == "blob" and obj_name == ".gitignore":
                        file += 1
                    elif obj_type == "tree" and obj_name == "src":
                        folder += 1
                    elif obj_type == "tree" and obj_name == "docs":
                        folder += 1
                    elif obj_type == "tree" and obj_name == "test-files":
                        folder += 1

                if file >= 3 and folder >= 3:
                    print(Fore.GREEN + "Branch structure is OK" + Fore.RESET)
                    project_struct += 1
                else:
                    print(Fore.RED + "Branch structure not accepted" + Fore.RESET)
                    project_bad += 1

            if project_bad > 0:
                print("#------------------------------------------#" + "\n"
                      "# --> Project: " + project.name + Fore.RED + " Structure is not validated" + Fore.RESET)
                project_bad_count += 1
                print("# --> Users to report: " + str(user_list) + "\n"
                      "#------------------------------------------#" + "\n\n")

                for user in user_list:
                    file = open("./reports/" + str(user) + ".txt", "a")
                    file.write(str(project.name) + "\n")
                    file.close()

                teams_msg = pymsteams.connectorcard(teams_url)

                teams_msg.title("- Bad Project Structure -")
                teams_msg.text("# - Project : " + project.name + " --> Structure is not validated" + "\n"
                               "# - Users to report : " + str(user_list) + "\n")
                teams_msg.addLinkButton("Open convention wiki", url)
                teams_msg.color('EA680F')
                teams_msg.send()

            else:
                print("#------------------------------------------#" + "\n"
                      "# --> Project: " + project.name + Fore.GREEN + " Structure is validated" + Fore.RESET + "\n"
                      "#------------------------------------------#" + "\n\n")

            project_count += 1

        print("-----------------------------------\n"
              "| Projects number : " + str(project_count) + "\n"
              "-----------------------------------")
        print("| Validated projects structure : " + str(project_count - project_bad_count) + "\n"
              "-----------------------------------")

    if __name__ == "__main__":
        list_projects()
    return render_template('convention_result.html')


# Verifyer for extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.debug = True
    app.run()
