轨迹复现
=======================================================================

.. toctree:: 
    :maxdepth: 5

环境搭建
-------------------------------------------

**Step1**: 升级插件和SDK服务端，要求版本为V3.0.7及以下版本，升级完成后重启控制器。

**Step2**: 将 ROS2 Action 通信所需的接口功能包(fairino_sdk_server_interfaces)解压至上位机，通过 colcon 构建工具编译，生成相应的消息、服务及动作类型。如下图1所示。
   
.. limage:: 010.png
   :align: center
   :width: 6in

.. centered:: 图表 4-1 编译接口功能包

**Step3**: 编译完成后，执行 source install/setup.bash 加载工作空间环境变量，使 ROS2 Action 接口类型在当前终端环境中可用。然后使用 ROS2 Action 接口向机器人下发控制指令，并接收执行结果。如下图2所示。
   
.. limage:: 011.png
   :align: center
   :width: 6in

.. centered:: 图表 4-2 加载工作空间环境变量

轨迹复现功能介绍
-------------------------------------------------------

接口说明
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

获取指定关节运动速度。

.. list-table::
   :widths: 20 20 60
   :header-rows: 0
   :align: center

   * - **指令名称**
     - **功能描述**
     - **输入参数说明**

   * - StartJOG
     - 点动开始，可以设置关节点动和笛卡尔点动参数。
     - | args[0]: 0-左臂 1-右臂，单臂配置为0
       | args[1]: 0-关节点动 1-笛卡尔点动(基坐标系)
       | args[2]: 1-关节1/x,...,6-关节6/rz,7-关节7
       | args[3]: 0-负方向，1-正方向
       | args[4]: 速度百分比
       | args[5]: 加速度百分比
       | args[6]: 加加速度百分比
       | args[7]: 单次最大点动距离
      
   * - StopJOG
     - 停止点动
     - args[0]: 0-左臂 1-右臂，单臂配置为0
	
   * - RobotHoming
     - 机械臂回零点
     - | args[0]: 0-左臂 1-右臂，单臂配置为0
       | args[1]: 速度百分比
       | args[2]: 加速度百分比
       | args[3]: 加加速度百分比
       | args[4]: 是否阻塞 -1-非阻塞 0-阻塞
   	
   * - SetTPDStart
     - 开始轨迹记录
     - | args[0]: 0-左臂 1-右臂，单臂配置为0
       | args[1]: 0-关节位置
       | args[2]: 轨迹文件名
       | args[3]: 数据采样周期，2、4、8ms
        	
   * - SetTPDEnd
     - 停止轨迹记录。
     - args[0]: 0-左臂 1-右臂，单臂配置为0
        	
   * - GetTPDStartPose
     - 获取轨迹起始点位数据。
     - | args[0]: 0-左臂 1-右臂，单臂配置为0
       | args[1]: 轨迹文件名
         	
   * - MoveToTPDStart
     - 运动到轨迹记录起点
     - | args[0]: 0-左臂 1-右臂，单臂配置为0
       | args[1]: 轨迹文件名
       | args[2]: 运动类型0-PTP
       | args[3]: 运动速度百分比
            	
   * - LoadTPD
     - 轨迹预加载
     - | args[0]: 0-左臂 1-右臂，单臂配置为0
       | args[1]: 轨迹文件名
                	
   * - MoveTPD
     - 轨迹复现运动
     - | args[0]: 0-左臂 1-右臂，单臂配置为0
       | args[1]: 轨迹文件名
       | args[2]: 速度百分比
                  	
   * - SetTPDUpdate
     - 轨迹微调更新
     - | args[0]: 0-左臂 1-右臂，单臂配置为0
       | args[1]: 轨迹文件名
       | args[2]: 微调方法 1-点动微调 2-拖动微调
       | args[3]: 数据采样周期，2、4、8ms
                     	
   * - SetTPDDelete
     - 轨迹文件删除
     - | args[0]: 0-左臂 1-右臂，单臂配置为0
       | args[1]: 轨迹文件名
                       	
   * - GetTPDList
     - 获取当前轨迹列表
     - args[0]: 0-左臂 1-右臂，单臂配置为0
                      	
   * - SetSpeed
     - 设置全局速度百分比
     - | args[0]: 0-左臂 1-右臂，单臂配置为0
       | args[1]: 速度百分比
                      	
   * - SetAccScale
     - 设置全局加速度百分比
     - | args[0]: 0-左臂 1-右臂，单臂配置为0
       | args[1]: 加速度百分比
                      	
   * - GetSpeed
     - 获取全局速度百分比
     - args[0]: 0-左臂 1-右臂，单臂配置为0
                      	
   * - GetAccScale
     - 获取全局加速度百分比
     - args[0]: 0-左臂 1-右臂，单臂配置为0
                      	
   * - GetActualJointDeg
     - 获取当前机械臂关节位置
     - args[0]: 0-左臂 1-右臂，单臂配置为0
                      	
   * - GetRobotErrorCode
     - 获取机械臂错误码
     - args[0]: 参数为0
                      	
   * - PauseMotion
     - 暂停机械臂运动
     - args[0]: 0-左臂 1-右臂，单臂配置为0
                      	
   * - ResumeMotion
     - 恢复机械臂运动
     - args[0]: 0-左臂 1-右臂，单臂配置为0
                      	
   * - StopMotion
     - 停止机械臂运动
     - args[0]: 0-左臂 1-右臂，单臂配置为0
                      	
   * - ResetError
     - 清除错误
     - 无

调试用例
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

轨迹记录与复现使用案例：

.. code-block:: console
    :linenos:

    source install/setup.bash

    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1001, command: 'SetTPDStart(0,0,traj1,2)'}"    // 轨迹记录开始

    /* 按住拖动按钮进入拖动 */

    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1002, command: 'SetTPDEnd(0)'}"    // 轨迹记录结束

    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1003, command: 'LoadTPD(0,traj1)'}"    // 轨迹预加载
    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1004, command: 'MoveToTPDStart(0,traj1,0,50)'}"    // 运动到轨迹起点
    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1005, command: 'MoveTPD(0,traj1,10)'}"    // 轨迹复现

笛卡尔点动轨迹微调使用案例：

.. code-block:: console
    :linenos:

    source install/setup.bash

    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1001, command: 'LoadTPD(0,traj1)'}"    // 轨迹预加载
    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1002, command: 'MoveToTPDStart(0,traj1,0,50)'}"    // 运动到轨迹起点
    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1003, command: 'MoveTPD(0,traj1,10)'}"    // 轨迹复现

    /* 运动到待微调位置 */
    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1004, command: 'StopMotion(0)'}"    // 轨迹复现停止运动
    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1005, command: 'StartJOG(0,1,1,1,10,10,10,1)'}"    // 笛卡尔点动，延基坐标系X轴正方向最大移动1mm
    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1006, command: 'SetTPDUpdate(0,traj1,1,2)'}"    // 笛卡尔点动轨迹微调保存

    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1007, command: 'LoadTPD(0,traj1)'}"    // 轨迹预加载
    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1008, command: 'MoveToTPDStart(0,traj1,0,50)'}"    // 运动到轨迹起点
    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1009, command: 'MoveTPD(0,traj1,10)'}"    // 轨迹复现

拖动示教轨迹微调使用案例：

.. code-block:: console
    :linenos:

    source install/setup.bash

    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1001, command: 'LoadTPD(0,traj1)'}"    // 轨迹预加载
    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1002, command: 'MoveToTPDStart(0,traj1,0,50)'}"    // 运动到轨迹起点
    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1003, command: 'MoveTPD(0,traj1,10)'}"    // 轨迹复现

    /* 运动到待微调位置 */
    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1004, command: 'StopMotion(0)'}"    // 轨迹复现停止运动
    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1005, command: 'SetTPDStart(0,0,traj1_tmp,2)'}"    // 微调轨迹记录开始,注意轨迹命名格式，原轨迹+”_tmp”
    /* 按住拖动按钮进入拖动 */
    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1006, command: 'SetTPDEnd(0)'}"    // 微调轨迹记录结束
    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1007, command: 'SetTPDUpdate(0,traj1,2,2)'}"    // 拖动示教轨迹微调保存，注意轨迹文件名称

    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1008, command: 'LoadTPD(0,traj1)'}"    // 轨迹预加载
    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1009, command: 'MoveToTPDStart(0,traj1,0,50)'}"    // 运动到轨迹起点
    ros2 action send_goal /fairino_sdk/execute_command fairino_sdk_server_interfaces/action/ExecuteCommand "{client_request_id: 1010, command: 'MoveTPD(0,traj1,10)'}"    // 轨迹复现