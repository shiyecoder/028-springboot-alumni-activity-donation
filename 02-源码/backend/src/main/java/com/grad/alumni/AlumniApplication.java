package com.grad.alumni;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/** 校友活动与捐赠项目管理系统启动类 */
@SpringBootApplication
@MapperScan("com.grad.alumni.mapper")
public class AlumniApplication {
    public static void main(String[] args) {
        SpringApplication.run(AlumniApplication.class, args);
    }
}
