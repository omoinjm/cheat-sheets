# The Language of Cloud Computing

## <mark>EXAM TIPS</mark>

Cloud computing has terms that are specific and critical to understanding it.

- High availability means systems are always available - even automatically!
- Reliability describes how Azure can tolerate failures or even disasters.
- Scalability refers to scaling out or scaling up while automatically providing resources as needed.
- Predictability is knowing your application will always perform as expected and knowing what it will cost.
- Security is having full control of your cloud security posture.
- Governance is standardizing cloud deployments to meet requirements/company standards
- Manageability is management of cloud resources and how we interact with them.

##  Resilience

The ability of a system to recover from failures and continue to function

### ✅ High Availability

| Traditional                    | Cloud                                        |
| ------------------------------ | -------------------------------------------- |
| You own the hardware.          | You don't own the hardware.                  |
| You have physical access.      | Add more servers with a click.               |
| You can't 'just add servers.'  | If the hardware fails, replace it instantly. |
|                                | Use clusters to ensure high availability.    |

### ✅ Reliability

(a.k.a. Fault Tolerance/Disaster Recovery)

**Deploy in Multiple Locations**:

- Global-scale computing

- Protects against regional failure/disaster

**No Single Point of Failure**:

- Resources in multiple locations

- If one computer goes down, others pick up the load

### ✅ Scalability

Automatically adjust resources (**horizontally** or **vertically**) to meet demand.

**Example**: Increase the number of VMs to handle peak traffic.

Don’t overpay for services

Automatically reduce resources when demand drops.

**Horizontal vs. Vertical Scaling**

Horizontal Scaling is a typical cloud model

| Horizontal                           | Vertical                                          |
| ------------------------------------ | ------------------------------------------------- |
| Adding additional VMs/containers.    | Increasing power (e.g., CPU/RAM) of existing VMs. |
| Scaling out.                         | Scaling up.                                       |

### ✅ Predictability

Predictable Performance and Costs

**Performance**

- Consistent experience for users regardless of traffic.

- Autoscaling, load balancing, and high availability provide a consistent experience.

**Costs**

- No unexpected surprises.

- Track and forecast resource usage in real time.

## Management

### ✅ Security

Full control of the security of your cloud environment. Patches, maintenance,
network control, and more!

### ✅ Governance

- Standardized environments

- Regulatory requirements

- Audit for compliance

### ✅ Manageability

Management of the cloud:

- Autoscaling

- Monitoring

- Template-based deployments 

Management in the cloud:

- Portal

- CLI

- APIs
