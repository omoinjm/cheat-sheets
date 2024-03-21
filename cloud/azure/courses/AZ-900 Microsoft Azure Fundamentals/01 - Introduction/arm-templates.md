# Azure Resource Templates

Automate and replicate tasks, actions and processes.

ARM templates provide a structured and efficient way to describe resource usage within Azure environments. Whether you're updating, deleting, or creating resources, ARM templates offer a consistent approach.

## Key Features

- **Resource Description**: Clearly articulate what resources are being manipulated within your Azure infrastructure.
- **Common Syntax**: ARM templates utilize a defined language, streamlining the process and making it easier to formalize and learn.
- **Idempotent**: Ensures that applying an ARM template multiple times yields the same result, promoting consistency and reliability.

By leveraging ARM templates, you can efficiently manage your Azure resources while maintaining consistency and reliability across deployments.


## Example

```json
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#", "contentVersion": "1.0.0.0",
    "resources":[
    {
        "type": "Microsoft.Storage/storageAccounts",
        "apiVersion": "2019-04-01",
        "name": "{provide-unique-name}",
        "location": "eastus",
        "sku": {
            "name": "Standard_LRS"
        },
        "kind": "StorageV2",
        "properties":{
            "supportsHttps TrafficOnly": true
        }
    }
}
```

- `$schema`: properties that are available in the template.

- `contentVersion`: version of the template. used to indicate changes and how major they are.

- `resources`: specify the resources you want and how to manipulate them.

## Benefits

- **Idempotent**: Run the same templates once, twice, or as many times as you like. It will have the same outcome.
- **Source Control**: Keep track of all changes to the ARM templates.
- **Reuse**: Use a combination of multiple partial ARM templates to achieve glory or at least complex templates.
- **Declarative**: Specify what you want, not how it is done.
- **No Human Errors**: Automation means humans don't repeat the same mistakes.
