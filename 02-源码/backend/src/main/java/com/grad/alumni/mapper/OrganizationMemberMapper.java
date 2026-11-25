package com.grad.alumni.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.entity.OrganizationMember;
import org.apache.ibatis.annotations.Mapper;

/** OrganizationMember 数据访问 */
@Mapper
public interface OrganizationMemberMapper extends BaseMapper<OrganizationMember> {
}
