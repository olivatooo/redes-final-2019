#!/bin/bash

echo -e "\e[92m ______     ______     ______   ______     ______     _____     ______     ______       "
echo -e "\e[92m/\  == \   /\  __ \   /\__  _\ /\  ___\   /\  __ \   /\  __-.  /\  __ \   /\  == \      "
echo -e "\e[92m\ \  __<   \ \ \/\ \  \/_/\ \/ \ \  __\   \ \  __ \  \ \ \/\ \ \ \ \/\ \  \ \  __<      "
echo -e "\e[92m \ \_\ \_\  \ \_____\    \ \_\  \ \_____\  \ \_\ \_\  \ \____-  \ \_____\  \ \_\ \_\    "
echo -e "\e[92m  \/_/ /_/   \/_____/     \/_/   \/_____/   \/_/\/_/   \/____/   \/_____/   \/_/ /_/    "
echo -e "\e[92m   __     __  __     __   __     __     __   __     __  __     ______"
echo -e '\e[92m  /\ \   /\ \/\ \   /\ "-.\ \   /\ \   /\ "-.\ \   /\ \_\ \   /\  __ \'
echo -e '\e[92m _\_\ \  \ \ \_\ \  \ \ \-.  \  \ \ \  \ \ \-.  \  \ \  __ \  \ \ \/\ \'
echo -e '\e[92m/\_____\  \ \_____\  \ \_\" \_\  \ \_\  \ \_\" \_\  \ \_\ \_\  \ \_____\'
echo -e '\e[92m\/_____/   \/_____/   \/_/ \/_/   \/_/   \/_/ \/_/   \/_/\/_/   \/_____/v2'

sleep 2
./roteador.py &
sleep 5
echo -e "\e[1;49;33mWorking on tests (haha)\n"
sudo slattach -vLp slip /dev/pts/1 &
sleep 1
echo -e "It worked for me... \n"
sudo slattach -vLp slip /dev/pts/2 &
sleep 1
echo -e "Merging 'WIP: Do Not Merge This Branch' Into Master \n"
sudo slattach -vLp slip /dev/pts/3 &
sleep 1
echo -e "did everything \n"
sudo ifconfig sl0 192.168.123.1 pointopoint 192.168.122.1 mtu 1500
sleep 1
echo -e "\e[1;49;33mOut for vacation... DONT YOU DARE TO CALL ME. \n"
sudo ip route add 192.168.124.0/24 via 192.168.122.1
sleep 1
echo -e "\e[1;49;33mNever before had a small typo like this one caused so much damage. \n"
sudo ip route add 192.168.125.0/24 via 192.168.122.1
sleep 1
echo -e "Continued development... \n"
sudo ip netns add ns1
sleep 1
echo -e "Things went wrong... \n"
sudo ip link set sl1 netns ns1
sleep 1
echo -e "Don't tell me you're too blind to see \n"
sudo ip netns exec ns1 ifconfig sl1 192.168.124.1 pointopoint 192.168.122.1 mtu 1500
sleep 1
echo -e "This line is a lie \n"
sudo ip netns exec ns1 ip route add 0.0.0.0/0 via 192.168.122.1
sleep 1
echo -e "magic, have no clue but it works \n"
sudo ip netns add ns2
sleep 1
echo -e "apparently i did something… \n"
sudo ip link set sl2 netns ns2
sleep 1
echo -e "This bug has driven lots of coders completely mad. You won't believe how it ended up being fixed \n"
sudo ip netns exec ns2 ifconfig sl2 192.168.125.1 pointopoint 192.168.122.1 mtu 1500
sleep 1
echo -e "omgsosorry \n"
sudo ip netns exec ns2 ip route add 0.0.0.0/0 via 192.168.122.1
sleep 1
echo -e "No changes after this point.\n"
exit 0
