# import jenkins and sqlite
import jenkins
import sqlite3

# Hello this small script for Jenkins CI Servers API
# it will connect to specific instance and get all jobs and it's status
# and Saved it in sqlite Db
# this script devloped by : Sameh Ahmed

def main() :

    ServerUrl = input("What is Jenkins server url? ")
    username = input("What is Jenkins server Username? ")
    pswd = input('Password:')

    # connect to jenkins server  server
    server = jenkins.Jenkins(ServerUrl, username=username, password=pswd)
    user = server.get_whoami()
    version = server.get_version()
    print('Hello %s from Jenkins %s' % (user['fullName'], version))

    # create the database and jobs table
    db = sqlite3.connect("jenkensjobs.db")
    db.row_factory = sqlite3.Row
    db.execute("create table if not exists JenkinsJobs(Name text, status  text)")

    # get all jobs from jenkins server
    jobs = server.get_jobs()

    # iterate throw all jobs in the server and add it and it's statuss into database
    for job in jobs:
        jobinfo = server.get_job_info(job['name'])

        # check if this job buldable and contain status or not
        if ('color' in jobinfo):
            print(jobinfo);
            db.execute("insert into JenkinsJobs (Name,status) values (? , ?)", (jobinfo['fullName'], jobinfo['color']))

        else:
            print(jobinfo);
            db.execute("insert into JenkinsJobs (Name,status) values (? , ?)", (jobinfo['fullName'], "not buildable"))

        db.commit()
        print("Thanks All jobs and it's status saved in our SQLLite DB ... ")



if __name__ == '__main__':main()