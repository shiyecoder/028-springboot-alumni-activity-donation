package com.grad.alumni.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.entity.AlumniProfile;
import org.apache.ibatis.annotations.Mapper;

/** AlumniProfile 数据访问 */
@Mapper
public interface AlumniProfileMapper extends BaseMapper<AlumniProfile> {
}
