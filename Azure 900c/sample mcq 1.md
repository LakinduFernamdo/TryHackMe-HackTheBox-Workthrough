# AZ-900 Practice Question Bank
## Consolidated questions with correct answers


# Weak-Area Quiz 1 — 10 Questions

### 1. Hybrid cloud deployment

**Question:** A company operates its main application infrastructure in an on-premises private datacenter. It wants to extend its environment into Azure while keeping some workloads on-premises. Which cloud deployment model best describes this architecture?

- A. Public cloud
- B. Private cloud
- C. Hybrid cloud
- D. Community cloud

**Correct answer: C — Hybrid cloud**

**Explanation:** Hybrid cloud combines on-premises or private infrastructure with public cloud services such as Azure.

### 2. Dedicated private connectivity

**Question:** A company needs a dedicated private network connection between its on-premises datacenter and Azure. The company wants to avoid sending this connectivity over the public internet. Which Azure service should it choose?

- A. Azure VPN Gateway
- B. Azure ExpressRoute
- C. Azure Bastion
- D. Azure Front Door

**Correct answer: B — Azure ExpressRoute**

**Explanation:** ExpressRoute provides private connectivity between an on-premises network and Microsoft cloud services through a connectivity provider.

### 3. Private IP access to Azure Storage

**Question:** An organization hosts an Azure Storage account. A virtual machine in its VNet must access the storage service using a private IP address rather than its public endpoint. Which feature should be configured?

- A. Service Endpoint
- B. Private Endpoint
- C. Public DNS Zone
- D. Network Security Group

**Correct answer: B — Private Endpoint**

**Explanation:** A Private Endpoint assigns a private IP address in the VNet for private connectivity to the Azure service.

### 4. Private DNS for an Azure SQL Private Endpoint

**Question:** A company creates a Private Endpoint for an Azure SQL Database. Its virtual machines must resolve the database's normal service hostname to the Private Endpoint's private IP address. Which additional configuration is commonly required?

- A. Create and link an appropriate Private DNS zone
- B. Create an Azure Public DNS zone only
- C. Configure an Azure Load Balancer
- D. Create a Network Security Group

**Correct answer: A — Create and link an appropriate Private DNS zone**

**Explanation:** A Private DNS zone can contain the private DNS record and be linked to the VNet so its VMs resolve the service hostname privately.

### 5. Estimating Azure costs before deployment

**Question:** A company plans to deploy 10 virtual machines in Azure next month. Before deployment, the finance team wants to estimate the expected monthly cost using planned configurations and expected usage. Which tool is most appropriate?

- A. Azure Cost Management
- B. Azure Pricing Calculator
- C. Azure Advisor
- D. Azure Service Health

**Correct answer: B — Azure Pricing Calculator**

**Explanation:** The Pricing Calculator estimates expected costs before deployment using planned services, configurations, and usage.

### 6. Reviewing actual Azure spending

**Question:** An organization already runs several Azure workloads. Its finance team wants to examine historical spending, identify which services are increasing costs, and create budgets to track future spending. Which service is most suitable?

- A. Azure Pricing Calculator
- B. Azure Cost Management
- C. Azure Monitor
- D. Azure Policy

**Correct answer: B — Azure Cost Management**

**Explanation:** Cost Management provides cost analysis, spending insights, budgets, and cost-management capabilities.

### 7. Data governance and classification

**Question:** A company needs to discover sensitive information across its data estate, classify data, and establish data governance policies. Which Microsoft service is designed for this purpose?

- A. Microsoft Defender for Cloud
- B. Microsoft Purview
- C. Azure Bastion
- D. Azure Application Gateway

**Correct answer: B — Microsoft Purview**

**Explanation:** Microsoft Purview supports data discovery, classification, cataloging, and data governance.

### 8. Private Endpoint and DNS configuration — select THREE

**Question:** An organization has created a Private Endpoint for an Azure service. It wants VMs in a different subnet of the same VNet to resolve the service hostname to the Private Endpoint's private IP. Which THREE configurations or components support this design? Select all that apply.

- A. A Private Endpoint connected to the Azure service
- B. An appropriate Private DNS zone containing the private record
- C. A VNet link connecting the Private DNS zone to the VNet
- D. A public DNS zone replacing the Private DNS zone

**Correct answers: A, B, and C**

**Explanation:** The Private Endpoint provides private connectivity, the Private DNS zone stores the private DNS record, and the VNet link makes the zone available to resources in that VNet.

### 9. Cost Management budgets

**Question:** Azure Cost Management can be used to analyze actual Azure spending and create budgets to help control future costs.

- True
- False

**Correct answer: True**

**Explanation:** Cost Management supports cost analysis and budgets, helping organizations understand spending and monitor future costs.

### 10. Private Endpoint and public access

**Question:** Creating an Azure Private Endpoint automatically disables the public network access option for the connected Azure service.

- True
- False

**Correct answer: False**

**Explanation:** A Private Endpoint creates private connectivity, but creating it does not automatically guarantee that public network access is disabled. Public network access is controlled separately through the service's networking configuration.

---

# Weak-Area Quiz 2 — 10 Questions

### 11. Hybrid cloud with an on-premises database

**Question:** A company keeps its customer database in an on-premises datacenter because of internal requirements. During periods of high demand, it runs additional application servers in Azure. The application continues to use the on-premises database. Which cloud approach does this represent?

- A. Public cloud only
- B. Hybrid cloud
- C. Private cloud only
- D. Community cloud

**Correct answer: B — Hybrid cloud**

**Explanation:** The solution combines on-premises infrastructure with Azure resources, which is a hybrid cloud approach.

### 12. Encrypted site-to-site VPN over the internet

**Question:** A company has a small branch office and needs an encrypted site-to-site connection to its Azure virtual network. It is acceptable for the connection to travel over the public internet. Which service should it use?

- A. Azure ExpressRoute
- B. Azure VPN Gateway
- C. Azure Private Link
- D. Azure Traffic Manager

**Correct answer: B — Azure VPN Gateway**

**Explanation:** VPN Gateway supports site-to-site VPN connectivity using encrypted IPsec/IKE tunnels over the public internet.

### 13. Encryption over ExpressRoute

**Question:** An organization uses Azure ExpressRoute for private connectivity. Its security team requires encryption for traffic crossing the connection. Which statement is most accurate?

- A. ExpressRoute always encrypts all traffic automatically
- B. ExpressRoute provides private connectivity, but encryption must be addressed separately
- C. ExpressRoute requires all traffic to pass through a public VPN tunnel
- D. ExpressRoute encrypts traffic only when an NSG is attached

**Correct answer: B — ExpressRoute provides private connectivity, but encryption must be addressed separately**

**Explanation:** ExpressRoute provides private connectivity, but encryption is not automatically guaranteed for every connection. The organization must consider an appropriate encryption solution.

### 14. Hybrid DNS resolution

**Question:** A company uses its own DNS servers on-premises. Employees connect to Azure through a hybrid network and need to resolve Azure Private Endpoint hostnames correctly. Which Azure capability can help forward DNS queries from the on-premises environment to Azure-hosted DNS resolution?

- A. Azure DNS Private Resolver
- B. Azure Load Balancer
- C. Azure Firewall
- D. Azure Bastion

**Correct answer: A — Azure DNS Private Resolver**

**Explanation:** Azure DNS Private Resolver supports inbound and outbound DNS resolution between on-premises networks and Azure virtual networks without requiring DNS forwarder VMs.

### 15. Sharing a Private DNS zone across VNets

**Question:** An organization has two Azure virtual networks that must resolve records stored in the same Azure Private DNS zone. What should the administrator configure to make the zone available to both networks?

- A. A virtual network link for each VNet
- B. A separate public DNS zone for each VNet
- C. A separate ExpressRoute circuit for each VNet
- D. A load-balancing rule for each VNet

**Correct answer: A — A virtual network link for each VNet**

**Explanation:** Private DNS zones can be linked to multiple VNets so resources in each linked network can resolve the zone's records.

### 16. Comparing on-premises costs with Azure

**Question:** A company wants to compare the estimated cost of running its current on-premises infrastructure with the expected cost of moving equivalent workloads to Azure. Which tool is designed for this comparison?

- A. Azure Pricing Calculator
- B. Azure Total Cost of Ownership (TCO) Calculator
- C. Azure Cost Management
- D. Azure Advisor

**Correct answer: B — Azure Total Cost of Ownership (TCO) Calculator**

**Explanation:** The TCO Calculator helps estimate potential cost savings by comparing on-premises infrastructure costs with Azure.

### 17. Tracing data origins and movement

**Question:** A data governance team wants to understand where data originates, how it moves between systems, and which downstream reports or assets depend on it. Which Microsoft Purview capability is most relevant?

- A. Data lineage
- B. Conditional Access
- C. Threat detection
- D. Network traffic inspection

**Correct answer: A — Data lineage**

**Explanation:** Data lineage helps track data origins and transformations, including how data flows between assets.

### 18. Microsoft Purview capabilities — select THREE

**Question:** An organization is implementing Microsoft Purview for enterprise data governance. Which THREE activities are supported by Purview capabilities? Select all that apply.

- A. Discovering and cataloging data assets
- B. Classifying sensitive information
- C. Tracking data lineage across systems
- D. Establishing encrypted site-to-site VPN tunnels

**Correct answers: A, B, and C**

**Explanation:** Purview supports data discovery and cataloging, sensitive-data classification, and data lineage. VPN connectivity is provided by networking services such as Azure VPN Gateway.

### 19. VPN Gateway site-to-site connectivity

**Question:** Azure VPN Gateway can establish an encrypted site-to-site VPN connection between an on-premises network and an Azure virtual network over the public internet.

- True
- False

**Correct answer: True**

**Explanation:** VPN Gateway supports site-to-site VPN connectivity using encrypted IPsec/IKE tunnels over the public internet.

### 20. Private DNS zone availability

**Question:** An Azure Private DNS zone automatically becomes available to every virtual network in an Azure subscription without any virtual network links.

- True
- False

**Correct answer: False**

**Explanation:** A Private DNS zone does not automatically become available to every VNet; the relevant virtual networks must be linked, unless another DNS architecture provides the resolution.



