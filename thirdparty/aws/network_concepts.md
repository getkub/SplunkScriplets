## How to do VPC, subnet, IGW, route table

- https://www.youtube.com/watch?v=aa3gGwJpCro


Concepts are
- Create VPC (10.0.0.0/16)
- Create multiple subnets 
  -  public  (10.0.1.0/24, 10.0.2.0/24 )
  -  private (10.0.3.0/24, 10.0.4.0/24 )
- Create internet gateway (IGW) and attach to VPC
- Create Route Table and attach to VPC. This will have only local routes by default
- For PUBLIC  Routes -> Edit Routes -> destination (0.0.0.0/0)  -> Target of Internet Gateway and attach to relevant IGW
- For PRIVATE Routes -> Subnet Association -> Associate two private networks to private route table
- For PUBLIC  Routes -> Subnet Association -> Associate two public  networks to private route table

- NAT Gateway required for egress
