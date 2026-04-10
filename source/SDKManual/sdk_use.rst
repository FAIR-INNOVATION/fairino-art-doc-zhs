
SDK客户端动态库使用
================================================

.. toctree:: 
    :maxdepth: 5


SDK库的使用需要在上位机上，SDK库会通过TCP连接与机器人控制器建立通讯，推荐使用Ubuntu系统，Windows系统暂时不支持。执行SDK所需要的文件目录如下所示。

.. limage:: 004.png
   :align: center
   :width: 4in

.. centered:: 图表 2-1 SDK库目录

.. note:: 
    注意事项：
    1.注意需要将libfairino_middleware_logger、libfairino_motion_planner和libkine_FR_7Axis动态库与libhumanorid_sdk动态库放到同一文件目录下。