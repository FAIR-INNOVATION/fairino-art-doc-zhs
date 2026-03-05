ROS2接口使用说明
================================================

.. toctree:: 
    :maxdepth: 5

概述
-----------------------------------------------
控制器采用的系统是Ubuntu22.04LTS，对应的ROS2版本是Humble。机械臂ROS2相关接口是基于ros2 control框架构建的，因此使用ROS2控制的时候，需要特别留意版本对齐，以免出现DDS通讯版本不兼容的情况。

ros2 conrol插件的启动
--------------------------------------------------------------------
首先，需要使用SSH登录控制器，控制器上的LAN1口设定ip为”192.168.58.1”，LAN2口设定ip为”192.168.137.77”。需要将上位机设定到对应网段的不同ip，才可以使用SSH登录。

我们假设使用Tera term软件登录SSH，打开软件，得到如下界面，再主机框中输入对应口的ip，我们假设使用LAN1口，因此ip应该填写192.168.58.1。
   
.. limage:: 038.png
   :align: center
   :width: 6in

.. centered:: 图表 5-1 Tera term初始界面

点击确定后，会弹出提示框，输入用户名fairino，密码1，然后点击确定。
   
.. limage:: 039.png
   :align: center
   :width: 6in

.. centered:: 图表 5-2 登录界面
 
进入bash界面之后，如果是单臂用户，使用cd指令进入single_ART3_R7_project文件夹，若是双臂用户，进入dual_ART3_R7_project。
   
.. limage:: 040.png
   :align: center
   :width: 6in

.. centered:: 图表 5-3 进入单臂工程文件夹
  
输入./runqhal.sh指令，启动底层HAL库程序，建立机械臂通讯，此时会提示输入密码，输入1然后回车即可。
   
.. limage:: 041.png
   :align: center
   :width: 6in

.. centered:: 图表 5-4 启动HAL库程序
 
等待10s之后，再输入./runplguin指令，即可启动ros2 control插件程序，等待约10s，手臂可以进入使能状态。
   
.. limage:: 042.png
   :align: center
   :width: 6in

.. centered:: 图表 5-5 启动ros2 control插件程序

ros2 control接口说明
--------------------------------------------------------------------
单臂下的配置参考下图所示，插件会启动一个名为single_arm_controller的控制器，类型是joint_trajectory_controller/JointTrajectoryController。另外，插件还会启动joint_state_broadcaster这个控制器，类型是joint_state_broadcaster/JointStateBroadcaster。
   
.. limage:: 043.png
   :align: center
   :width: 4in

.. centered:: 图表 5-6 单臂配置参考

双臂下的配置参考下图所示，插件会启动一个名为dual_arm_controller的控制器，类型是joint_trajectory_controller/JointTrajectoryController。Joint_state_bradcaster这个控制器也会启动启动。
   
.. limage:: 044.png
   :align: center
   :width: 4in

.. centered:: 图表 5-7 双臂配置参考

远程桌面的使用
--------------------------------------------------------------------
控制器中集成了xrdp远程桌面，方便习惯使用图形化界面的用户拷贝文件，编写代码等操作，注意：远程桌面的用户权限无法让ros2 control插件获取实时优先级，因此启动HAL程序和ros2 control插件务必注意不能在远程桌面中进行。
假设使用windows系统登录远程桌面，打开windows的远程桌面服务，在文本框中输入ip地址，假设连接的是LAN1口，那么ip地址应该是192.168.58.1。
   
.. limage:: 045.png
   :align: center
   :width: 6in

.. centered:: 图表 5-8 远程桌面连接
  
点击连接后，跳出xrdp登录界面，username输入fairino，password是1，然后点击ok。
   
.. limage:: 046.png
   :align: center
   :width: 4in

.. centered:: 图表 5-9 xrdp登录界面
  
进入ubuntu桌面后可能会多次弹出授权窗口，要求输入密码，此时填入1按回车即可，最后可以正常显示桌面。
   
.. limage:: 047.png
   :align: center
   :width: 6in

.. centered:: 图表 5-10 Ubuntu桌面

ART3_R7 SDK使用说明
--------------------------------------------------------------------
由于SDK有专门的《ART3_R7 SDK手册》，因此该部分内容不在本手册中赘述