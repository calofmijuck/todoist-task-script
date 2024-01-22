# todoist-task-script

This is a python script for adding multiple (sub)tasks to Todoist.

Mainly supports YAML files, but CSV also works.

## YAML

YAML schema mainly follows the deverloper docs, but contains additional hierarchy of subtasks.

Refer to `samples/sample.yaml` for further details.

## CSV

CSV schema is from the Todoist official schema, as described [here](https://todoist.com/help/articles/format-a-csv-file-to-import-into-todoist).

When using CSV files, `project_id` must be given separately.

## Usage

```bash
poetry install

# yaml
python -m task_script --tasks "samples/sample.yaml"

# csv
python -m task_script --tasks "samples/sample.csv" --csv --project "project-id"
```
