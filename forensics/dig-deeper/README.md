# Dig Deeper

by IGNITE

---

## Flag

COMPFEST14{152.118.70.20_39061}  

COMPFEST14{152.118.70.20_33685}  

COMPFEST14{152.118.70.20_17189}  

COMPFEST14{152.118.70.20_4645} 

COMPFEST14{152.118.70.20_21365}


## Description
Lately, my dear friend Thomas is interested in DNS. He is trying to make a custom DNS server using his computer. He reads lot of articles about what is DNS to help him understand. After hours of work, he finally succeeds to make his own custom DNS server, The server that he made only have 1 domain stored in its database, but there is still some issue about the server. If we try to find out the IP address from the domain that is stored in the database of the custom server, there will be an error. Thomas asks me for help to retrieve information about the stored domain, but I guess you guys are more capable to do it. Here's the traffic that’s captured when Thomas is trying to learn about DNS, maybe it can help you solve it. Oh yeah, 1 more thing, Thomas mentioned something about port 3534, hope it helps

## Difficulty
Tingkat kesulitan soal:medium

## Hints
* have you try to make a forwarding server?

## Tags
dns, wireshark

## Deployment
1. jalankan file challenge_server.py
2. program akan melakukan bind ke port 3534 (UDP)


## Notes
format flag: COMPFEST14{IPAddress_ID}
