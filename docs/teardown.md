# Teardown

Milestone 1 is local only. Stop the preview and API processes, then `make native-down` or `make db-stop`. This preserves data for reproducibility; it does not delete the project or database volume. Original documents, hashes and exports should be retained before any future cleanup.

No cloud teardown is currently necessary because nothing was provisioned. Before a future AWS exercise, document separate showcase/demo destroy procedures and ownership, backups and retention policies. After destroying compute/database resources, verify remaining snapshots, backups, ECR images, S3 object versions, CloudWatch logs, secrets and Terraform state/bootstrap resources. These can remain billable. Do not describe stopping an RDS instance as permanent cost elimination.
