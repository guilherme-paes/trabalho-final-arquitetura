Utilizando VirtualBox para comparar arquiteturas RISC-V e Von Neumann utilizando a Lei de Amdahl.

Este trabalho tem como objetivo comparar as arquiteturas de computadores Von Neumann e RISC-V e descrever os resultados coletados.

A arquitetura RISC-V deverá ser emulada através de um simulador web, enquanto a arquitetura de Von Neumann é precisamente a arquitetura-base de todas as distros do Linux (de maneira coneceitual, considerando que a arquitetura não é uma ISA).

Distro do linux utilizada: CentOS (https://www.centos.org/download/);
VirtualBox download: https://www.virtualbox.org/wiki/Downloads

O código utilizado para efetuar a comparação é baseado no código-fonte apresentado pelo professor em um trabalho passado e encontra-se presente neste repositório. Para instalá-lo no ambiente CentOS virtualizado, utilize o seguinte comando no terminal:

sudo yum install python3 python3-pip
pip3 install matplotlib psutil

