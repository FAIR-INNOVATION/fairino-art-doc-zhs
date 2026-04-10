SDK服务端部署及启动
================================================

.. toctree:: 
    :maxdepth: 5

SDK服务端启动
-----------------------------------------------------

**Step1**：SDK服务端在启动之前，需要确定FAIRINO_ARTPlugin插件是否启动成功。

.. limage:: 001.png
   :align: center
   :width: 6in

.. centered:: 图表 1-1 FAIRINO_ARTPlugin插件启动结果

**Step2**：进入SDK包解压缩目录中，比如控制器默认部署路径是home/fairino/ros2_ws，找到如下文件runSDKServer.sh，并执行。

.. limage:: 002.png
   :align: center
   :width: 6in

.. centered:: 图表 1-2 SDK部署路径

**Step3**：在该路径打开bash命令窗口，然后输入./runSDKServer.sh，执行后，出现以下界面为成功。

.. limage:: 003.png
   :align: center
   :width: 6in

.. centered:: 图表 1-3 SDK Server启动页面

.. note:: 
    注意事项：
    1. runSDKServer.sh脚本启动之前，打开脚本查看是否设置ROS_DOMAIN_ID。