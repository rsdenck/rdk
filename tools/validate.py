import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-(?:alpha|beta|rc)\.(0|[1-9]\d*))?$")
EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F]")
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py"}


def load_json(path, errors):
    try:
        return json.loads(path.read_text())
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return None


def load_yaml(path, errors):
    try:
        return yaml.safe_load(path.read_text())
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid YAML: {exc}")
        return None


def validate_against(name, data, schema, errors):
    validator = Draft202012Validator(schema)
    for issue in validator.iter_errors(data):
        location = ".".join(str(part) for part in issue.absolute_path)
        errors.append(f"{name}{('.' + location) if location else ''}: {issue.message}")


def main():
    errors = []
    version = (ROOT / "VERSION").read_text().strip()
    if not SEMVER.fullmatch(version):
        errors.append(f"VERSION: invalid semantic version {version!r}")

    major = version.split(".", 1)[0]
    readme = (ROOT / "README.md").read_text()
    if f"Versao atual: {version}" not in readme:
        errors.append("README.md: current version is not declared")

    changelog = (ROOT / "CHANGELOG.md").read_text()
    releases = re.findall(r"^## \[([^\]]+)\]", changelog, flags=re.MULTILINE)
    if not releases or releases[0] != version:
        errors.append("CHANGELOG.md: latest release does not match VERSION")

    compatibility = (ROOT / "docs/COMPATIBILITY.md").read_text()
    if version not in compatibility:
        errors.append("docs/COMPATIBILITY.md: current version is missing")

    schemas = {}
    for path in sorted((ROOT / "schema").glob("*.json")):
        if path.name == "index.json":
            continue
        schema = load_json(path, errors)
        if schema is None:
            continue
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON Schema: {exc}")
        schema_id = schema.get("$id", "")
        if f"/v{major}/" not in schema_id:
            errors.append(f"{path.relative_to(ROOT)}: $id is not on major v{major}")
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{path.relative_to(ROOT)}: $schema must be Draft 2020-12")
        schemas[path.name] = schema

    envelope = schemas.get("rdk-envelope.schema.json")
    if envelope is None:
        errors.append("schema/rdk-envelope.schema.json: missing")

    schema_index = load_json(ROOT / "schema/index.json", errors)
    if schema_index is not None:
        if schema_index.get("version") != version:
            errors.append("schema/index.json: version does not match VERSION")
        if str(schema_index.get("major")) != major:
            errors.append("schema/index.json: major does not match VERSION")
        indexed = {row.get("file") for row in schema_index.get("schemas", [])}
        if indexed != set(schemas):
            errors.append(f"schema/index.json: indexed files mismatch: {sorted(indexed ^ set(schemas))}")
        for row in schema_index.get("schemas", []):
            schema = schemas.get(row.get("file"))
            if schema is not None and row.get("id") != schema.get("$id"):
                errors.append(f"schema/index.json: id mismatch for {row.get('file')}")
            if row.get("status") not in {"active", "deprecated", "removed"}:
                errors.append(f"schema/index.json: invalid status for {row.get('file')}")

    version_history = load_yaml(ROOT / "registry/version-history.yaml", errors)
    if version_history is not None:
        versions = version_history.get("versions", [])
        if not versions or versions[0].get("version") != version:
            errors.append("registry/version-history.yaml: latest version does not match VERSION")
        for row in versions:
            if row.get("status") not in {"active", "deprecated", "removed"}:
                errors.append(f"registry/version-history.yaml: invalid status for {row.get('version')}")
            if not isinstance(row.get("breaking"), bool):
                errors.append(f"registry/version-history.yaml: breaking must be boolean for {row.get('version')}")

    examples = {}
    message_ids = set()
    for path in sorted((ROOT / "examples").glob("*.json")):
        data = load_json(path, errors)
        if data is None:
            continue
        examples[path.name] = data
        message_id = data.get("message_id")
        if message_id in message_ids:
            errors.append(f"{path.relative_to(ROOT)}: duplicated message_id")
        if isinstance(message_id, str):
            message_ids.add(message_id)

    for name, data in examples.items():
        if data.get("spec_version") != version:
            errors.append(f"examples/{name}: spec_version does not match VERSION")
        message_type = data.get("type")
        schema = schemas.get(f"{message_type}.schema.json")
        if schema is None:
            errors.append(f"examples/{name}: no schema for type {message_type!r}")
            continue
        validate_against(f"examples/{name}", data, schema, errors)
        if envelope is not None:
            validate_against(f"examples/{name} envelope", data, envelope, errors)
        correlation_id = data.get("correlation_id")
        if correlation_id is not None and correlation_id not in message_ids:
            errors.append(f"examples/{name}: correlation_id has no example source")

    invalid_examples = []
    for path in sorted((ROOT / "examples/invalid").glob("*.json")):
        data = load_json(path, errors)
        if data is None:
            continue
        invalid_examples.append(path.name)
        schema = schemas.get(f"{data.get('type')}.schema.json")
        rejected = data.get("spec_version") != version
        if schema is not None:
            rejected = rejected or bool(list(Draft202012Validator(schema).iter_errors(data)))
        if envelope is not None:
            rejected = rejected or bool(list(Draft202012Validator(envelope).iter_errors(data)))
        if not rejected:
            errors.append(f"examples/invalid/{path.name}: fixture was accepted as valid")

    operations_doc = load_yaml(ROOT / "registry/operations.yaml", errors)
    errors_doc = load_yaml(ROOT / "registry/error-codes.yaml", errors)
    operation_keys = set()
    operation_ids = set()
    if operations_doc is None:
        operations = []
    else:
        if operations_doc.get("version") != version:
            errors.append("registry/operations.yaml: version does not match VERSION")
        operations = operations_doc.get("operations", [])
        for operation in operations:
            key = (operation.get("id"), operation.get("version"))
            if key in operation_keys:
                errors.append(f"registry/operations.yaml: duplicated operation {key}")
            operation_keys.add(key)
            operation_ids.add(operation.get("id"))
            if not SEMVER.fullmatch(str(operation.get("version", ""))):
                errors.append(f"registry/operations.yaml: invalid version for {operation.get('id')}")
            if operation.get("status") not in {"active", "deprecated", "removed"}:
                errors.append(f"registry/operations.yaml: invalid status for {operation.get('id')}")

    error_codes = set()
    if errors_doc is None:
        error_rows = []
    else:
        if errors_doc.get("version") != version:
            errors.append("registry/error-codes.yaml: version does not match VERSION")
        error_rows = errors_doc.get("codes", [])
        for row in error_rows:
            code = row.get("code")
            if code in error_codes:
                errors.append(f"registry/error-codes.yaml: duplicated code {code}")
            error_codes.add(code)
            if not isinstance(row.get("retryable"), bool):
                errors.append(f"registry/error-codes.yaml: retryable must be boolean for {code}")
            if row.get("status") not in {"active", "deprecated", "removed"}:
                errors.append(f"registry/error-codes.yaml: invalid status for {code}")

    command = examples.get("command.json")
    if command is not None:
        key = (command.get("payload", {}).get("operation"), command.get("payload", {}).get("operation_version"))
        if key not in operation_keys:
            errors.append(f"examples/command.json: operation {key} is not registered")
        if command.get("authorization", {}).get("scope") != key[0]:
            errors.append("examples/command.json: authorization scope does not match operation")

    hello = examples.get("hello.json")
    if hello is not None:
        for capability in hello.get("payload", {}).get("capabilities", []):
            if capability not in operation_ids:
                errors.append(f"examples/hello.json: capability {capability} is not registered")

    error_example = examples.get("error.json")
    if error_example is not None:
        code = error_example.get("payload", {}).get("code")
        if code not in error_codes:
            errors.append(f"examples/error.json: code {code} is not registered")

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        if path.suffix not in TEXT_SUFFIXES and path.name not in {"VERSION", "Makefile", "CODEOWNERS"}:
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            errors.append(f"{path.relative_to(ROOT)}: non UTF-8 text")
            continue
        if "\u2014" in text:
            errors.append(f"{path.relative_to(ROOT)}: U+2014 is forbidden")
        if EMOJI.search(text):
            errors.append(f"{path.relative_to(ROOT)}: emoji is forbidden")

    if errors:
        print("rdk validate: failed", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print(
        f"rdk validate: ok version={version} schemas={len(schemas)} examples={len(examples)} "
        f"invalid={len(invalid_examples)} operations={len(operation_keys)} codes={len(error_codes)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
