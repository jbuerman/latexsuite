"""
Tests for git module.
"""

import os
import subprocess

from latex_suite.git import GitInteraction


class TestGitInteraction:

    def test_execute_bash_git_cmd(self, tmp_path):
        os.chdir(tmp_path)
        repo_name = "sample_repo"
        os.mkdir(repo_name)
        os.chdir(repo_name)
        print(os.curdir)
        p = subprocess.Popen("git init", stderr=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()
        p = subprocess.Popen("git status", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        msg, _ = p.communicate()
        p.wait()
        assert "On branch master" in str(msg), "Test setup error. Error initiating git repo."
        username = "test@test.org"
        u_name_params = GitInteraction.get_git_config_credential_set_username_parameter_string(username)
        GitInteraction.execute_bash_git_cmd(GitInteraction.CONFIG, u_name_params)
        found_credentials = False
        with open(".git/config", "r") as config_file:
            for line in config_file:
                if found_credentials:
                    assert f"username = {username}" in line, "Git credential setting was not successful."
                elif line.startswith("[credential"):
                    found_credentials = True
