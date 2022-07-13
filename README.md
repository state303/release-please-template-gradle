# Example Template for Gradle Project

---

Preconfigured repository utilizing
[release-please-action](https://github.com/google-github-actions/release-please-action),
[codecov](https://about.codecov.io/).

## Reference

Majority of contents are combined from following sources.

- [Conventional Commits](https://www.conventionalcommits.org/en/)

- [Article](https://dwmkerr.com/conventional-commits-and-semantic-versioning-for-java/)
  by [Dave Kerr](https://github.com/dwmkerr)

- [Fabric Example Mod](https://github.com/axieum/fabric-example-mod)
  by [Jonathan Hiles](https://github.com/axieum)

## Features

- Automated version control, changelog and labeling with GitHub Actions
- Jacoco test coverage + codecov integration

## Prep

Clone the project to directory

```shell
git clone https://github.com/state303/release-please-template.git
```

Rename the folder name to match new repository name

```shell
mv release-please-template <your_repo_name>
```

Re-initialize git

```shell
cd <your_repo_name>
rm -rf .git
git init
```

And we need search and replace some properties.

| Path                          | Key               | Value               | Example        |
|-------------------------------|-------------------|---------------------|----------------|
| settings.gradle               | 	rootProject.name | 	your artifact name | netty          |
| gradle.properties             | 	maven_group      | 	your own group     | com.example    |
| gradle.properties             | 	github_repo      | 	GitHubID/RepoName  | state303/netty |
| gradle.properties             | 	artifact_version | 	initial version    | 0.0.0          |
| .github/workflows/release.yml | 	package-name     | 	package name       | netty          |


Remove irrelevant java package directory.
```shell
rm -rf src/main/java/io
```

For code coverage report, you must register to codecov.
Or, you may remove ***.github/workflows/coverage.yml***

(Optional) Apply git hook for [Conventional Commits](https://www.conventionalcommits.org/en/)

```shell
git config core.hooksPath .githooks
```

Now you are ready to push and work with your git repository with GitHub.
