"""Refresh the citation branch from the owner's network using existing gh login."""

import base64
import json
import subprocess
import tempfile
from pathlib import Path

from main import collect


REPOSITORY = "mynotwo/mynotwo.github.io"
BRANCH = "google-scholar-stats"


def api(endpoint, method="GET", body=None):
    command = ["gh", "api", f"repos/{REPOSITORY}/{endpoint}", "--method", method]
    if body is not None:
        command.extend(["--input", "-"])
    result = subprocess.run(command, input=json.dumps(body) if body is not None else None,
                            text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


def refresh():
    ref = api(f"git/ref/heads/{BRANCH}")["object"]["sha"]
    commit = api(f"git/commits/{ref}")
    previous = api(f"contents/gs_data.json?ref={ref}")
    with tempfile.TemporaryDirectory(prefix="scholar-refresh-") as folder:
        path = Path(folder)
        (path / "previous.json").write_bytes(base64.b64decode(previous["content"]))
        collect("Iw3bTCAAAAAJ", path / "previous.json", path)
        tree = api("git/trees", "POST", {
            "base_tree": commit["tree"]["sha"],
            "tree": [{"path": name, "mode": "100644", "type": "blob",
                      "content": (path / name).read_text(encoding="utf-8")}
                     for name in ("gs_data.json", "gs_data_shieldsio.json")],
        })
        updated = api("git/commits", "POST", {
            "message": "Refresh verified public Scholar citation data",
            "tree": tree["sha"], "parents": [ref],
        })
        # A concurrent writer makes this non-fast-forward update fail, preserving their data.
        api(f"git/refs/heads/{BRANCH}", "PATCH", {"sha": updated["sha"], "force": False})
        published = api(f"contents/gs_data.json?ref={updated['sha']}")
        if base64.b64decode(published["content"]) != (path / "gs_data.json").read_bytes():
            raise RuntimeError("Published data differs from the validated snapshot")
        print(f"Published and read back citation snapshot: {updated['sha']}")
        return updated["sha"]


if __name__ == "__main__":
    refresh()
