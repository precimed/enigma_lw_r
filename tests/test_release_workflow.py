from pathlib import Path


WORKFLOW_FILE = Path('.github/workflows/release.yml')


def test_release_workflow_exists_and_triggers_on_version_tags():
    assert WORKFLOW_FILE.exists()
    content = WORKFLOW_FILE.read_text()
    assert 'on:' in content
    assert 'tags:' in content
    assert '- "v*.*.*"' in content


def test_release_workflow_checks_tag_commit_is_on_main():
    content = WORKFLOW_FILE.read_text()
    command = (
        'git merge-base --is-ancestor "$GITHUB_SHA" '
        '"origin/main"'
    )
    assert 'Ensure tag commit is on main' in content
    assert command in content


def test_release_workflow_checks_version_and_generates_notes():
    content = WORKFLOW_FILE.read_text()
    assert 'export TAG_VERSION="${GITHUB_REF_NAME#v}"' in content
    assert 'version/version.py' in content
    assert 'VERSION' in content
    assert 'softprops/action-gh-release@v2' in content
    assert 'generate_release_notes: true' in content
