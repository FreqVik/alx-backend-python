#!/usr/bin/env python3

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value and calls get_json once"""
        expected = {"login": org_name, "repos_url": f"https://api.github.com/orgs/{org_name}/repos"}
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        result = client.org
        self.assertEqual(result, expected)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test that the public_repos_url property returns the correct URL"""
        org_name = "google"
        client = GithubOrgClient(org_name)
        expected_url = f"https://api.github.com/orgs/{org_name}/repos"
        self.assertEqual(client._public_repos_url, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the correct list of repository names"""
        org_name = "google"
        repos_data = [
            {"name": "repo1", "license": {"key": "MIT"}},
            {"name": "repo2", "license": {"key": "Apache-2.0"}},
            {"name": "repo3", "license": None},
        ]
        org_data = {"repos_url": f"https://api.github.com/orgs/{org_name}/repos"}

        # Return org_data on first call, repos_data on second
        mock_get_json.side_effect = [org_data, repos_data]

        client = GithubOrgClient(org_name)
        result = client.public_repos(license="MIT")
        expected_repos = ["repo1"]
        self.assertEqual(result, expected_repos)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method with different license keys"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)



if __name__ == "__main__":
    unittest.main()
