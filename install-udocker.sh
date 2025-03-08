#!/bin/bash
clear
echo "Code By SNIPAVN"
echo "Installing Udocker/ Cài Đặt Udocker"
echo "Wait 3s to Install / Chờ 3s để cài"
sleep 3
sudo pip install udocker
echo "Đã Tải Xong Package Python-Udocker"
sleep 1
clear
echo -e "Nhập Tên User của Udocker"
read newuser
adduser --disabled-password --gecos '' $newuser
clear 
echo "Code By SNIPA VN"
echo "Đã tải xong Udocker"
echo "To run Udocker /Để Chạy Udocker : "sudo -u $newuser udocker (run/setup) (container image)'"
