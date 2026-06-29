调试工具
=======================================================================

.. toctree:: 
    :maxdepth: 5

根据第二章节的阐述，ARTPlugin插件系统提供了看板和指令两条人机交互通道，但是ROS2的接口需要程序对接上才能正常交互，这部分ROS2系统并没有提供便捷的人机交互界面。更进一步的，用户学习使用插件，或者调试过程中往往需要产品能够首先简单运动，然后再往后继续深入。基于此，法奥提供了便捷的可视化交互工具，方便用户入门ARTPlugin系统。

调试工具启动
---------------------------------------------------
上面提到对于用户交互最重要的3个方面为：状态看板人机交互，Action指令人机交互和伺服调试人机交互。这3个方面依次给出了人机交互界面调试工具，第一个为rqt自带的topic monitor，第二个和第三个为专门为插件开发的配套调试软件fairino_debug_tool。

首先进入/opt/fairino_art_plugin目录下，运行改目录下runrqttool.sh脚本，可以看到界面会依次弹出3个软件页面。

Topic Monitor界面：
   
.. limage:: 002.png
   :align: center
   :width: 6in

.. centered:: 图表 3-1 状态看板

在Topic列表里面勾选hardware_state话题，就可以看到插件发布的全状态。

Action调试界面：
   
.. limage:: 003.png
   :align: center
   :width: 6in

.. centered:: 图表 3-2 Action指令调试工具

在该界面中，点击refresh，会自动刷新action服务列表，选择fairino_hardware_command_controller/command这个action服务，然后在Comman String后面的文本框中可以输入指令字符，点击call发送，下面的文本框会反馈指令执行结果：
   
.. limage:: 004.png
   :align: center
   :width: 6in

.. centered:: 图表 3-3 Action指令调试工具收发指令

多关节调试工具：

该工具是可以加载joint_trajectory_controller，然后对controller关联的关节进行位置调试。首先，需要激活至少一个joint_trjectory_controller，可以通过上一个action指令调试工具实现。
   
.. limage:: 005.png
   :align: center
   :width: 6in

.. centered:: 图表 3-4 激活left_arm_controller

然后在多关节调试工具页面上点击刷新列表按钮，就可以看到刚激活的controller。
   
.. limage:: 006.png
   :align: center
   :width: 6in

.. centered:: 图表 3-5 获取到controller的页面

点击同步并获取关节配置，可以获取到该controller对应的关节名称和数量信息，用户可以设置每一个关节的限位和最大速度。
   
.. limage:: 007.png
   :align: center
   :width: 6in

.. centered:: 图表 3-6 配置界面

设置完毕后，点击进入调试界面，就可以进入主界面，该界面会同步当前伺服关节的实际位置，用户可以通过点击同步位置手动刷新当前实际位置到界面中。
   
.. limage:: 008.png
   :align: center
   :width: 6in

.. centered:: 图表 3-7 运动调试界面

该页面支持的功能：

- 用户通过手动调节关节滑块，设定期望的关节移动目标位置，点击执行当前位置，各关节可以通过样条规划曲线运动值目标位置，用户可以通过速度比例和加速度值(单位rad/s2)调节运动快慢
- 点击记录点位，可以把当前位置记录成一个示教点，记录多个点之后，点击开始循环，可以在各个示教点之间顺序循环移动，通过点间停顿，可以调节点和点之间的运动暂停间隔时间。用户可以通过删除点位删除选中的示教点
- 无论是点击执行当前位置还是开始循环，机械臂产生的运动均可以通过紧急停止来立马停在原地

配置工具使用
---------------------------------------------------

在V3.0.3版本及之后，插件中的关键配置信息统一由配置工具管理。这样便于用户集中维护系统参数，降低配置复杂度。通过独立的配置工具，用户可以集中的修改诸如DOMAIN_ID还有DDS类型，改变以往修改参数需要深入到工程目录中的脚本或者配置文件中挨个修改，不小心会导致修改格式错误变砖。

进入/opt/fairino_art_plugin目录下，运行改目录下runconfigeditor.sh脚本，可以看到配置编辑器的主界面，如下图所示：
   
.. limage:: 009.png
   :align: center
   :width: 6in

.. centered:: 图表 3-8 配置编辑器主界面

界面upgrade settings区是设置升级配置项的:

- Update Mode是升级模式选择，选项有all,program_only和custom，all代表升级的时候，升级包中的程序和yaml配置文件都会覆盖到文件目录中，这样不光软件可执行文件会更新，所有的yaml配置文件也会被覆盖。Program_only是只更新软件可执行文件，配置文件保留当前软件版本中的不变;
- Custeom update config是在custom启用的时候，会读取文本框里面的内容，升级程序只会更新用户指定的ros2功能包的配置文件，其他的都不变。

Runtime Settings是设置ROS_DOMAIN_ID和DDS类型的，以往设置这两个数据需要修改启动service脚本还有rqttool.sh脚本里面的值，现在只需要在这个界面中配置即可，不需要在其他地方再设置。

Command Controller Auto Execut Setting是用于fairino_hardware_command_controller中配置开机自执行指令的部分，以往需要在command_controller的install文件夹中自行写入yaml配置文件，现在只需要勾选Enable Auto Execute就可以开机，点击之后，下方会出现Add command按钮，点击按钮即可添加自执行指令函数名称和参数。