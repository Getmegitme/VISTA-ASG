##3. Integration Runtime — connecting on-premises and cloud

##•	Explain in plain English why a Self-hosted IR is needed for an on-premises ERP database.

--A Self-hosted Integration Runtime (IR) is required because the ERP database is located inside the company's private network and protected by a firewall.

--Azure Data Factory runs in the Azure cloud and cannot directly access systems inside a corporate network.

--The Self-hosted IR acts as a secure bridge between Azure and the on-premises ERP system.

--The manufacturing company stores production records in an on-premises SQL Server ERP system.

--Every night:

--Self-hosted IR connects to ERP.
--Reads production data.
--Sends data securely to ADLS raw layer.
--ADF continues the pipeline from there.

--Without Self-hosted IR, Azure Data Factory would not be able to access the ERP database.

##•	Draw the network flow for a Self-hosted IR connecting an on-premises SQL Server to ADLS.

─────────────────────────────
 On-Premises Network                        
 SQL Server ERP Database                     
─────────────┬───────────────
             │
─────────────────────────────
 Self-hosted Integration     
 Runtime (IR)               
 Installed on Windows Server 
─────────────┬───────────────
             │ Outbound HTTPS
─────────────────────────────
 Azure Data Factory (ADF)    
─────────────┬───────────────
             │
─────────────────────────────
 ADLS Gen2                   
 raw/production/             
─────────────────────────────

--The data flow is as follows: 
--ERP Database -> Self hosted IR -> ADF Pipeline -> ADLS Raw Layer.

--The purpose is to transfer production data securely from the corporate network to Azure without exposing the ERP system to public internet.

##•	Explain what would happen if you tried to use Azure IR to connect to an on-premises database.

--The connection would fail. Azure Integration Runtime (Azure IR) is designed for cloud-to-cloud communication.

--Azure IR cannot directly access systems behind a corporate firewall. As a result, the connection test & copy activity will fail, data cannot be extracted and the pipeline execution will stop.

--Azure IR works only when both systems are accessible from Azure.

##•	Explain why the Self-hosted IR uses outbound connections only and why this matters for security.

--Self-hosted IR uses outbound HTTPS connections only because it is more secure.

--Instead of Azure opening connections into the company network, the IR initiates the connection to Azure.

--Security benefits:
--No Firewall Ports Need to be Opened
--Reduced Attack Surface
--Easier Compliance
--Data Remains Protected

--If inbound access were allowed then the ERP system would become vulnerable to unauthorized access, data theft, malware attacks and compliance violations. 
--Outbound-only communication prevents these risks. 
