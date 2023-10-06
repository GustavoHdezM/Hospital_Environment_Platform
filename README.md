# Architectural interventions to mitigate the spread of SARS-CoV-2 in emergency departments



## Description

In this project, we explore how architectural interventions could mitigate the spread of emerging respiratory pathogens using the example of SARS-CoV-2 during the first pandemic wave in 2020 in a prototypical emergency department (ED) setting. For more information, please refer to the paper draft.

## Dependencies

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- The ED modeling platform was developed in Python 3.11
- Tool for launching parallel tasks (scenarios) - [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html#)
- Epidemiology Endpoints tests run in R


- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://zivgitlab.uni-muenster.de/mejia/architectural_interventions_emergency_dep.git
git branch -M main
git push -uf origin main
```

## Running Scenarios
### Platform files (.py)
```main_architect_interv_ED```. This file contains the complete modeling platform for running each scenario, base case, and each architectural intervention. Comment/uncomment the code section for the scenario to be tested.

```funct_architect_interv_ED```. Contains complementary functions, callable from the main file.

```parall_architect_interv_ED```. File for launching parallel scenarios, runs X number of parallel simulations, case example with 1000 simulations. Ensure changing the saving path for each new testing scenario.

```figs_architect_interv_ED```. Produce boxplots for each scenario and ED area plotting the number of new infections (patients and healthcare workers) per scenario.

## In code section for testing scenarios 

    ```
                         OFFICIAL INTERVENTIONS
    
    NOTE: Comment/uncomment the code section for the scenario to test
          
    1. Flexible Partitions (FP) 
    (in the code, the intervention can be found as "curtains")
    2. Attention Area Separation (AS).
    3. Holding Area Separation (HS).
    (in the code, the intervention can be found as "waiting area separation")
    4. ED Base Separation (EBS).
    (in the code, ED Base can be found as "Nurse base")
    5. ED Base Extension (EBE).
    6. Ventilation (Vent).
    7. HS + AS
    8. FP + Vent
    9. AS + Vent
    10. EBE + Vent
    11. AS + EBE +Vent


    ```



- [ ] [Set up project integrations](https://zivgitlab.uni-muenster.de/mejia/architectural_interventions_emergency_dep/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing(SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thank you to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README
Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
