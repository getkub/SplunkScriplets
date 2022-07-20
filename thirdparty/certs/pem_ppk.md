### PEM key conversions
- https://aws.amazon.com/premiumsupport/knowledge-center/ec2-ppk-pem-conversion/


```
brew install putty
# Convert ppk to pem
puttygen ppkkey.ppk -O private-openssh -o pemkey.pem

# .pem file to a .ppk file
puttygen pemKey.pem -o ppkKey.ppk -O private
```
