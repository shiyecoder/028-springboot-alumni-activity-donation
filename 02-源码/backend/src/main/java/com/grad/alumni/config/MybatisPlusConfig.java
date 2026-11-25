package com.grad.alumni.config;

import com.baomidou.mybatisplus.annotation.DbType;
import com.baomidou.mybatisplus.extension.plugins.MybatisPlusInterceptor;
import com.baomidou.mybatisplus.extension.plugins.inner.PaginationInnerInterceptor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** 分页插件：所有列表接口使用服务端分页 */
@Configuration
public class MybatisPlusConfig {

    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor i = new MybatisPlusInterceptor();
        PaginationInnerInterceptor p = new PaginationInnerInterceptor(DbType.MYSQL);
        p.setMaxLimit(200L);
        i.addInnerInterceptor(p);
        return i;
    }
}
