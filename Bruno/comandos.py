#Comando para destruir todas as QoS e todas as Filas
sudo ovs-vsctl -- --all destroy QoS -- --all destroy Queue


#Comando para rodar o ryu
sudo ryu-manager ryu.app.ofctl_rest ryu.app.simple_swit_13_mod ryu.app.rest_conf_switch ryu.app.rest_qos ~/ryu/Bruno/MeuApp.py

sudo ryu-manager ryu.app.ofctl_rest ryu.app.simple_switch_13_mod ryu.app.rest_conf_switch ryu.app.rest_qos ~/ryu/Bruno/MeuApp.py

#Como ja foi importado os modulos dentro do MeuApp
sudo ryu-manager  ~/ryu/Bruno/MeuApp.py --observe-links

#Instalando o networkx
https://networkx.github.io/documentation/networkx-1.1/install.html
