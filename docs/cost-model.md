# Cost controls — local milestone

No AWS resources, paid data subscription or hosted generation calls were created/executed for milestone 1. The embedding model is downloaded publicly and runs locally; local CPU/memory/storage still have operating costs. Hosted-model cost in the recorded development evaluation is zero because its request/token count is zero, not because arbitrary live generation is assumed free.

No cloud quote has been calculated and no region has been selected. Before provisioning, price the independent showcase and demo stacks in the selected region, including RDS storage/backups/snapshots, Fargate runtime, networking/public IPv4 or VPC endpoints, S3/CloudFront requests/transfer, Lambda/API Gateway, queues/status, Secrets Manager and retained logs/images/state. A NAT-free design is not zero-network-cost. Budget alerts are notifications, not spending caps. Add durable per-run/demo application budgets before live public use.
