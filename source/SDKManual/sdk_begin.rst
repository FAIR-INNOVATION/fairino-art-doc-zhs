SDK服务端部署及启动
================================================

.. toctree:: 
    :maxdepth: 5

SDK服务端升级
-----------------------------------------------------

**Step1**：将SDK服务端升级文件复制到控制器内，并解压得到升级包和升级脚本。

.. limage:: 001.png
   :align: center
   :width: 6in

.. centered:: 图表 1-1 FAIRINO_ARTSDK升级文件内容

**Step2**：打开终端，执行升级脚本，输入参数(升级包路径)。

.. limage:: 002.png
   :align: center
   :width: 6in

.. centered:: 图表 1-2 SDK服务端升级

**Step3**：执行sudo nano /etc/systemd/system/fairino_sdk.service，修改SDK服务端自启动脚本中的域和DDS的设置，最后重启机器人。

.. limage:: 003.png
   :align: center
   :width: 6in

.. centered:: 图表 1-3 SDK Server启动域和DDS设置

.. note:: V3.0.4版本 SDK服务端建议使用升级脚本进行升级SDK服务端，以确保SDK服务端开机自启动功能正常运行。

SDK服务端启动
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

v3.0.4版本 SDK服务端采用开机自启动的方式，在关节没有报错的前提下50S内SDK服务端会完成启动。可以通过如下指令查看SDK服务端日志信息。

.. limage:: 005.png
   :align: center
   :width: 6in

.. centered:: 图表 1-4 SDK Server日志

.. note:: 若开机SDK服务端启动后，机器人没有正常使能，请使用FAIRINO_ARTPlugin插件工具查看机器人关节驱动器是否故障码。
