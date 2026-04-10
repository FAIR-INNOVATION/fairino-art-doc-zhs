
SDK函数介绍
================================================

.. toctree:: 
    :maxdepth: 5

接口调用返回值类型：

.. code-block:: c++
    :linenos:

    typedef enum _ARMErrorCode{
    }ARMErrorCode;

机械臂的SDK函数介绍
-----------------------------------------------------

实例化机械臂
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  实例化机械臂
    * @param [in] robotype 机械臂型号
    * @param [in] robotname 单臂、左臂或者右臂
    * @param [in] 机械臂DH参数补偿值
    **/
    SingleRobot(int robotype, RobotName robotname, double DHCompensations[28] = nullptr);

关闭机械臂
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  关闭机械臂
    **/
    ~SingleRobot();

关节空间运动
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  关节空间运动
    * @param [in] destJointPos   目标点关节位置，单位deg
    * @param [in] velocity 速度百分比，范围[0-100]
    * @param [in] acceleration 加速度百分比，范围[0-100]，暂不开放
    * @param [out] errMsg 错误信息打印
    * @return 错误码
    **/
    ARMErrorCode MoveJ(double* destJointPos, double velocity, double acceleration, char errMsg[1024]);

关节空间运动代码示例-单臂
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    int MoveJTest()
    {
        SingleRobot robot(SingleRobot::ART3_R7, SingleRobot::LeftArm);        // 实例化机械臂

        // 目标点点位信息
        double j1_left[7] = {10, 10, 10, 10, 10, -10, 10};  // 点位数据仅供参考
        double velocity = 20;
        double acceleration = 20;
        robot.SetSpeed(10);     // 设置最大运动速度
        robot.SetAccScale(10);  // 设置运动加速度
        char errMsg[1024];
        ARMErrorCode rtnCode = robot.MoveJ(j1_left, velocity, acceleration, errMsg);
        if (rtnCode != ARMErrorCode::Success)
        {
            return -1;
        }
        // 判断是否运动完成
        while(true)
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(1000));
            uint8_t state;
            robot.GetRobotMotionDone(state);
            if (state == 1)
            {
                break;
            }
        }
        printf("moveJ errorcode: %d\n", rtnCode);

        return 0;
    }

关节空间运动代码示例-双臂
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    int MoveJTest2()
    {
        SingleRobot robot_left(SingleRobot::ART3_R7, SingleRobot::LeftArm);        // 实例化机械臂-左臂
        SingleRobot robot_right(SingleRobot::ART3_R7, SingleRobot::RightArm);      // 实例化机械臂-右臂

        // 目标点点位信息
        double j1_left[7] = {10, 10, 10, 10, 10, -10, 10};
        double j1_right[7] = {10, 10, 10, 10, 10, -10, 10};
        double velocity = 20;
        double acceleration = 20;
        robot_left.SetSpeed(10);     // 设置最大运动速度
        robot_left.SetAccScale(10);  // 设置运动加速度
        robot_right.SetSpeed(10);     // 设置最大运动速度
        robot_right.SetAccScale(10);  // 设置运动加速度
        char errMsg[1024];
        ARMErrorCode rtnCode = robot_left.MoveJ(j1_left, velocity, acceleration, errMsg);
        if (rtnCode != ARMErrorCode::Success)
        {
            return -1;
        }
        memset(errMsg, 0, 1024);
        rtnCode = robot_right.MoveJ(j1_right, velocity, acceleration, errMsg);
        if (rtnCode != ARMErrorCode::Success)
        {
            return -1;
        }
        // 判断是否运动完成
        uint8_t state_left = 0;
        uint8_t state_right = 0;
        while(true)
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(1000));
            
            robot_left.GetRobotMotionDone(state_left);
            robot_right.GetRobotMotionDone(state_right);
            if (state_left == 1 && state_right == 1)
            {
                break;
            }
        }
        printf("moveJ errorcode: %d\n", rtnCode);

        return 0;
    }

笛卡尔空间点到点运动
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  笛卡尔空间点到点运动
    * @param [in] destCartPos 目标点笛卡尔位姿[mm, deg]
    * @param [in] destArmAngle 目标点机械臂臂角，单位deg
    * @param [in] velocity 速度百分比，范围[0-100]
    * @param [in] acceleration 加速度百分比，范围[0-100]，暂不开放
    * @param [out] errMsg 错误信息打印
    * @return 错误码
    **/
    ARMErrorCode MoveP(double* destCartPos, double destArmAngle, double velocity, double acceleration, char errMsg[1024]);

笛卡尔空间直线运动
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  笛卡尔空间直线运动
    * @param [in] destCartPos   目标点笛卡尔位姿[mm, deg]
    * @param [in] destArmAngle 目标点机械臂臂角，单位deg
    * @param [in] velocity 速度百分比，范围[0-100]
    * @param [in] acceleration 加速度百分比，范围[0-100]，暂不开放
    * @param [out] errMsg 错误信息打印
    * @return 错误码
    **/
    ARMErrorCode MoveL(double* destCartPos, double destArmAngle, double velocity, double acceleration, char errMsg[1024]);

笛卡尔空间直线运动代码示例-单臂
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    int MoveLTest()
    {
        SingleRobot robot(SingleRobot::ART3_R7, SingleRobot::LeftArm);        // 实例化机械臂

        // 笛卡尔空间直线运动轨迹规划
        double j0_left[7] = {10, 10, 10, 10, 10, -10, 10};
        double desc_pos1_left[6] = {148.545536, 14.373573, 791.612359, 14.266475, 4.332141, 29.863598};
        double armAngle1_left = 351.959826;
        double velocity = 20;
        double acceleration = 20;
        robot.SetSpeed(10);     // 设置最大运动速度
        robot.SetAccScale(10);  // 设置运动加速度
        char errMsg[1024];
        ARMErrorCode rtnCode = robot.MoveJ(j0_left, velocity, acceleration, errMsg);  // 运动到直线轨迹起点
        if (rtnCode != ARMErrorCode::Success)
        {
            return -1;
        }
        // 判断运动是否完成
        while(true)
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(1000));
            uint8_t state;
            robot.GetRobotMotionDone(state);
            if (state == 1)
            {
                break;
            }
        }

        memset(errMsg, 0, 1024);
        rtnCode = robot.MoveL(desc_pos1_left, armAngle1_left, velocity, acceleration, errMsg);
        if (rtnCode != ARMErrorCode::Success)
        {
            return -1;
        }
        // 判断运动是否完成
        while(true)
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(1000));
            uint8_t state;
            robot.GetRobotMotionDone(state);
            if (state == 1)
            {
                break;
            }
        }
        printf("moveL errorcode: %d\n", rtnCode);

        return 0;
    }

笛卡尔空间直线运动代码示例-双臂
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    int MoveLTest2()
    {
        SingleRobot robot_left(SingleRobot::ART3_R7, SingleRobot::LeftArm);        // 实例化机械臂-左臂
        SingleRobot robot_right(SingleRobot::ART3_R7, SingleRobot::RightArm);      // 实例化机械臂-右臂

        // 笛卡尔空间直线运动轨迹规划
        double j0_left[7] = {10, 10, 10, 10, 10, -10, 10};
        double j0_right[7] = {10, 10, 10, 10, 10, -10, 10};
        double desc_pos1_left[6] = {148.545536, 14.373573, 791.612359, 14.266475, 4.332141, 29.863598};
        double armAngle1_left = 351.959826;
        double desc_pos1_right[6] = {148.545536, 14.373573, 791.612359, 14.266475, 4.332141, 29.863598};
        double armAngle1_right = 351.959826;
        double velocity = 20;
        double acceleration = 20;
        robot_left.SetSpeed(10);     // 设置最大运动速度
        robot_left.SetAccScale(10);  // 设置运动加速度
        robot_right.SetSpeed(10);     // 设置最大运动速度
        robot_right.SetAccScale(10);  // 设置运动加速度
        char errMsg[1024];

        // 左右臂运动到直线轨迹起点
        ARMErrorCode rtnCode = robot_left.MoveJ(j0_left, velocity, acceleration, errMsg);
        if (rtnCode != ARMErrorCode::Success)
        {
            return -1;
        }
        memset(errMsg, 0, 1024);
        rtnCode = robot_right.MoveJ(j0_right, velocity, acceleration, errMsg);
        if (rtnCode != ARMErrorCode::Success)
        {
            return -1;
        }
        // 判断是否运动完成
        uint8_t state_left = 0;
        uint8_t state_right = 0;
        while(true)
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(1000));
            robot_left.GetRobotMotionDone(state_left);
            robot_right.GetRobotMotionDone(state_right);
            if (state_left == 1 && state_right == 1)
            {
                break;
            }
        }

        memset(errMsg, 0, 1024);
        rtnCode = robot_left.MoveL(desc_pos1_left, armAngle1_left, velocity, acceleration, errMsg);
        if (rtnCode != ARMErrorCode::Success)
        {
            return -1;
        }
        memset(errMsg, 0, 1024);
        rtnCode = robot_right.MoveL(desc_pos1_right, armAngle1_right, velocity, acceleration, errMsg);
        if (rtnCode != ARMErrorCode::Success)
        {
            return -1;
        }
        // 判断运动是否完成
        state_left = 0;
        state_right = 0;
        while(true)
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(1000));
            robot_left.GetRobotMotionDone(state_left);
            robot_right.GetRobotMotionDone(state_right);
            if (state_left == 1 && state_right == 1)
            {
                break;
            }
        }
        printf("moveL errorcode: %d\n", rtnCode);

        return 0;
    }

笛卡尔空间圆弧运动
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  笛卡尔空间圆弧运动
    * @param [in] midCartPos   中间点笛卡尔位姿，单位 [mm deg]
    * @param [in] midArmAngle 中间点机械臂臂角，单位deg
    * @param [in] destCartPos   目标点笛卡尔位姿，单位 [mm deg]
    * @param [in] destArmAngle 目标点机械臂臂角，单位deg
    * @param [in] velocity 速度百分比，范围[0-100]
    * @param [in] acceleration 加速度百分比，范围[0-100]，暂不开放
    * @param [out] errMsg 错误信息打印
    * @return 错误码
    **/
    ARMErrorCode MoveC(double* midCartPos, double midArmAngle, double* destCartPos, double destArmAngle, double velocity, double acceleration, char errMsg[1024]);

笛卡尔空间圆弧运动代码示例-单臂
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    int MoveCTest()
    {
        SingleRobot robot(SingleRobot::ART3_R7, SingleRobot::LeftArm);        // 实例化机械臂

        // 圆弧起点、中间点、目标点点位信息
        double desc_pos1_left[6] = {148.545536, 14.373573, 791.612359, 14.266475, 4.332141, 29.863598};
        double armAngle1_left = 351.959826;
        double desc_pos2_left[6] = {237.686578, 36.090539, 763.929631, 16.922444, 13.941801, 30.475488};
        double armAngle2_left = 352.413796;
        double desc_pos3_left[6] = {321.576660, 56.804783, 723.049930, 19.871510, 23.501873, 31.687545};
        double armAngle3_left = 352.574131;
        double velocity = 10;
        double acceleration = 10;
        robot.SetSpeed(10);     // 设置最大运动速度
        robot.SetAccScale(10);  // 设置运动加速度

        // 运动到圆弧轨迹起点
        char errMsg[1024];
        ARMErrorCode rtnCode = robot.MoveP(desc_pos1_left, armAngle1_left, velocity, acceleration, errMsg);
        if (rtnCode != ARMErrorCode::Success)
        {
            return -1;
        }
        // 判断是否运动完成
        while(true)
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(1000));
            uint8_t state;
            robot.GetRobotMotionDone(state);
            if (state == 1)
            {
                break;
            }
        }
        printf("moveJ errorcode: %d\n", rtnCode);

        // 笛卡尔空间圆弧运动轨迹规划
        memset(errMsg, 0, 1024);
        rtnCode = robot.MoveC(desc_pos2_left, armAngle2_left, desc_pos3_left, armAngle3_left, velocity, acceleration, errMsg);
        if (rtnCode != ARMErrorCode::Success)
        {
            return -1;
        }
        // 判断是否运动完成
        while(true)
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(1000));
            uint8_t state;
            robot.GetRobotMotionDone(state);
            if (state == 1)
            {
                break;
            }
        }
        printf("moveC errorcode: %d\n", rtnCode);

        return 0;
    }

笛卡尔空间圆弧运动代码示例-双臂
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    int MoveCTest2()
    {
        SingleRobot robot_left(SingleRobot::ART3_R7, SingleRobot::LeftArm);        // 实例化机械臂-左臂
        SingleRobot robot_right(SingleRobot::ART3_R7, SingleRobot::RightArm);      // 实例化机械臂-右臂

        // 圆弧起点、中间点、目标点点位信息
        double desc_pos1_left[6] = {148.545536, 14.373573, 791.612359, 14.266475, 4.332141, 29.863598};
        double armAngle1_left = 351.959826;
        double desc_pos1_right[6] = {148.545536, 14.373573, 791.612359, 14.266475, 4.332141, 29.863598};
        double armAngle1_right = 351.959826;
        double desc_pos2_left[6] = {237.686578, 36.090539, 763.929631, 16.922444, 13.941801, 30.475488};
        double armAngle2_left = 352.413796;
        double desc_pos2_right[6] = {237.686578, 36.090539, 763.929631, 16.922444, 13.941801, 30.475488};
        double armAngle2_right = 352.413796;
        double desc_pos3_left[6] = {321.576660, 56.804783, 723.049930, 19.871510, 23.501873, 31.687545};
        double armAngle3_left = 352.574131;
        double desc_pos3_right[6] = {321.576660, 56.804783, 723.049930, 19.871510, 23.501873, 31.687545};
        double armAngle3_right = 352.574131;
        double velocity = 10;
        double acceleration = 10;
        robot_left.SetSpeed(10);     // 设置最大运动速度
        robot_left.SetAccScale(10);  // 设置运动加速度
        robot_right.SetSpeed(10);     // 设置最大运动速度
        robot_right.SetAccScale(10);  // 设置运动加速度
        char errMsg[1024];

        // 左右臂运动到圆弧轨迹起点
        ARMErrorCode rtnCode = robot_left.MoveP(desc_pos1_left, armAngle1_left, velocity, acceleration, errMsg);
        if (rtnCode != ARMErrorCode::Success)
        {
            return -1;
        }
        memset(errMsg, 0, 1024);
        rtnCode = robot_right.MoveP(desc_pos1_right, armAngle1_right, velocity, acceleration, errMsg);
        if (rtnCode != ARMErrorCode::Success)
        {
            return -1;
        }
        // 判断是否运动完成
        uint8_t state_left = 0;
        uint8_t state_right = 0;
        while(true)
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(1000));
            robot_left.GetRobotMotionDone(state_left);
            robot_right.GetRobotMotionDone(state_right);
            if (state_left == 1 && state_right == 1)
            {
                break;
            }
        }

        // 笛卡尔空间圆弧运动轨迹规划
        memset(errMsg, 0, 1024);
        rtnCode = robot_left.MoveC(desc_pos2_left, armAngle2_left, desc_pos3_left, armAngle3_left, velocity, acceleration, errMsg);
        if (rtnCode != ARMErrorCode::Success)
        {
            return -1;
        }
        memset(errMsg, 0, 1024);
        rtnCode = robot_right.MoveC(desc_pos2_right, armAngle2_right, desc_pos3_right, armAngle3_right, velocity, acceleration, errMsg);
        if (rtnCode != ARMErrorCode::Success)
        {
            return -1;
        }
        // 判断运动是否完成
        state_left = 0;
        state_right = 0;
        while(true)
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(1000));
            robot_left.GetRobotMotionDone(state_left);
            robot_right.GetRobotMotionDone(state_right);
            if (state_left == 1 && state_right == 1)
            {
                break;
            }
        }
        printf("moveC errorcode: %d\n", rtnCode);

        return 0;
    }

笛卡尔空间伺服运动
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  笛卡尔空间伺服运动
    * @param [in] servo_cartPos   笛卡尔伺服运动轨迹点，[末端法兰坐标系位置、坐标系rpy角、机械臂臂角]，长度7*len，单位[mm、deg、deg]
    * @param [in] len   笛卡尔伺服运动轨迹点个数
    * @param [out] errMsg 错误信息打印
    * @return 错误码
    **/
    ARMErrorCode ServoCart(double* servo_cartPos, uint32_t len, char errMsg[1024]);

伺服运动开始
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief 伺服运动开始，配合ServoJ指令使用
    * @return 错误码
    **/
    ARMErrorCode ServoMoveStart();

伺服运动结束
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief 伺服运动结束，配合ServoJ指令使用
    * @return 错误码
    **/
    ARMErrorCode ServoMoveEnd();

关节空间伺服模式运动
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  关节空间伺服模式运动
    * @param [in] jointPos   目标关节位置，单位deg
    * @param [in] period   指令下发周期，单位ms
    * @param [out] errMsg 错误信息打印
    * @return 错误码
    **/
    ARMErrorCode ServoJ(double* jointPos, int period, char errMsg[1024]);

关节空间伺服模式运动-单臂
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    int ServoJTest()
    {
        SingleRobot robot(SingleRobot::ART3_R7, SingleRobot::LeftArm);        // 实例化机械臂

        // 目标点点位信息
        double j1_left[7] = {10, 10, 10, 10, 10, -10, 10};
        double velocity = 20;
        double acceleration = 20;
        robot.SetSpeed(10);     // 设置最大运动速度
        robot.SetAccScale(10);  // 设置运动加速度
        char errMsg[1024];
        ARMErrorCode rtnCode = robot.MoveJ(j1_left, velocity, acceleration, errMsg);
        // if (rtnCode != ARMErrorCode::Success)
        // {
        //     return -1;
        // }
        // 判断是否运动完成
        while(true)
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(1000));
            uint8_t state;
            robot.GetRobotMotionDone(state);
            if (state == 1)
            {
                break;
            }
        }
        printf("moveJ errorcode: %d\n", rtnCode);

        int stepTime = 5;  // ms
        double speed = 5;
        double runTime = 1.0;  // s
        int totalNum = runTime*1000.0/stepTime;
        double nextJoint[7] = {0};

        memset(errMsg, 0, 1024);
        rtnCode = robot.ServoMoveStart();
        if (rtnCode != ARMErrorCode::Success)
        {
            return -1;
        }
        for (int i = 0; i < totalNum; i++)
        {
            for (int j = 0; j < 7; j++)
            {
                nextJoint[j] = j1_left[j] + i*1.0/totalNum*speed;
            }
            rtnCode = robot.ServoJ(nextJoint, stepTime, errMsg);
            if (rtnCode != ARMErrorCode::Success)
            {
                std::cout << (int)rtnCode << std::endl;
                break;
            }
        }
        printf("servoJ errorcode: %d\n", rtnCode);
        rtnCode = robot.ServoMoveEnd();
        if (rtnCode != ARMErrorCode::Success)
        {
            return -1;
        }
    
        return 0;
    }

关节空间伺服模式运动-双臂
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    int ServoJTest2()
    {
        std::thread th_left([]{
            SingleRobot robot_left(SingleRobot::ART3_R7, SingleRobot::LeftArm);        // 实例化机械臂-左臂
            // 目标点点位信息
            double j1_left[7] = {10, 10, 10, 10, 10, -10, 10};
            double velocity = 20;
            double acceleration = 20;
            robot_left.SetSpeed(10);     // 设置最大运动速度
            robot_left.SetAccScale(10);  // 设置运动加速度
            char errMsg_l[1024];

            ARMErrorCode rtnCode = robot_left.MoveJ(j1_left, velocity, acceleration, errMsg_l);
            if (rtnCode != ARMErrorCode::Success)
            {
                return -1;
            }
            // 判断是否运动完成
            uint8_t state_left = 0;
            while(true)
            {
                std::this_thread::sleep_for(std::chrono::milliseconds(1000));
                
                robot_left.GetRobotMotionDone(state_left);
                if (state_left == 1)
                {
                    break;
                }
            }
            printf("left arm moveJ errorcode: %d\n", rtnCode);

            int stepTime = 5;  // ms
            double speed = 5;
            double runTime = 1.0;  // s
            int totalNum = runTime*1000.0/stepTime;
            double nextJoint[7] = {0};
            ARMErrorCode rtnCode_l = robot_left.ServoMoveStart();
            if (rtnCode_l != ARMErrorCode::Success)
            {
                std::cout << (int)rtnCode_l << std::endl;
                robot_left.ServoMoveEnd();
                return -1;
            }
            for (int i = 0; i < totalNum; i++)
            {
                for (int j = 0; j < 7; j++)
                {
                    nextJoint[j] = j1_left[j] + i*1.0/totalNum*speed;
                }
                rtnCode_l = robot_left.ServoJ(nextJoint, stepTime, errMsg_l);
                if (rtnCode_l != ARMErrorCode::Success)
                {
                    break;
                }
            }
            printf("servoJ errorcode: %d\n", rtnCode_l);
            rtnCode_l = robot_left.ServoMoveEnd();
            if (rtnCode_l != ARMErrorCode::Success)
            {
                return -1;
            }
        });
        if (th_left.joinable())
        {
            th_left.join();
        }

        std::this_thread::sleep_for(std::chrono::microseconds(1000));
        std::thread th_right([]{
            SingleRobot robot_right(SingleRobot::ART3_R7, SingleRobot::RightArm);      // 实例化机械臂-右臂
            // 目标点点位信息
            double j1_right[7] = {10, 10, 10, 10, 10, -10, 10};
            double velocity = 20;
            double acceleration = 20;
            robot_right.SetSpeed(10);     // 设置最大运动速度
            robot_right.SetAccScale(10);  // 设置运动加速度
            char errMsg_r[1024];

            ARMErrorCode rtnCode = robot_right.MoveJ(j1_right, velocity, acceleration, errMsg_r);
            if (rtnCode != ARMErrorCode::Success)
            {
                return -1;
            }
            // 判断是否运动完成
            uint8_t state_right = 0;
            while(true)
            {
                std::this_thread::sleep_for(std::chrono::milliseconds(1000));
                
                robot_right.GetRobotMotionDone(state_right);
                if (state_right == 1)
                {
                    break;
                }
            }
            printf("right arm moveJ errorcode: %d\n", rtnCode);

            int stepTime = 5;  // ms
            double speed = 5;
            double runTime = 1.0;  // s
            int totalNum = runTime*1000.0/stepTime;
            double nextJoint[7] = {0};
            ARMErrorCode rtnCode_r = robot_right.ServoMoveStart();
            if (rtnCode_r != ARMErrorCode::Success)
            {
                std::cout << (int)rtnCode_r << std::endl;
                robot_right.ServoMoveEnd();
                return -1;
            }
            for (int i = 0; i < totalNum; i++)
            {
                for (int j = 0; j < 7; j++)
                {
                    nextJoint[j] = j1_right[j] + i*1.0/totalNum*speed;
                }
                rtnCode_r = robot_right.ServoJ(nextJoint, stepTime, errMsg_r);
                if (rtnCode_r != ARMErrorCode::Success)
                {
                    break;
                }
            }
            printf("servoJ errorcode: %d\n", rtnCode_r);
            rtnCode_r = robot_right.ServoMoveEnd();
            if (rtnCode_r != ARMErrorCode::Success)
            {
                return -1;
            }
        });
        if (th_right.joinable())
        {
            th_right.join();
        }

        return 0;
    }

停止运动
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  停止运动
    * @return 错误码
    **/
    ARMErrorCode StopMotion();

设置工具坐标系
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  设置工具坐标系
    * @param [in] toolNum 工具坐标系id 范围1-19
    * @param [in] corrd 工具坐标系 {x, y, z, rx, ry, rz}, 单位：[mm, deg]
    * @return 错误码
    **/
    ARMErrorCode SetToolCorrd(int toolNum, double* corrd);

设置机械臂加速度百分比
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  设置机械臂加速度百分比
    * @param [in] scale 加速度百分比
    * @return 错误码
    **/
    ARMErrorCode SetAccScale(double scale);

设置全局速度百分比
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  设置全局速度百分比
    * @param [in] speed 速度百分比
    * @return 错误码
    **/
    ARMErrorCode SetSpeed(double speed);

正运动学求解
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  正运动学求解
    * @param [in] joint_val 关节位置，单位deg
    * @param [out] xyzrpy 笛卡尔位姿
    * @param [out] arm_angle 机械臂臂角
    * @return 错误码
    **/
    ARMErrorCode GetForwardKin(double* joint_val, double* desc_pos, double& arm_angle);

逆运动学求解
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  逆运动学求解
    * @param [in] trans 末端笛卡尔位姿，单位 [mm deg]
    * @param [in] arm_angle 机械臂臂角，单位deg
    * @param [out] joint_val 关节位置，单位deg
    * @return 错误码
    **/
    ARMErrorCode GetInverseKin(double* desc_pos, double arm_angle, double* joint_val);

逆运动学求解(参考位置)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  逆运动学求解，参考指定关节位置求解
    * @param [in] trans 末端笛卡尔位姿，单位 [mm deg]
    * @param [in] arm_angle 机械臂臂角，单位deg
    * @param [in] ref_joint_val 参考关节位置，单位deg
    * @param [out] joint_val 关节位置，单位deg
    * @return 错误码
    **/
    ARMErrorCode GetInverseKinRef(double* desc_pos, double arm_angle, double* ref_joint_val, double* joint_val);

获取当前关节位置(角度)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  获取当前关节位置(角度)
    * @param [out] joint_pos，单位[deg]
    * @return 错误码
    **/
    ARMErrorCode GetActualJointPosDegree(double joint_pos[7]);

查询机械臂运动是否完成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  查询机械臂运动是否完成
    * @param [out] state，0-未完成，1-完成
    * @return 错误码
    **/
    ARMErrorCode GetRobotMotionDone(uint8_t& state);

获取当前末端速度
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  获取当前末端速度
    * @param [out] eeVal，单位[mm/s、deg/s]
    * @return 错误码
    **/
    ARMErrorCode GetEEVel(double eeVal[6]);

关节使能
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  关节使能
    * @param [in] joint_id 关节序号 0-机械臂所有关节，1-7-机械臂对应关节
    * @return 错误码
    **/
    ARMErrorCode AxisEnable(int joint_id);

关节去使能
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  关节去使能
    * @param [in] joint_id 关节序号 0-机械臂所有关节，1-7-机械臂对应关节
    * @return 错误码
    **/
    ARMErrorCode AxisDisable(int joint_id);

关节校零
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  关节校零
    * @param [in] joint_id 关节序号 0-机械臂所有关节，1-7-机械臂对应关节
    * @return 错误码
    **/
    ARMErrorCode AxisZeroing(int joint_id);

清除控制器错误
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  清除控制器错误
    * @return 错误码
    **/
    ARMErrorCode AxisResetError();

获取当前末端法兰位姿
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  获取当前末端法兰位姿
    * @param [in] jointPos 当前机械臂关节位置，单位deg
    * @param [out] fLangePos [末端法兰位置、姿态、机械臂臂角]，单位[mm、deg、deg]
    * @return 错误码
    **/
    ARMErrorCode GetActualToolFlangePose(double jointPos[7], double fLangePos[7]);

设置机械臂正限位
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  设置机械臂正限位
    * @param [in] limitPositive 关节正限位，单位deg
    * @return 错误码
    **/
    ARMErrorCode SetLimitPositive(double limitPositive[7]);

设置机械臂负限位
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  设置机械臂负限位
    * @param [in] limitNegative 关节负限位，单位deg
    * @return 错误码
    **/
    ARMErrorCode SetLimitNegative(double limitNegative[7]);

获取关节软限位角度
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  获取机械臂关节软限位角度
    * @param [out] limitNegative 关节负限位，单位deg
    * @param [out] limitPositive 关节正限位，单位deg
    * @return 错误码
    **/
    ARMErrorCode GetJointSoftLimitDeg(double limitNegative[7], double limitPositive[7]);

腰部的SDK函数介绍(存在腰部关节的情况下)
-----------------------------------------------------------------------------------------

实例化腰部
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  实例化腰部
    **/
    RobotWaist();

关闭腰部
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  关闭腰部
    **/
    ~RobotWaist();

关节空间运动
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  关节空间运动
    * @param [in] destJointPos   目标点关节位置，单位deg
    * @param [in] velocity 速度百分比，范围[0-100]
    * @param [in] acceleration 加速度百分比，范围[0-100]，暂不开放
    * @param [out] errMsg 错误信息打印
    * @return 错误码
    **/
    ARMErrorCode MoveJ(double* destJointPos, double velocity, double acceleration, char errMsg[1024]);

停止运动
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  停止运动
    * @return 错误码
    **/
    ARMErrorCode StopMotion();

获取当前关节位置(角度)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  获取当前关节位置(角度)
    * @param [out] joint_pos，单位[deg]
    * @return 错误码
    **/
    ARMErrorCode GetActualJointPosDegree(double* joint_pos);

查询运动是否完成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    @brief  查询运动是否完成
    * @param [out] state，0-未完成，1-完成
    * @return 错误码
    **/
    ARMErrorCode GetRobotMotionDone(uint8_t& state);

关节使能
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  关节使能
    * @param [in] joint_id 关节序号 0-腰部所有关节使能 1,2,...-腰部对应关节
    * @return 错误码
    **/
    ARMErrorCode AxisEnable(int joint_id);

关节去使能
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  关节去使能
    * @param [in] joint_id 关节序号 0-腰部所有关节使能 1,2,...-腰部对应关节
    * @return 错误码
    **/
    ARMErrorCode AxisDisable(int joint_id);

关节校零
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  关节校零
    * @param [in] joint_id 关节序号 0-腰部所有关节使能 1,2,...-腰部对应关节
    * @return 错误码
    **/
    ARMErrorCode AxisZeroing(int joint_id);

清除控制器错误
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  清除控制器错误
    * @return 错误码
    **/
    ARMErrorCode AxisResetError();

设置腰部正限位
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  设置腰部正限位
    * @param [in] limitPositive 关节正限位，单位deg
    * @return 错误码
    **/
    ARMErrorCode SetLimitPositive(double* limitPositive);

设置腰部负限位
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  设置腰部负限位
    * @param [in] limitNegative 关节负限位，单位deg
    * @return 错误码
    **/
    ARMErrorCode SetLimitNegative(double* limitNegative);

获取关节软限位角度
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  获取腰部关节软限位角度
    * @param [out] limitNegative 关节负限位，单位deg
    * @param [out] limitPositive 关节正限位，单位deg
    * @return 错误码
    **/
    ARMErrorCode GetJointSoftLimitDeg(double* limitNegative, double* limitPositive);

设置腰部加速度百分比
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  设置腰部加速度百分比
    * @param [in] scale 加速度百分比
    * @return 错误码
    **/
    ARMErrorCode SetAccScale(double scale);

设置腰部全局速度百分比
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  设置腰部全局速度百分比
    * @param [in] speed 速度百分比
    * @return 错误码
    **/
    ARMErrorCode SetSpeed(double speed);

工具部分的SDK函数介绍
------------------------------------------------------------

实例化工具类
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  实例化工具类
    **/
    RobotTool();

关闭工具类
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  关闭工具类对象
    **/
    ~RobotTool();

设置机器人配置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  设置机器人配置-FAIRINO-ARTPlugin插件升级
    * @param [in] mode 0-单臂7轴配置 1-双臂14轴配置 2-双臂+腰16轴配置
    * @return 错误码
    **/
    ARMErrorCode RobotFrConfig(int mode);

日志导出
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  日志导出
    * @return 错误码
    **/
    ARMErrorCode RobotPackLog();

数据记录
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  数据记录
    * @param [in] state 1-记录开始 0-记录结束并导出
    * @return 错误码
    **/
    ARMErrorCode RobotRecordData(int state);

SDK服务端部署
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
    :linenos:

    /**
    * @brief  SDK服务端部署
    * @param [in] filepath 升级包全路径
    * @return 错误码
    **/
    ARMErrorCode UpdateSDKServer(std::string filepath);