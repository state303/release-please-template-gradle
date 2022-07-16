# Example Template for Gradle Project

---

Preconfigured gradle repository utilizing
[release-please-action](https://github.com/google-github-actions/release-please-action),
[codecov](https://about.codecov.io/).

## Reference

Majority of contents are combined from following sources.

- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/en/)
- [Article](https://dwmkerr.com/conventional-commits-and-semantic-versioning-for-java/)
  by [Dave Kerr](https://github.com/dwmkerr)
- [Fabric Example Mod](https://github.com/axieum/fabric-example-mod)
  by [Jonathan Hiles](https://github.com/axieum)

## Features

- Automated version control, changelog and labeling with GitHub Actions
- Jacoco test coverage + codecov integration

## Prep

Download generate.py
```shell
curl -LO https://raw.githubusercontent.com/state303/release-please-template/main/generate.py
```

Install dependency 'PyYAML' if you don't have.

```shell
# check if you have it
pip list | grep -i "pyyaml"
# if nothing shows up, you need to install the pyyaml
pip install pyyaml
```

Write your configuration on the (recommended)

```yaml
# prefer config.yaml on the same path as generate.py
#
# any missing value or if config itself is missing
# these the default values will be applied for each, or all of them

# default: <YOUR_USERNAME_VALUE>
# key: ["username", "user"]
username: YOUR_GITHUB_USERNAME
# default: <YOUR_REPONAME_VALUE>
# key: ["reponame", "repo", "repository"]
reponame: YOUR_GITHUB_REPOSITORY_NAME
# default: <YOUR_ARTIFACT_VALUE>
# key: ["artifact", "maven-artifact"]
maven-artifact: YOUR_MAVEN_ARTIFACT_NAME
# default: <YOUR_GROUP_VALUE>
# key: ["group", "mavengroup", "maven-group"]
maven-group: YOUR_MAVEN_GROUP_NAME
# default: <YOUR_PACKAGE_NAME_VALUE>
# key: ["pkg", "package", "packagename", "package-name"]
package-name: PREFIX_FOR_YOUR_REPOSITORY_RELEASE_PACKAGE_NAME
# default: false
# key: publish only
# value: true, false TruE, faLSE, 0, 1
publish: true
# default: false
# key: codecov only
# value: true, false TruE, faLSE, 0, 1
codecov: true
```

Now, as you have config.yaml on the same path as generate.py, you may run

```shell 
python generate.py
```

The script **_will work_** even if you do not have the config. <br>
However, the values will be set to default for each path.

If you have config file named differently, or under different path, you may run

```shell
python generate.py -f {YOUR_CONFIG_PATH}
# OR
python generate.py --file {YOUR_CONFIG_PATH}
```

Git will be initialized if you ran generate.py. Just set upstream and branch, etc.

Now settings are all done, and will automatically do most of the CI for you.

## Optional

If you want, apply git hook for [Conventional Commits](https://www.conventionalcommits.org/en/)

```shell
git config core.hooksPath .githooks
```

If you already integrated your GitHub account with codecov; uncomment from build workflow<br>
Or, if you already set **_codecov_** to **_true_** in config.yaml, then you can skip this section.

```yaml
      - name: 🎯️ Upload codecov
        uses: codecov/codecov-action@v3
        with:
          files: "**/build/reports/jacoco/test/jacocoTestReport.xml"
```

If you wish to publish your maven package to somewhere like GitHub, Nexus, or Artifactory;<br>
Uncomment from release workflow.<br>
Or, if you already set _**publish**_ to **_true_** in config.yaml, then you can skip this section.

```yaml
      - name: 🚀 Publish new package
        run: ./gradlew publish
        env: 
          # set these secrets from your repository.action.secrets section
          # or adjust these to fit your needs 
          GITHUB_ACTOR: ${{ secrets.REPO_USER }}
          GITHUB_TOKEN: ${{ secrets.REPO_PASS }}
```
