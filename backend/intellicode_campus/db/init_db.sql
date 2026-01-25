--A. 用户与基础模块 (User & Auth)
-- 用户表：集成人脸识别字段
CREATE TABLE `tb_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `username` varchar(150) NOT NULL COMMENT '登录账号',
  `password` varchar(128) NOT NULL COMMENT '加密密码',
  `role` tinyint(1) NOT NULL DEFAULT '1' COMMENT '角色: 1-学生, 2-教师, 3-管理员',
  `nickname` varchar(50) DEFAULT NULL COMMENT '姓名/昵称',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像路径',
  `face_feature` text COMMENT '核心创新点: 人脸识别特征值(128维向量数组)',
  `class_name` varchar(50) DEFAULT NULL COMMENT '所属班级(仅学生有效)',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户及人脸数据表';

-- 系统公告表
CREATE TABLE `tb_notice` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL COMMENT '标题',
  `content` longtext NOT NULL COMMENT '公告内容(富文本)',
  `author_id` bigint(20) NOT NULL COMMENT '发布人ID',
  `type` tinyint(1) DEFAULT '1' COMMENT '1-普通公告, 2-竞赛通知',
  `publish_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统公告表';

--B. 课程与作业模块 (Course & Assignment)
-- 课程信息表
CREATE TABLE `tb_course` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL COMMENT '课程名称',
  `teacher_id` bigint(20) NOT NULL COMMENT '关联教师ID',
  `category` varchar(50) COMMENT '课程类型(如Python基础)',
  `cover_img` varchar(255) COMMENT '封面图',
  `description` text COMMENT '课程简介',
  `view_count` int(11) DEFAULT '0' COMMENT '浏览量(用于看板统计)',
  `status` tinyint(1) DEFAULT '1' COMMENT '1-上架, 0-下架',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='课程主表';

-- 作业发布表
CREATE TABLE `tb_assignment` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `course_id` bigint(20) NOT NULL COMMENT '所属课程',
  `title` varchar(100) NOT NULL,
  `requirements` text COMMENT '作业要求',
  `deadline` datetime NOT NULL COMMENT '截止时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='作业发布表';

-- 作业提交表 (关联 Echarts 可视化数据源)
CREATE TABLE `tb_assignment_submission` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `assignment_id` bigint(20) NOT NULL,
  `student_id` bigint(20) NOT NULL,
  `file_path` varchar(255) COMMENT '作业文件路径',
  `content` text COMMENT '文本内容',
  `score` decimal(5,2) DEFAULT NULL COMMENT '得分',
  `teacher_comment` text COMMENT '教师评语',
  `status` tinyint(1) DEFAULT '0' COMMENT '0-未批改, 1-已批改',
  `submit_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='作业提交记录表';

--C. 编程竞赛与题库模块 (Competition & Judge)
-- 竞赛信息表
CREATE TABLE `tb_competition` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL COMMENT '竞赛名称',
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `description` text COMMENT '竞赛规则',
  `is_active` tinyint(1) DEFAULT '0' COMMENT '是否开启报名',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='编程竞赛表';

-- 编程题目表 (支持OJ判题)
CREATE TABLE `tb_problem` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL COMMENT '题目名称',
  `difficulty` varchar(10) COMMENT '简单/中等/困难',
  `content` longtext NOT NULL COMMENT '题目描述(支持Markdown)',
  `input_desc` text COMMENT '输入描述',
  `output_desc` text COMMENT '输出描述',
  `test_cases` json COMMENT '核心: 测试用例JSON [{"in":"1 1", "out":"2"}]',
  `time_limit` int(11) DEFAULT '1000' COMMENT '时间限制(ms)',
  `memory_limit` int(11) DEFAULT '256' COMMENT '内存限制(MB)',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='编程题库表';

-- 竞赛报名表
CREATE TABLE `tb_enrollment` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `competition_id` bigint(20) NOT NULL,
  `student_id` bigint(20) NOT NULL,
  `status` tinyint(1) DEFAULT '0' COMMENT '0-审核中, 1-已通过, 2-拒绝',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='竞赛报名表';

-- 评测记录/代码提交表
CREATE TABLE `tb_judge_record` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `student_id` bigint(20) NOT NULL,
  `problem_id` bigint(20) NOT NULL,
  `competition_id` bigint(20) DEFAULT NULL COMMENT '如果是在比赛中提交则填此ID',
  `code` longtext NOT NULL COMMENT '提交的代码',
  `language` varchar(20) NOT NULL COMMENT 'Python/C++/Java',
  `status` varchar(20) COMMENT '判题结果: AC, WA, TLE, RE',
  `score` int(11) DEFAULT '0' COMMENT '判题得分',
  `ai_advice` text COMMENT '创新点: AI助手给出的代码优化建议',
  `submit_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='代码评测记录表';